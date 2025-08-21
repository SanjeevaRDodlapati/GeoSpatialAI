# 🦎 Project 5: Species Occurrence Mapping and Environmental Context

## 🎯 Project Overview

This project explores **species occurrence patterns** using GBIF biodiversity data, focusing on Madagascar's endemic fauna. We analyze occurrence records, environmental relationships, and spatial patterns to understand species distributions and habitat preferences.

### 🔍 Key Objectives

1. **Acquire and process GBIF species occurrence data** for Madagascar endemic species
2. **Map occurrence patterns** and identify biodiversity hotspots
3. **Extract environmental context** (elevation, climate, land cover) at occurrence locations
4. **Analyze species-environment relationships** and habitat preferences
5. **Assess data quality** and sampling bias in occurrence records

## 🗺️ Study Area: Madagascar

Building on **Project 4's land cover analysis**, this project focuses on Madagascar's unique biodiversity, exploring how endemic species relate to the diverse landscapes we previously analyzed.

**Target Species:**
- **Lemur catta** (Ring-tailed Lemur) - Endangered primate
- **Propithecus verreauxi** (Verreaux's Sifaka) - Critically endangered primate
- **Brookesia micra** (Nosy Hara Leaf Chameleon) - Near threatened reptile
- **Furcifer pardalis** (Panther Chameleon) - Least concern reptile
- **Coua caerulea** (Blue Coua) - Endemic bird
- **Vanga curvirostris** (Hook-billed Vanga) - Endemic bird

## 📊 Data Sources

### Primary Data
- **GBIF (Global Biodiversity Information Facility)**: Species occurrence records
  - API: https://api.gbif.org/v1/occurrence/search
  - Quality filters: hasCoordinate=true, hasGeospatialIssue=false
  - Geographic filter: Madagascar bounds (43.2°W to 50.5°E, -25.6°S to -11.9°N)
  - Temporal filter: 2000-2024 (recent data)

### Environmental Context Data
- **Elevation**: SRTM/MERIT DEM data
- **Climate**: WorldClim bioclimatic variables (optional)
- **Land Cover**: ESA WorldCover 2020 (from Project 4)
- **Administrative Boundaries**: Natural Earth country boundaries

## 🛠️ Methodology

### Phase 1: Data Acquisition
1. **GBIF API Integration**: Automated species occurrence download
2. **Data Caching**: Local storage to avoid repeated API calls
3. **Quality Filtering**: Coordinate validation and uncertainty assessment
4. **Synthetic Data Fallback**: Realistic demonstration data when API unavailable

### Phase 2: Data Processing
1. **Coordinate Validation**: Geographic bounds checking and outlier detection
2. **Temporal Analysis**: Occurrence patterns by year and season
3. **Data Quality Assessment**: Uncertainty analysis and bias evaluation
4. **Geometric Processing**: Conversion to equal-area projections for analysis

### Phase 3: Spatial Analysis
1. **Occurrence Mapping**: Point pattern visualization and density analysis
2. **Hotspot Identification**: Kernel density estimation and clustering
3. **Environmental Sampling**: Raster value extraction at occurrence points
4. **Habitat Analysis**: Species-environment relationship modeling

### Phase 4: Integration Analysis
1. **Land Cover Integration**: Relate occurrences to Project 4 land cover analysis
2. **Multi-species Comparison**: Comparative habitat preferences
3. **Conservation Assessment**: Species richness and threat analysis

## 📁 Project Structure

```
project_5_species_mapping/
├── data/
│   ├── raw/                    # GBIF downloads and cache files
│   │   ├── Lemur_catta_occurrences.json
│   │   ├── Propithecus_verreauxi_occurrences.json
│   │   └── [other species files]
│   └── processed/              # Cleaned occurrence data
│       ├── lemur_catta_occurrences.geojson
│       ├── propithecus_verreauxi_occurrences.geojson
│       └── [other processed files]
├── notebooks/
│   └── 06_species_occurrence_mapping.ipynb  # Main analysis notebook
├── outputs/
│   ├── figures/                # Maps and visualizations
│   │   ├── madagascar_species_overview.png
│   │   ├── occurrence_density_maps.png
│   │   ├── environmental_relationships.png
│   │   └── habitat_preferences_analysis.png
│   └── tables/                 # Summary statistics and reports
│       ├── species_download_summary.csv
│       ├── environmental_summary.csv
│       └── habitat_analysis_results.csv
└── README.md
```

## 🔧 Technical Implementation

### Key Libraries Used
- **GeoPandas**: Spatial data processing and analysis
- **Rasterio/Rioxarray**: Environmental raster data handling
- **Requests**: GBIF API integration
- **SciPy**: Statistical analysis and kernel density estimation
- **Scikit-learn**: Clustering and pattern analysis
- **Matplotlib/Seaborn**: Visualization and mapping

### Memory Optimization (Building on Project 4)
- **Efficient data types**: uint8 for categorical data, float32 for coordinates
- **Progressive loading**: Process species data incrementally
- **Caching strategy**: Local storage of API responses
- **Optimized visualizations**: Lower DPI and simplified rendering

### CRS Management
- **Input CRS**: EPSG:4326 (WGS84) for GBIF data
- **Analysis CRS**: EPSG:32738 (UTM Zone 38S) for Madagascar-specific analysis
- **Global CRS**: EPSG:6933 (World Cylindrical Equal Area) for global comparisons

## 📈 Expected Outputs

### Maps and Visualizations
1. **Species Occurrence Overview**: Multi-species occurrence map with Madagascar context
2. **Density Hotspot Maps**: Kernel density analysis showing biodiversity hotspots
3. **Environmental Relationship Plots**: Elevation and climate preference analysis
4. **Habitat Preference Charts**: Species-land cover relationship analysis
5. **Data Quality Assessment**: Coordinate uncertainty and temporal coverage maps

### Tables and Statistics
1. **Species Summary Table**: Record counts, date ranges, data quality metrics
2. **Environmental Summary**: Mean elevation, climate variables by species
3. **Habitat Analysis**: Land cover preferences and significance tests
4. **Conservation Assessment**: Species richness patterns and threat analysis

## 🎯 Learning Outcomes

### Technical Skills
- **Biodiversity Data APIs**: GBIF integration and data acquisition
- **Point Pattern Analysis**: Occurrence mapping and density analysis
- **Environmental Data Integration**: Multi-layer raster analysis
- **Data Quality Assessment**: Coordinate validation and bias detection

### Domain Knowledge
- **Madagascar Biodiversity**: Endemic species and conservation status
- **Species Distribution Modeling**: Environmental preferences and habitat suitability
- **Conservation Biology**: Threat assessment and habitat requirements
- **Biogeography**: Species-environment relationships and patterns

## 🚨 Data Quality Considerations

### GBIF Data Limitations
- **Sampling Bias**: Uneven geographic and temporal coverage
- **Taxonomic Bias**: Some species better documented than others
- **Coordinate Uncertainty**: Variable precision in location data
- **Identification Errors**: Potential misidentifications in citizen science data

### Quality Control Measures
- **Coordinate Validation**: Geographic bounds and precision checking
- **Outlier Detection**: Identify and flag suspicious records
- **Uncertainty Mapping**: Visualize coordinate uncertainty patterns
- **Temporal Analysis**: Assess sampling effort changes over time

## 🔗 Integration with Other Projects

### Project 4 Connection (Land Cover Analysis)
- **Shared Study Area**: Madagascar focus for regional expertise
- **Land Cover Context**: Relate species occurrences to habitat types
- **Conservation Assessment**: Species-habitat relationships and threats

### Future Project Connections
- **Project 6 (Hazard Exposure)**: Species vulnerability to environmental threats
- **Phase 2 (ML Applications)**: Species distribution modeling and prediction

## 🌍 Conservation Implications

### Biodiversity Hotspots
- **Protected Area Assessment**: Coverage of high-diversity areas
- **Gap Analysis**: Underprotected habitats and species
- **Priority Conservation Areas**: Data-driven conservation planning

### Threat Assessment
- **Habitat Loss Risk**: Vulnerable species and habitat requirements
- **Climate Change Vulnerability**: Elevation and climate preferences
- **Human Impact Assessment**: Species in human-modified landscapes

## 📚 References and Data Citations

### Data Sources
- GBIF.org (2024). GBIF Occurrence Download. https://doi.org/10.15468/dl.[dataset-id]
- ESA WorldCover 2020 v100 (from Project 4 analysis)
- Natural Earth Administrative Boundaries v5.1.2

### Scientific References
- Goodman, S.M. & Benstead, J.P. (2005). Updated estimates of biotic diversity and endemism for Madagascar. Oryx, 39(1), 73-77.
- Myers, N. et al. (2000). Biodiversity hotspots for conservation priorities. Nature, 403, 853-858.
- Ganzhorn, J.U. et al. (2001). The biodiversity of Madagascar: one of the world's hottest hotspots on its way out. Oryx, 35(4), 346-348.

## ⚠️ Known Limitations

### Data Availability
- **Real GBIF Data**: May require API registration for large downloads
- **Synthetic Data**: Used for demonstration when API unavailable
- **Environmental Data**: Simplified elevation/climate variables

### Analysis Scope
- **Species Selection**: Limited to well-documented endemic species
- **Temporal Coverage**: Recent data (2000-2024) may miss historical patterns
- **Environmental Variables**: Basic elevation and climate only

### Technical Constraints
- **API Rate Limits**: GBIF requests limited to prevent server overload
- **Memory Optimization**: Simplified analysis for educational purposes
- **Coordinate Precision**: Variable accuracy in occurrence locations

---

**Next Steps**: After completing this analysis, proceed to Project 6 (Hazard Exposure Analysis) to complete Phase 1, then transition to Phase 2 (Machine Learning Applications) for advanced species distribution modeling.
