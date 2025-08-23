"""
Visualization utilities for geospatial model implementations
Provides plotting, mapping, and results visualization functions
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import ListedColormap, Normalize
import seaborn as sns
import folium
from folium import plugins
import geopandas as gpd
import rasterio.plot
from rasterio.windows import Window
import contextily as ctx
from pathlib import Path
import logging
from typing import Tuple, List, Optional, Dict, Union, Any
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class VisualizationUtils:
    """Utilities for visualizing geospatial data and model results"""
    
    def __init__(self, style: str = 'seaborn-v0_8', figsize: Tuple[int, int] = (12, 8)):
        """
        Initialize visualization utilities
        
        Args:
            style: Matplotlib style
            figsize: Default figure size
        """
        plt.style.use(style)
        self.default_figsize = figsize
        self.madagascar_center = (-19.0, 46.8)
        
        # Color palettes for different visualizations
        self.palettes = {
            'vegetation': ['#8B4513', '#CD853F', '#FFFF00', '#ADFF2F', '#00FF00', '#006400'],
            'water': ['#000080', '#0000FF', '#1E90FF', '#87CEEB', '#B0E0E6'],
            'elevation': ['#0000FF', '#00FFFF', '#FFFF00', '#FFA500', '#FF0000'],
            'change': ['#FF0000', '#FFFF00', '#00FF00'],
            'species': sns.color_palette("husl", 10)
        }
    
    def plot_satellite_image(self, 
                           image: np.ndarray,
                           bands: Optional[List[int]] = None,
                           title: str = "Satellite Image",
                           enhance: bool = True,
                           figsize: Optional[Tuple[int, int]] = None) -> plt.Figure:
        """
        Plot satellite image with optional band combination
        
        Args:
            image: Image array (bands, height, width) or (height, width, bands)
            bands: Band indices for RGB display [R, G, B]
            title: Plot title
            enhance: Whether to enhance contrast
            figsize: Figure size
            
        Returns:
            matplotlib Figure
        """
        figsize = figsize or self.default_figsize
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        
        # Handle different image dimensions
        if image.ndim == 3:
            if image.shape[0] <= 13:  # Channels first
                display_image = np.transpose(image, (1, 2, 0))
            else:  # Channels last
                display_image = image.copy()
        else:
            display_image = image
        
        # Select bands for RGB display
        if bands and display_image.ndim == 3:
            if len(bands) == 3 and max(bands) < display_image.shape[2]:
                display_image = display_image[:, :, bands]
            else:
                logger.warning(f"Invalid bands {bands}, using first 3 channels")
                display_image = display_image[:, :, :3]
        elif display_image.ndim == 3 and display_image.shape[2] > 3:
            display_image = display_image[:, :, :3]
        
        # Enhance contrast if requested
        if enhance:
            display_image = self._enhance_image(display_image)
        
        # Plot image
        if display_image.ndim == 2:
            im = ax.imshow(display_image, cmap='gray')
            plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        else:
            ax.imshow(display_image)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Pixel X')
        ax.set_ylabel('Pixel Y')
        
        plt.tight_layout()
        return fig
    
    def plot_vegetation_index(self, 
                            vi_array: np.ndarray,
                            vi_name: str = "NDVI",
                            vmin: float = -1.0,
                            vmax: float = 1.0,
                            figsize: Optional[Tuple[int, int]] = None) -> plt.Figure:
        """
        Plot vegetation index with appropriate colormap
        
        Args:
            vi_array: Vegetation index array
            vi_name: Name of vegetation index
            vmin: Minimum value for colormap
            vmax: Maximum value for colormap
            figsize: Figure size
            
        Returns:
            matplotlib Figure
        """
        figsize = figsize or self.default_figsize
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        
        # Use vegetation colormap
        cmap = ListedColormap(self.palettes['vegetation'])
        
        im = ax.imshow(vi_array, cmap=cmap, vmin=vmin, vmax=vmax)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label(vi_name, rotation=270, labelpad=20, fontsize=12)
        
        ax.set_title(f"{vi_name} Analysis", fontsize=14, fontweight='bold')
        ax.set_xlabel('Pixel X')
        ax.set_ylabel('Pixel Y')
        
        plt.tight_layout()
        return fig
    
    def plot_change_detection(self, 
                            before: np.ndarray,
                            after: np.ndarray,
                            change_map: np.ndarray,
                            titles: List[str] = None,
                            figsize: Optional[Tuple[int, int]] = None) -> plt.Figure:
        """
        Plot before/after images and change detection results
        
        Args:
            before: Before image
            after: After image  
            change_map: Change detection result
            titles: List of subplot titles
            figsize: Figure size
            
        Returns:
            matplotlib Figure
        """
        figsize = figsize or (15, 5)
        fig, axes = plt.subplots(1, 3, figsize=figsize)
        
        if titles is None:
            titles = ['Before', 'After', 'Change Detection']
        
        # Plot before image
        if before.ndim == 3:
            before_display = self._prepare_for_display(before)
            axes[0].imshow(before_display)
        else:
            axes[0].imshow(before, cmap='gray')
        axes[0].set_title(titles[0], fontsize=12, fontweight='bold')
        axes[0].axis('off')
        
        # Plot after image
        if after.ndim == 3:
            after_display = self._prepare_for_display(after)
            axes[1].imshow(after_display)
        else:
            axes[1].imshow(after, cmap='gray')
        axes[1].set_title(titles[1], fontsize=12, fontweight='bold')
        axes[1].axis('off')
        
        # Plot change map
        change_cmap = ListedColormap(['green', 'yellow', 'red'])  # No change, minor change, major change
        im = axes[2].imshow(change_map, cmap=change_cmap)
        axes[2].set_title(titles[2], fontsize=12, fontweight='bold')
        axes[2].axis('off')
        
        # Add colorbar for change map
        cbar = plt.colorbar(im, ax=axes[2], fraction=0.046, pad=0.04)
        cbar.set_label('Change Intensity', rotation=270, labelpad=20)
        
        plt.tight_layout()
        return fig
    
    def plot_species_detections(self, 
                              image: np.ndarray,
                              detections: List[Dict],
                              confidence_threshold: float = 0.5,
                              figsize: Optional[Tuple[int, int]] = None) -> plt.Figure:
        """
        Plot species detection results on image
        
        Args:
            image: Background image
            detections: List of detection dictionaries with bbox, class, confidence
            confidence_threshold: Minimum confidence to display
            figsize: Figure size
            
        Returns:
            matplotlib Figure
        """
        figsize = figsize or self.default_figsize
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        
        # Display background image
        if image.ndim == 3:
            display_image = self._prepare_for_display(image)
            ax.imshow(display_image)
        else:
            ax.imshow(image, cmap='gray')
        
        # Plot detections
        colors = plt.cm.Set3(np.linspace(0, 1, len(set([d['class'] for d in detections]))))
        class_colors = {cls: color for cls, color in 
                       zip(set([d['class'] for d in detections]), colors)}
        
        for detection in detections:
            if detection['confidence'] >= confidence_threshold:
                bbox = detection['bbox']  # Assuming [x, y, width, height]
                class_name = detection['class']
                confidence = detection['confidence']
                
                # Create rectangle
                rect = patches.Rectangle(
                    (bbox[0], bbox[1]), bbox[2], bbox[3],
                    linewidth=2, edgecolor=class_colors[class_name],
                    facecolor='none'
                )
                ax.add_patch(rect)
                
                # Add label
                ax.text(bbox[0], bbox[1] - 5, 
                       f"{class_name}: {confidence:.2f}",
                       fontsize=10, color=class_colors[class_name],
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.7))
        
        ax.set_title("Species Detection Results", fontsize=14, fontweight='bold')
        ax.set_xlabel('Pixel X')
        ax.set_ylabel('Pixel Y')
        
        plt.tight_layout()
        return fig
    
    def create_interactive_map(self, 
                             center: Optional[Tuple[float, float]] = None,
                             zoom: int = 6,
                             tiles: str = 'OpenStreetMap') -> folium.Map:
        """
        Create interactive map centered on Madagascar
        
        Args:
            center: Map center (lat, lon)
            zoom: Zoom level
            tiles: Tile provider
            
        Returns:
            folium Map
        """
        center = center or self.madagascar_center
        
        # Create base map
        m = folium.Map(
            location=center,
            zoom_start=zoom,
            tiles=tiles,
            control_scale=True
        )
        
        # Add fullscreen button
        plugins.Fullscreen().add_to(m)
        
        # Add mouse position
        plugins.MousePosition().add_to(m)
        
        return m
    
    def add_satellite_overlay(self, 
                            folium_map: folium.Map,
                            image: np.ndarray,
                            bounds: Tuple[float, float, float, float],
                            name: str = "Satellite Image",
                            opacity: float = 0.8) -> folium.Map:
        """
        Add satellite image overlay to folium map
        
        Args:
            folium_map: Base folium map
            image: Image array to overlay
            bounds: Image bounds (south, north, west, east)
            name: Layer name
            opacity: Layer opacity
            
        Returns:
            Updated folium map
        """
        # Convert image to RGB if needed
        if image.ndim == 3:
            if image.shape[0] <= 13:  # Channels first
                display_image = np.transpose(image, (1, 2, 0))
            else:
                display_image = image
            
            if display_image.shape[2] > 3:
                display_image = display_image[:, :, :3]
        else:
            display_image = image
        
        # Normalize image
        display_image = self._enhance_image(display_image)
        
        # Add to map (this is simplified - real implementation would need proper georeferencing)
        folium.raster_layers.ImageOverlay(
            image=display_image,
            bounds=[[bounds[0], bounds[2]], [bounds[1], bounds[3]]],
            opacity=opacity,
            name=name,
            overlay=True,
            control=True
        ).add_to(folium_map)
        
        return folium_map
    
    def plot_time_series(self, 
                        dates: List,
                        values: np.ndarray,
                        labels: Optional[List[str]] = None,
                        title: str = "Time Series Analysis",
                        ylabel: str = "Value",
                        figsize: Optional[Tuple[int, int]] = None) -> plt.Figure:
        """
        Plot time series data
        
        Args:
            dates: List of dates
            values: Array of values (time_steps, variables)
            labels: Variable labels
            title: Plot title
            ylabel: Y-axis label
            figsize: Figure size
            
        Returns:
            matplotlib Figure
        """
        figsize = figsize or self.default_figsize
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        
        if values.ndim == 1:
            ax.plot(dates, values, linewidth=2, marker='o')
        else:
            for i in range(values.shape[1]):
                label = labels[i] if labels and i < len(labels) else f"Variable {i+1}"
                ax.plot(dates, values[:, i], linewidth=2, marker='o', label=label)
            ax.legend()
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
    
    def plot_model_performance(self, 
                             metrics: Dict[str, float],
                             title: str = "Model Performance",
                             figsize: Optional[Tuple[int, int]] = None) -> plt.Figure:
        """
        Plot model performance metrics
        
        Args:
            metrics: Dictionary of metric names and values
            title: Plot title
            figsize: Figure size
            
        Returns:
            matplotlib Figure
        """
        figsize = figsize or (10, 6)
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        
        metric_names = list(metrics.keys())
        metric_values = list(metrics.values())
        
        bars = ax.bar(metric_names, metric_values, 
                     color=sns.color_palette("viridis", len(metric_names)))
        
        # Add value labels on bars
        for bar, value in zip(bars, metric_values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel('Metric Value')
        ax.set_ylim(0, max(metric_values) * 1.2)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
    
    def _enhance_image(self, image: np.ndarray, percentile: float = 2.0) -> np.ndarray:
        """Enhance image contrast using percentile stretching"""
        if image.dtype != np.uint8:
            # Apply percentile stretching
            p_low, p_high = np.percentile(image, [percentile, 100 - percentile])
            image_stretched = np.clip((image - p_low) / (p_high - p_low), 0, 1)
            return (image_stretched * 255).astype(np.uint8)
        return image
    
    def _prepare_for_display(self, image: np.ndarray) -> np.ndarray:
        """Prepare multi-band image for display"""
        if image.shape[0] <= 13:  # Channels first
            display_image = np.transpose(image, (1, 2, 0))
        else:
            display_image = image
        
        if display_image.shape[2] > 3:
            display_image = display_image[:, :, :3]
        
        return self._enhance_image(display_image)
    
    def save_figure(self, fig: plt.Figure, filename: str, dpi: int = 300, 
                   bbox_inches: str = 'tight') -> Path:
        """Save figure to file"""
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        fig.savefig(output_path, dpi=dpi, bbox_inches=bbox_inches)
        logger.info(f"Saved figure to {output_path}")
        
        return output_path

# Convenience functions
def quick_plot_satellite(image: np.ndarray, title: str = "Satellite Image") -> plt.Figure:
    """Quick function to plot satellite image"""
    viz = VisualizationUtils()
    return viz.plot_satellite_image(image, title=title)

def quick_plot_detections(image: np.ndarray, detections: List[Dict]) -> plt.Figure:
    """Quick function to plot detection results"""
    viz = VisualizationUtils()
    return viz.plot_species_detections(image, detections)
