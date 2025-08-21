# Project 0: Projection & Cartography Practice

**Status**: 🚀 Ready to Start  
**Difficulty**: Beginner  
**Estimated Time**: 2-3 hours

## Objective

This warm-up project ensures your geospatial Python environment is properly configured and introduces fundamental concepts of coordinate reference systems (CRS), map projections, and cartographic design. You'll create world and regional maps with different projections while learning best practices for styling and exporting high-quality figures.

## Learning Goals

By completing this project, you will:
- Understand how to work with different coordinate reference systems (CRS)
- Learn to transform geospatial data between projections
- Practice basic cartographic design principles
- Master exporting publication-quality maps
- Establish a reproducible geospatial workflow

## Datasets

All data comes from **Natural Earth**, a public domain map dataset built for cartographers:

### Primary Datasets:
- **Admin 0 - Countries** (`ne_50m_admin_0_countries.shp`)
  - Source: https://www.naturalearthdata.com/downloads/50m-cultural-vectors/
  - Version: 5.1.1
  - Contains world country boundaries

- **Admin 1 - States/Provinces** (`ne_50m_admin_1_states_provinces.shp`)
  - Source: https://www.naturalearthdata.com/downloads/50m-cultural-vectors/
  - Version: 5.1.1
  - Contains sub-national administrative divisions

- **Populated Places** (`ne_50m_populated_places.shp`)
  - Source: https://www.naturalearthdata.com/downloads/50m-cultural-vectors/
  - Version: 5.1.2
  - Contains cities and towns worldwide

- **Physical Features** (Optional):
  - Ocean (`ne_50m_ocean.shp`)
  - Rivers and Lakes (`ne_50m_rivers_lake_centerlines.shp`)
  - Source: https://www.naturalearthdata.com/downloads/50m-physical-vectors/

## Key Libraries

```python
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib_scalebar.scalebar import ScaleBar
import cartopy.crs as ccrs
import cartopy.feature as cfeature
```

**Library Purposes:**
- **GeoPandas**: Read/write shapefiles, CRS transformations, spatial operations
- **Matplotlib**: Create and customize maps, add cartographic elements
- **Cartopy**: Advanced projection support and cartographic features
- **matplotlib-scalebar**: Add professional scale bars to maps

## Workflow Overview

### 1. Environment Setup & Data Download
- Install required packages
- Download Natural Earth datasets
- Verify data integrity

### 2. Basic World Map
- Load country boundaries
- Create a simple world map in Geographic CRS (EPSG:4326)
- Add basic styling (colors, borders)

### 3. Projection Comparison
Create the same map in 4 different projections:
- **Geographic (Plate Carrée)**: EPSG:4326 or `PlateCarree()`
- **Robinson**: `Robinson()` - Good all-purpose world projection
- **Equal Earth**: `EqualEarth()` - Equal-area, aesthetically pleasing
- **Mollweide**: `Mollweide()` - Equal-area, elliptical

### 4. Regional Focus Map
- Select a region (e.g., North America, Europe, your country)
- Use appropriate regional projection (e.g., Lambert Conformal Conic)
- Add populated places (cities) as points
- Include state/province boundaries

### 5. Cartographic Enhancement
- Add professional cartographic elements:
  - Scale bar
  - North arrow
  - Legend
  - Title and subtitle
  - Data source attribution
  - Coordinate grid (graticule)

### 6. Export and Documentation
- Export maps as high-resolution PNG (300 DPI)
- Save source code and document projection choices
- Create comparison figure showing all projections

## Quality Assurance Checklist

- [ ] **CRS Verification**: Confirm each map uses the intended projection
- [ ] **Geometry Validation**: Check for invalid geometries, fix if needed
- [ ] **Visual Inspection**: Ensure maps render correctly with no gaps or overlaps
- [ ] **Label Accuracy**: Verify coordinate labels match the projection
- [ ] **Export Quality**: Confirm exported images are high-resolution and crisp
- [ ] **Reproducibility**: Test that notebook runs from start to finish

## Expected Outputs

### Figures (`outputs/figures/`):
1. `world_map_geographic.png` - Basic world map in geographic coordinates
2. `world_map_robinson.png` - World map in Robinson projection
3. `world_map_equalearth.png` - World map in Equal Earth projection  
4. `world_map_mollweide.png` - World map in Mollweide projection
5. `regional_map_detailed.png` - Regional map with cities and enhanced cartography
6. `projection_comparison.png` - 2x2 panel comparing all four world projections

### Data (`data/processed/`):
- Cleaned and validated shapefiles (if any preprocessing was needed)

## Stretch Goals

If you finish early or want additional practice:

1. **Interactive Element**: Create a simple interactive map using Folium
2. **Thematic Mapping**: Color countries by population or GDP
3. **Multiple Regions**: Create detailed maps for 2-3 different regions
4. **Historical Context**: Download and compare different vintage years of Natural Earth data
5. **Graticule Customization**: Add custom coordinate grids with different intervals

## Common Pitfalls to Avoid

1. **Web Mercator for Analysis**: Don't use EPSG:3857 for area calculations
2. **Missing CRS**: Always explicitly set CRS when creating GeoDataFrames
3. **Projection Distortion**: Understand what each projection preserves (area, distance, angles)
4. **File Path Issues**: Use relative paths and maintain consistent folder structure
5. **Memory Issues**: For large datasets, consider spatial filtering before reprojection

## Resources and References

### Projection Guide:
- **Equal Area Projections**: Use for statistical mapping, density analysis
- **Conformal Projections**: Use when angles matter (navigation, local maps)
- **Compromise Projections**: Good for general reference maps

### Helpful Links:
- [EPSG.io](https://epsg.io/) - CRS reference database
- [Projection Wizard](http://projectionwizard.org/) - Choose appropriate projections
- [Natural Earth Documentation](https://www.naturalearthdata.com/about/)
- [GeoPandas CRS Tutorial](https://geopandas.org/en/stable/docs/user_guide/projections.html)

## Data Attribution

**Natural Earth Data**: Made with Natural Earth. Free vector and raster map data @ naturalearthdata.com.

## Next Steps

After completing this project, you'll be ready to tackle Project 1 (Census Mapping) with confidence in:
- CRS handling and transformations
- Basic cartographic design
- File organization and reproducible workflows
- Quality assurance procedures

---

**Estimated Completion Time**: 2-3 hours  
**Prerequisites**: Basic Python familiarity  
**Difficulty**: ⭐⭐☆☆☆
