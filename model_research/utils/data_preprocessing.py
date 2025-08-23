"""
Core data preprocessing utilities for geospatial models
Provides common functionality for loading, cleaning, and formatting data
across different model implementations.
"""

import numpy as np
import pandas as pd
import rasterio
from rasterio.windows import Window
from rasterio.warp import calculate_default_transform, reproject, Resampling
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging
from typing import Tuple, List, Optional, Union, Dict, Any
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataPreprocessor:
    """Core data preprocessing utilities for geospatial analysis"""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize data preprocessor
        
        Args:
            cache_dir: Directory for caching preprocessed data
        """
        self.cache_dir = Path(cache_dir) if cache_dir else Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
        
    def load_satellite_image(self, 
                           image_path: Union[str, Path], 
                           bands: Optional[List[int]] = None,
                           window: Optional[Window] = None,
                           normalize: bool = True) -> Tuple[np.ndarray, Dict]:
        """
        Load satellite imagery with optional band selection and windowing
        
        Args:
            image_path: Path to satellite image
            bands: List of band indices to load (1-indexed)
            window: Rasterio window for spatial subsetting
            normalize: Whether to normalize pixel values to [0, 1]
            
        Returns:
            tuple: (image_array, metadata)
        """
        try:
            with rasterio.open(image_path) as src:
                # Load specified bands or all bands
                if bands:
                    image = src.read(bands, window=window)
                else:
                    image = src.read(window=window)
                
                # Get metadata
                metadata = {
                    'crs': src.crs,
                    'transform': src.transform,
                    'bounds': src.bounds,
                    'shape': image.shape,
                    'dtype': image.dtype,
                    'nodata': src.nodata
                }
                
                # Normalize if requested
                if normalize and image.dtype != np.float32:
                    image = image.astype(np.float32)
                    # Handle different satellite data ranges
                    if image.max() > 1.0:
                        if image.max() <= 255:  # 8-bit data
                            image = image / 255.0
                        elif image.max() <= 65535:  # 16-bit data
                            image = image / 10000.0  # Common for Sentinel-2
                        else:
                            image = image / image.max()
                
                logger.info(f"Loaded satellite image: {image.shape} from {image_path}")
                return image, metadata
                
        except Exception as e:
            logger.error(f"Error loading satellite image {image_path}: {e}")
            raise
    
    def load_time_series_images(self, 
                              image_paths: List[Union[str, Path]], 
                              dates: List[datetime],
                              bands: Optional[List[int]] = None,
                              align_images: bool = True) -> Tuple[np.ndarray, List[Dict]]:
        """
        Load a time series of satellite images
        
        Args:
            image_paths: List of paths to satellite images
            dates: List of acquisition dates
            bands: List of band indices to load
            align_images: Whether to align images to same grid
            
        Returns:
            tuple: (time_series_array, metadata_list)
        """
        images = []
        metadata_list = []
        
        for i, (path, date) in enumerate(zip(image_paths, dates)):
            try:
                image, metadata = self.load_satellite_image(path, bands=bands)
                metadata['acquisition_date'] = date
                images.append(image)
                metadata_list.append(metadata)
                
            except Exception as e:
                logger.warning(f"Skipping image {path}: {e}")
                continue
        
        if not images:
            raise ValueError("No valid images loaded")
        
        # Stack images into time series
        time_series = np.stack(images, axis=0)
        logger.info(f"Loaded time series: {time_series.shape}")
        
        return time_series, metadata_list
    
    def preprocess_for_model(self, 
                           image: np.ndarray, 
                           target_size: Optional[Tuple[int, int]] = None,
                           model_type: str = "general") -> np.ndarray:
        """
        Preprocess image for specific model requirements
        
        Args:
            image: Input image array
            target_size: Target (height, width) for resizing
            model_type: Type of model (prithvi, satclip, yolo, etc.)
            
        Returns:
            Preprocessed image array
        """
        processed = image.copy()
        
        # Model-specific preprocessing
        if model_type.lower() == "prithvi":
            # PRITHVI expects specific input format
            if target_size:
                processed = self._resize_image(processed, target_size)
            # Ensure channel dimension is last
            if processed.ndim == 3 and processed.shape[0] < processed.shape[-1]:
                processed = np.transpose(processed, (1, 2, 0))
                
        elif model_type.lower() == "satclip":
            # SatCLIP expects 13-band input for Sentinel-2
            if target_size:
                processed = self._resize_image(processed, target_size)
            # Ensure channels first for PyTorch
            if processed.ndim == 3 and processed.shape[-1] < processed.shape[0]:
                processed = np.transpose(processed, (2, 0, 1))
                
        elif model_type.lower() == "yolo":
            # YOLO expects RGB format
            if processed.shape[0] > 3:  # Multi-spectral to RGB
                processed = processed[:3]  # Take first 3 bands
            if target_size:
                processed = self._resize_image(processed, target_size)
                
        logger.info(f"Preprocessed for {model_type}: {processed.shape}")
        return processed
    
    def _resize_image(self, image: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
        """Resize image to target size"""
        from skimage.transform import resize
        
        if image.ndim == 3:
            if image.shape[0] <= 13:  # Channels first
                resized = np.array([resize(band, target_size, preserve_range=True) 
                                 for band in image])
            else:  # Channels last
                resized = resize(image, target_size + (image.shape[2],), preserve_range=True)
        else:
            resized = resize(image, target_size, preserve_range=True)
            
        return resized.astype(image.dtype)
    
    def create_patches(self, 
                      image: np.ndarray, 
                      patch_size: Tuple[int, int],
                      overlap: float = 0.0) -> List[np.ndarray]:
        """
        Create patches from large image for processing
        
        Args:
            image: Input image
            patch_size: (height, width) of patches
            overlap: Fraction of overlap between patches
            
        Returns:
            List of image patches
        """
        patches = []
        h, w = image.shape[-2:]  # Assuming (..., H, W)
        patch_h, patch_w = patch_size
        
        step_h = int(patch_h * (1 - overlap))
        step_w = int(patch_w * (1 - overlap))
        
        for y in range(0, h - patch_h + 1, step_h):
            for x in range(0, w - patch_w + 1, step_w):
                if image.ndim == 3:
                    patch = image[:, y:y+patch_h, x:x+patch_w]
                else:
                    patch = image[y:y+patch_h, x:x+patch_w]
                patches.append(patch)
        
        logger.info(f"Created {len(patches)} patches of size {patch_size}")
        return patches
    
    def apply_cloud_mask(self, 
                        image: np.ndarray, 
                        cloud_mask: np.ndarray,
                        fill_value: float = 0.0) -> np.ndarray:
        """Apply cloud mask to satellite image"""
        masked_image = image.copy()
        if image.ndim == 3:
            for band in range(image.shape[0]):
                masked_image[band][cloud_mask] = fill_value
        else:
            masked_image[cloud_mask] = fill_value
            
        logger.info(f"Applied cloud mask, {cloud_mask.sum()} pixels masked")
        return masked_image
    
    def calculate_vegetation_indices(self, image: np.ndarray, band_map: Dict[str, int]) -> Dict[str, np.ndarray]:
        """
        Calculate common vegetation indices
        
        Args:
            image: Multi-spectral image
            band_map: Mapping of band names to indices (e.g., {'red': 3, 'nir': 7})
            
        Returns:
            Dictionary of vegetation indices
        """
        indices = {}
        
        # NDVI (Normalized Difference Vegetation Index)
        if 'red' in band_map and 'nir' in band_map:
            red = image[band_map['red']].astype(np.float32)
            nir = image[band_map['nir']].astype(np.float32)
            indices['ndvi'] = (nir - red) / (nir + red + 1e-8)
        
        # EVI (Enhanced Vegetation Index)
        if 'red' in band_map and 'nir' in band_map and 'blue' in band_map:
            red = image[band_map['red']].astype(np.float32)
            nir = image[band_map['nir']].astype(np.float32)
            blue = image[band_map['blue']].astype(np.float32)
            indices['evi'] = 2.5 * (nir - red) / (nir + 6 * red - 7.5 * blue + 1)
        
        # NDWI (Normalized Difference Water Index)
        if 'green' in band_map and 'nir' in band_map:
            green = image[band_map['green']].astype(np.float32)
            nir = image[band_map['nir']].astype(np.float32)
            indices['ndwi'] = (green - nir) / (green + nir + 1e-8)
        
        logger.info(f"Calculated {len(indices)} vegetation indices")
        return indices
    
    def save_processed_data(self, data: Any, filename: str) -> Path:
        """Save processed data to cache"""
        filepath = self.cache_dir / filename
        
        if isinstance(data, np.ndarray):
            np.save(filepath.with_suffix('.npy'), data)
        elif isinstance(data, pd.DataFrame):
            data.to_parquet(filepath.with_suffix('.parquet'))
        else:
            import pickle
            with open(filepath.with_suffix('.pkl'), 'wb') as f:
                pickle.dump(data, f)
        
        logger.info(f"Saved processed data to {filepath}")
        return filepath
    
    def load_processed_data(self, filename: str) -> Any:
        """Load processed data from cache"""
        possible_files = [
            self.cache_dir / f"{filename}.npy",
            self.cache_dir / f"{filename}.parquet", 
            self.cache_dir / f"{filename}.pkl"
        ]
        
        for filepath in possible_files:
            if filepath.exists():
                if filepath.suffix == '.npy':
                    return np.load(filepath)
                elif filepath.suffix == '.parquet':
                    return pd.read_parquet(filepath)
                elif filepath.suffix == '.pkl':
                    import pickle
                    with open(filepath, 'rb') as f:
                        return pickle.load(f)
        
        raise FileNotFoundError(f"No cached data found for {filename}")

# Convenience function for quick loading
def quick_load_satellite_image(image_path: Union[str, Path], 
                             bands: Optional[List[int]] = None,
                             normalize: bool = True) -> Tuple[np.ndarray, Dict]:
    """Quick function to load satellite image without creating preprocessor instance"""
    preprocessor = DataPreprocessor()
    return preprocessor.load_satellite_image(image_path, bands=bands, normalize=normalize)
