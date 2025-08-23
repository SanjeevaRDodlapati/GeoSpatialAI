"""
Satellite imagery utilities for geospatial model implementations
Handles coordinate transformations, satellite data access, and spatial operations
"""

import numpy as np
import rasterio
from rasterio.crs import CRS
from rasterio.warp import transform_bounds, reproject, Resampling
from rasterio.windows import from_bounds
from pyproj import Transformer
import requests
from pathlib import Path
import logging
from typing import Tuple, List, Optional, Dict, Union
from datetime import datetime, timedelta
import geopandas as gpd
from shapely.geometry import box, Point, Polygon
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class SatelliteUtils:
    """Utilities for satellite data processing and coordinate operations"""
    
    def __init__(self):
        # Madagascar bounding box (approximate)
        self.madagascar_bounds = {
            'west': 43.2,
            'south': -25.6, 
            'east': 50.5,
            'north': -11.9
        }
        
        # Common satellite band configurations
        self.band_configs = {
            'sentinel2': {
                'blue': 2, 'green': 3, 'red': 4, 'rededge1': 5,
                'rededge2': 6, 'rededge3': 7, 'nir': 8, 'narrow_nir': 8,
                'water_vapor': 9, 'swir1': 11, 'swir2': 12
            },
            'landsat8': {
                'blue': 2, 'green': 3, 'red': 4, 'nir': 5,
                'swir1': 6, 'swir2': 7, 'pan': 8, 'cirrus': 9,
                'thermal1': 10, 'thermal2': 11
            }
        }
    
    def geographic_to_utm(self, lon: float, lat: float) -> Tuple[int, CRS]:
        """
        Convert geographic coordinates to appropriate UTM zone
        
        Args:
            lon: Longitude
            lat: Latitude
            
        Returns:
            tuple: (utm_zone, utm_crs)
        """
        utm_zone = int((lon + 180) / 6) + 1
        hemisphere = 'north' if lat >= 0 else 'south'
        utm_crs = CRS.from_string(f"+proj=utm +zone={utm_zone} +{hemisphere} +datum=WGS84")
        
        return utm_zone, utm_crs
    
    def reproject_image(self, 
                       src_image: np.ndarray,
                       src_transform: rasterio.Affine,
                       src_crs: CRS,
                       dst_crs: CRS,
                       dst_resolution: Optional[float] = None) -> Tuple[np.ndarray, rasterio.Affine]:
        """
        Reproject image to new coordinate system
        
        Args:
            src_image: Source image array
            src_transform: Source transform
            src_crs: Source CRS
            dst_crs: Destination CRS
            dst_resolution: Target resolution in destination units
            
        Returns:
            tuple: (reprojected_image, new_transform)
        """
        # Calculate destination transform and dimensions
        dst_transform, width, height = calculate_default_transform(
            src_crs, dst_crs, src_image.shape[-1], src_image.shape[-2], 
            *rasterio.transform.array_bounds(src_image.shape[-2], src_image.shape[-1], src_transform),
            resolution=dst_resolution
        )
        
        # Create destination array
        if src_image.ndim == 3:
            dst_image = np.zeros((src_image.shape[0], height, width), dtype=src_image.dtype)
            
            for band in range(src_image.shape[0]):
                reproject(
                    source=src_image[band],
                    destination=dst_image[band],
                    src_transform=src_transform,
                    src_crs=src_crs,
                    dst_transform=dst_transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.bilinear
                )
        else:
            dst_image = np.zeros((height, width), dtype=src_image.dtype)
            reproject(
                source=src_image,
                destination=dst_image,
                src_transform=src_transform,
                src_crs=src_crs,
                dst_transform=dst_transform,
                dst_crs=dst_crs,
                resampling=Resampling.bilinear
            )
        
        logger.info(f"Reprojected image from {src_crs} to {dst_crs}")
        return dst_image, dst_transform
    
    def clip_to_aoi(self, 
                   image: np.ndarray,
                   transform: rasterio.Affine,
                   aoi_bounds: Tuple[float, float, float, float],
                   crs: CRS) -> Tuple[np.ndarray, rasterio.Affine]:
        """
        Clip image to area of interest
        
        Args:
            image: Input image
            transform: Image transform
            aoi_bounds: (minx, miny, maxx, maxy) in image CRS
            crs: Image CRS
            
        Returns:
            tuple: (clipped_image, new_transform)
        """
        # Calculate window for clipping
        window = from_bounds(*aoi_bounds, transform)
        
        # Clip image
        if image.ndim == 3:
            clipped = image[:, 
                          int(window.row_off):int(window.row_off + window.height),
                          int(window.col_off):int(window.col_off + window.width)]
        else:
            clipped = image[int(window.row_off):int(window.row_off + window.height),
                          int(window.col_off):int(window.col_off + window.width)]
        
        # Calculate new transform
        new_transform = rasterio.windows.transform(window, transform)
        
        logger.info(f"Clipped image to AOI: {clipped.shape}")
        return clipped, new_transform
    
    def create_madagascar_grid(self, 
                             cell_size_km: float = 10.0,
                             buffer_km: float = 0.0) -> gpd.GeoDataFrame:
        """
        Create a grid covering Madagascar for systematic analysis
        
        Args:
            cell_size_km: Size of grid cells in kilometers
            buffer_km: Buffer around Madagascar bounds
            
        Returns:
            GeoDataFrame with grid cells
        """
        # Convert to projected coordinates for accurate distance calculation
        madagascar_geom = box(
            self.madagascar_bounds['west'] - buffer_km/111.0,  # Rough km to degree conversion
            self.madagascar_bounds['south'] - buffer_km/111.0,
            self.madagascar_bounds['east'] + buffer_km/111.0,
            self.madagascar_bounds['north'] + buffer_km/111.0
        )
        
        # Create grid
        bounds = madagascar_geom.bounds
        cell_size_deg = cell_size_km / 111.0  # Rough conversion
        
        x_coords = np.arange(bounds[0], bounds[2], cell_size_deg)
        y_coords = np.arange(bounds[1], bounds[3], cell_size_deg)
        
        grid_cells = []
        for i, x in enumerate(x_coords[:-1]):
            for j, y in enumerate(y_coords[:-1]):
                cell = box(x, y, x_coords[i+1], y_coords[j+1])
                grid_cells.append({
                    'geometry': cell,
                    'grid_id': f"{i:03d}_{j:03d}",
                    'center_lon': cell.centroid.x,
                    'center_lat': cell.centroid.y
                })
        
        grid_gdf = gpd.GeoDataFrame(grid_cells, crs='EPSG:4326')
        logger.info(f"Created Madagascar grid with {len(grid_gdf)} cells")
        
        return grid_gdf
    
    def get_sentinel2_bands_for_date(self, 
                                   lat: float, 
                                   lon: float,
                                   date: datetime,
                                   days_tolerance: int = 10) -> Dict[str, str]:
        """
        Get Sentinel-2 band URLs for given location and date
        (This is a placeholder - would integrate with actual data providers)
        
        Args:
            lat: Latitude
            lon: Longitude  
            date: Target date
            days_tolerance: Days tolerance for finding images
            
        Returns:
            Dictionary mapping band names to URLs/paths
        """
        # This would integrate with services like:
        # - Microsoft Planetary Computer
        # - Google Earth Engine
        # - AWS Open Data
        # - USGS EarthExplorer
        
        # For now, return placeholder structure
        band_urls = {}
        for band_name, band_num in self.band_configs['sentinel2'].items():
            # Placeholder URL structure
            band_urls[band_name] = f"s2://sentinel-2/{date.strftime('%Y/%m/%d')}/{lat}_{lon}/B{band_num:02d}.tif"
        
        logger.info(f"Generated Sentinel-2 band URLs for {lat}, {lon} on {date}")
        return band_urls
    
    def calculate_cloud_coverage(self, image: np.ndarray, cloud_mask: np.ndarray) -> float:
        """Calculate percentage of cloud coverage in image"""
        total_pixels = cloud_mask.size
        cloud_pixels = np.sum(cloud_mask)
        cloud_percentage = (cloud_pixels / total_pixels) * 100
        
        logger.info(f"Cloud coverage: {cloud_percentage:.2f}%")
        return cloud_percentage
    
    def find_clear_images(self, 
                         image_list: List[Dict], 
                         max_cloud_cover: float = 20.0) -> List[Dict]:
        """
        Filter images by cloud coverage threshold
        
        Args:
            image_list: List of image metadata dictionaries
            max_cloud_cover: Maximum acceptable cloud coverage percentage
            
        Returns:
            Filtered list of clear images
        """
        clear_images = []
        for img_info in image_list:
            if img_info.get('cloud_cover', 0) <= max_cloud_cover:
                clear_images.append(img_info)
        
        logger.info(f"Found {len(clear_images)} clear images from {len(image_list)} total")
        return clear_images
    
    def create_time_series_composite(self, 
                                   images: List[np.ndarray],
                                   method: str = 'median') -> np.ndarray:
        """
        Create composite image from time series
        
        Args:
            images: List of image arrays
            method: Compositing method ('median', 'mean', 'max', 'min')
            
        Returns:
            Composite image
        """
        if not images:
            raise ValueError("No images provided for compositing")
        
        # Stack images
        image_stack = np.stack(images, axis=0)
        
        # Apply compositing method
        if method == 'median':
            composite = np.median(image_stack, axis=0)
        elif method == 'mean':
            composite = np.mean(image_stack, axis=0)
        elif method == 'max':
            composite = np.max(image_stack, axis=0)
        elif method == 'min':
            composite = np.min(image_stack, axis=0)
        else:
            raise ValueError(f"Unknown compositing method: {method}")
        
        logger.info(f"Created {method} composite from {len(images)} images")
        return composite.astype(images[0].dtype)
    
    def extract_pixel_time_series(self, 
                                images: List[np.ndarray],
                                coordinates: List[Tuple[float, float]],
                                transforms: List[rasterio.Affine]) -> Dict[Tuple[float, float], np.ndarray]:
        """
        Extract pixel time series for specific coordinates
        
        Args:
            images: List of image arrays
            coordinates: List of (lon, lat) coordinates
            transforms: List of transforms for each image
            
        Returns:
            Dictionary mapping coordinates to time series arrays
        """
        time_series = {}
        
        for coord in coordinates:
            lon, lat = coord
            pixel_values = []
            
            for image, transform in zip(images, transforms):
                # Convert geographic coordinates to pixel coordinates
                col, row = ~transform * (lon, lat)
                col, row = int(col), int(row)
                
                # Extract pixel value (handle bounds checking)
                if (0 <= row < image.shape[-2] and 0 <= col < image.shape[-1]):
                    if image.ndim == 3:
                        pixel_value = image[:, row, col]
                    else:
                        pixel_value = image[row, col]
                    pixel_values.append(pixel_value)
                else:
                    # Out of bounds - use NaN
                    if image.ndim == 3:
                        pixel_values.append(np.full(image.shape[0], np.nan))
                    else:
                        pixel_values.append(np.nan)
            
            time_series[coord] = np.array(pixel_values)
        
        logger.info(f"Extracted time series for {len(coordinates)} coordinates")
        return time_series
    
    def convert_bounds_to_crs(self, 
                            bounds: Tuple[float, float, float, float],
                            src_crs: Union[str, CRS],
                            dst_crs: Union[str, CRS]) -> Tuple[float, float, float, float]:
        """Convert bounding box between coordinate systems"""
        if isinstance(src_crs, str):
            src_crs = CRS.from_string(src_crs)
        if isinstance(dst_crs, str):
            dst_crs = CRS.from_string(dst_crs)
        
        return transform_bounds(src_crs, dst_crs, *bounds)
    
    def get_madagascar_protected_areas(self) -> gpd.GeoDataFrame:
        """
        Get Madagascar protected areas boundaries
        (This would integrate with WDPA or other datasets)
        
        Returns:
            GeoDataFrame with protected areas
        """
        # Placeholder for protected areas - would load from actual dataset
        protected_areas = [
            {'name': 'Andasibe-Mantadia National Park', 'type': 'National Park',
             'geometry': box(48.3, -18.9, 48.6, -18.7)},
            {'name': 'Isalo National Park', 'type': 'National Park',
             'geometry': box(45.3, -22.7, 45.7, -22.4)},
            {'name': 'Ankarafantsika National Park', 'type': 'National Park', 
             'geometry': box(46.7, -16.3, 47.2, -15.9)},
        ]
        
        return gpd.GeoDataFrame(protected_areas, crs='EPSG:4326')

# Convenience functions
def madagascar_bounds_check(lon: float, lat: float, buffer_deg: float = 0.1) -> bool:
    """Check if coordinates are within Madagascar bounds (with buffer)"""
    utils = SatelliteUtils()
    bounds = utils.madagascar_bounds
    return (bounds['west'] - buffer_deg <= lon <= bounds['east'] + buffer_deg and
            bounds['south'] - buffer_deg <= lat <= bounds['north'] + buffer_deg)

def get_madagascar_utm_zone(lon: float, lat: float) -> Tuple[int, CRS]:
    """Get appropriate UTM zone for Madagascar coordinates"""
    utils = SatelliteUtils()
    return utils.geographic_to_utm(lon, lat)
