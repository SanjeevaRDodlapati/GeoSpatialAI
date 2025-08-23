PHASE 1: GEOSPATIAL & GEOGRAPHIC DATA ANALYSIS — PROJECT DESCRIPTIONS

CONVENTIONS USED THROUGHOUT
• Target environment: Python with common geospatial libraries (e.g., GeoPandas, Shapely, PyProj, Rasterio, rioxarray, xarray, contextily, mapclassify, osmnx).
• Recommended folder layout per project:
project_name/
data/
raw/ (downloads as-is)
interim/ (cleaned, joined)
processed/ (analysis-ready)
notebooks/ (one main notebook; optional exploratory notebooks)
outputs/
figures/ (PNGs/SVGs for maps/plots)
tables/ (CSVs/PNGs for summary tables)
maps/ (geojson/shapefile/mbtiles if needed)
README.md (what, why, how; results highlights; data citations)
• CRS: Use an equal-area CRS for area/aggregation (e.g., EPSG:5070 for CONUS, EPSG:6933 global) and Web Mercator (EPSG:3857) only for basemap overlays.
• QA/QC checklist applied in each project:

Confirm CRS and units before any distance/area operation.

Validate geometry (fix self-intersections; drop empties).

Inspect joins (row counts pre/post; unmatched keys; spatial join sanity checks).

Record all filters and thresholds in the README with rationale.

Cite all datasets with version/date and URL.

PROJECT 1 — NEIGHBORHOOD SOCIO-DEMOGRAPHIC MAPPING (U.S. CENSUS)

Aim
Create small-area choropleth maps and summary tables of socio-demographic indicators to explore spatial inequality within a metro region, and practice tabular-to-geographic joins, classification schemes, and cartographic design.

Datasets (typical sources)
• TIGER/Line boundaries: Census tracts or block groups (https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)
• American Community Survey (ACS) 5-year tables (https://www.census.gov/data.html or API; indicators such as population, median household income, poverty rate, educational attainment, vehicle availability)

Geographic scope
Pick one U.S. metro area; use county FIPS to filter tracts/block groups.

Key libraries and why
• pandas + geopandas for join, clean, and map
• mapclassify for classification (quantiles, natural breaks, equal interval)
• contextily for base tiles when creating web-style backgrounds
• matplotlib for export-quality static figures

Workflow milestones

Data acquisition: download boundary shapefiles; pull ACS tables by GEOID.

Cleaning: standardize GEOID; handle missing/zero denominators; compute rates (e.g., percentage below poverty).

Joining: relational (GEOID), then CRS set to projected CRS appropriate to region.

Mapping: experiment with classification schemes; choose a perceptually even, color-blind-friendly palette; add scalebar, north arrow, legend, credits.

Small-multiple maps: create a panel for 3–4 indicators to compare spatial patterns.

Basic clustering (optional): compute Local Moran's I hot-/cold-spots of one indicator (only mapping result; defer formal spatial statistics to later).

Export: CSV summary per tract; PNG maps; write a short interpretive paragraph for each figure.

Quality concerns / pitfalls
• Margin of error in ACS (note limitations; avoid over-interpreting small-n geographies).
• MAUP: results sensitive to the choice of census unit.
• Classification bias: compare quantitative patterns across methods before selecting one.

Deliverables
• One main notebook producing: 3–5 choropleths, a small-multiples panel, and a CSV of indicators.
• README with data versions, chosen indicators and rationale, and interpretation highlights.

Stretch (no ML)
• Add road/rail/water overlays for context.
• Compare two ACS periods to visualize change.

PROJECT 2 — STREET NETWORKS, AMENITIES, AND WALKABILITY (OPENSTREETMAP)

Aim
Use OpenStreetMap (OSM) street networks and points of interest (POIs) to analyze local accessibility and create thematic maps/community profiles.

Datasets
• OSM extracts via Geofabrik (https://download.geofabrik.de/) or Overpass API (amenities like schools, clinics, supermarkets, parks)
• Administrative boundary for study area (Natural Earth: https://www.naturalearthdata.com/ or local boundary shapefile)

Key libraries
• osmnx to download and analyze street networks, compute graph metrics, and sample POIs
• geopandas/shapely for spatial joins and buffers
• mapclassify/matplotlib/contextily for cartography

Workflow milestones

Define area of interest: municipal boundary or buffered center point.

Street graph: download walking network; compute network density, average street length, node degree distribution, and intersection density.

Amenities: retrieve POIs by amenity tags; clean attributes (name, opening_hours if present).

Accessibility metrics:

Buffer-based: count amenities within 400m/800m of each neighborhood centroid.

Network-based (optional): compute network distance to nearest amenity category.

Composite walkability index (transparent): normalize z-scores for intersection density, amenity counts, and sidewalk presence if available; document weighting.

Mapping:

Heatmap or choropleth of index by neighborhood.

Dot maps of amenities, symbolized by category.

Network overlays for context.

Export: summary tables per neighborhood; figures of amenity clusters and index.

Quality concerns / pitfalls
• OSM completeness varies by city and category; acknowledge coverage caveats.
• Ensure de-duplication of POIs and consistent tags.
• Use projected CRS for buffer distances (meters), not Web Mercator.

Deliverables
• Notebook producing amenities dot maps, street metrics, and a walkability choropleth.
• README documenting tags used, completeness caveats, and the index recipe.

Stretch (no ML)
• Temporal comparison using OSM historical snapshots (if available via third-party archives).
• Compare network vs Euclidean accessibility maps.

PROJECT 3 — AIR QUALITY EXPLORATORY ANALYSIS AND SPATIAL INTERPOLATION (OPENAQ)

Aim
Explore PM2.5 and/or NO2 patterns using sensor observations, create time series summaries, and produce simple spatial interpolations for visualization.

Datasets
• OpenAQ observations and station metadata (https://openaq.org/ and API docs: https://docs.openaq.org/)
• Administrative boundaries for context (country/region/city)

Key libraries
• pandas for time series aggregation; geopandas for spatial joins
• matplotlib for time series plots; mapclassify/contextily for maps
• For interpolation to a grid (visualization-only): scipy's griddata or PyKrige (document assumptions)

Workflow milestones

Data fetch: select a period and pollutant; download stations and measurements; cache raw JSON/CSV.

Cleaning: parse timestamps to UTC; remove impossible values; aggregate to daily/weekly means per station.

Exploratory plots:

Daily/weekly trend for the study area.

Station coverage map with symbol size proportional to data availability.

Spatial visualization:

Station bubble map with mean pollutant levels.

Optional gridded surface (interpolated) with clear "for visualization only" caveat.

Context: overlay major roads or land-use polygons if available to interpret hotspots.

Export: tables of station summaries; maps; a short text summary of patterns (diurnal/weekly if available).

Quality concerns / pitfalls
• Station heterogeneity: different instruments/QA; do not infer absolute exposure gradients from simple interpolation.
• Temporal alignment: ensure consistent averaging window when comparing stations.
• Units: verify µg/m³ vs ppb/ppm; standardize unit labels on plots.

Deliverables
• Notebook producing time series, station maps, and an optional interpolated surface (with caveats).
• README with explicit limitations and data citation.

Stretch (no ML)
• Compute exceedance days vs WHO guideline thresholds.
• Contrast weekday vs weekend means.

PROJECT 4 — GLOBAL LAND COVER SNAPSHOT AND CHANGE-OF-INTEREST VIEW (RASTER)

Aim
Work with raster datasets to extract land-cover composition within a polygon (country, park, city) and visualize a "change of interest" view between two epochs.

Datasets (choose one set)
• ESA WorldCover 10 m (2020/2021): https://esa-worldcover.org/
• Or MODIS Land Cover (MCD12Q1) yearly global product (https://lpdaac.usgs.gov/; requires account)
• Study area boundary: Natural Earth or local AOI polygon

Key libraries
• rasterio/rioxarray/xarray for raster reading, masking, and zonal counts
• geopandas for vector masks
• matplotlib for category maps (use official color keys if provided)

Workflow milestones

Data acquisition: download the relevant tiles for AOI; keep raw compressed archives.

Preprocess: mosaic/clip to AOI; confirm category codes and legend.

Composition: count pixels by class; convert to area using pixel resolution; produce a bar chart and table.

Change-of-interest view: pick two dates; compute simple difference in "target" class presence (e.g., forest gained/lost, urban expansion) as a categorical comparison; map only the change of that class (gain/loss/no change).

Export: category composition table; static maps; legend image; clear note on the classification scheme used.

Quality concerns / pitfalls
• Different products/versions have different class schemas; don't mix without crosswalk.
• Beware resampling artifacts; prefer nearest neighbor for categorical rasters.
• Use equal-area CRS for area summaries.

Deliverables
• Notebook producing a clipped land-cover map, composition chart, and a target-class change view.
• README with product/version, tiles used, projection, and legend cross-reference.

Stretch (no ML)
• Add topography (SRTM) contours for context.
• Compare two different AOIs side by side.

PROJECT 5 — SPECIES OCCURRENCE MAPPING AND ENVIRONMENTAL CONTEXT (GBIF)

Aim
Map species occurrence records, clean common issues, summarize by habitat/biome, and relate observations to simple environmental gradients (elevation, temperature bins) for descriptive insight.

Datasets
• GBIF occurrence download for a chosen species/taxon and region (https://www.gbif.org/)
• Environmental layers (choose simple, low-barrier sets):

Elevation (SRTM/merit DEM; subsets via https://gisboundaries.org/ or regional sources)

Optionally WorldClim bioclimatic variables (https://www.worldclim.org/data/worldclim21.html)

Key libraries
• pandas/geopandas for tabular and spatial cleaning
• shapely for geometry creation from lat/long; drop invalids
• rasterio/rioxarray for extracting environmental values

Workflow milestones

GBIF download: include fields for coordinates, date, basis of record, coordinate uncertainty, and license.

Cleaning: drop records with high coordinate uncertainty or missing coordinates; filter to study window and plausible date range; remove exact duplicates; document filters in README.

Mapping: occurrence dot map; density hexbin or kernel density estimate (for visualization only) to highlight clusters.

Environmental context: sample elevation (and optionally temperature) at occurrence points; create distributions/boxplots; compare to random background points within AOI for context (visual only, no inference).

Summaries: counts by month/season; top data providers.

Export: cleaned occurrence CSV (with only non-sensitive fields), maps, and summary plots.

Quality concerns / pitfalls
• Coordinate uncertainty and sampling bias; never infer absence from lack of records.
• Sensitive species: check GBIF licenses and data sensitivity flags.
• Projection choice for density representations.

Deliverables
• Notebook producing occurrence maps, environmental distributions, and summary tables.
• README documenting quality filters and licensing.

Stretch (no ML)
• Stratify maps by basis of record (human observation vs machine).
• Compare two related species.

PROJECT 6 — HAZARD EXPOSURE OVERLAY: FLOOD OR WILDFIRE vs POPULATION

Aim
Overlay a hazard intensity surface with population to quantify and visualize potential exposure. Produce simple exposure tables and maps for decision support.

Datasets (choose per hazard)
• Flood hazard (global or national):

JRC Global Flood Hazard maps (e.g., 100-year flood) https://data.jrc.ec.europa.eu/collection/id-0054

FEMA NFHL (U.S.) https://msc.fema.gov/nfhl (vector)
• Wildfire (U.S. example):

Wildfire Hazard Potential (WHP) raster: https://www.fs.usda.gov/rds/archive/catalog/RDS-2020-0016
• Population

Gridded Population of the World (GPWv4) https://sedac.ciesin.columbia.edu/data/collection/gpw-v4

WorldPop as alternative https://www.worldpop.org/

Key libraries
• rasterio/rioxarray/xarray for rasters; geopandas for boundaries; numpy for zonal summaries
• mapclassify/matplotlib for maps and exposure bar charts

Workflow milestones

AOI boundary: country, state, or watershed polygon; reproject all layers to a suitable equal-area CRS.

Harmonize rasters: resample to a common grid/cell size; align extents (document resampling method).

Exposure classification: define hazard intensity classes (e.g., low/medium/high); categorize population raster to "population in class."

Zonal exposure table: sum population per hazard class overall and by administrative unit.

Maps:

Hazard map with class legend.

Bivariate or side-by-side maps of hazard and population density.

Choropleth of percent population in high hazard by admin unit.

Export: exposure tables (CSV), map figures, and a short written interpretation.

Quality concerns / pitfalls
• Resolution mismatch: document resampling direction and implications.
• Risk vs hazard: clarify you are mapping hazard coincidence with population, not risk outcomes.
• Population year vs hazard epoch: state the years; avoid implying temporal causality.

Deliverables
• Notebook producing exposure tables and maps, with clear legends and notes.
• README clarifying assumptions and limitations.

Stretch (no ML)
• Compare two hazards (e.g., flood and wildfire) and produce a combined exposure table.
• Add critical infrastructure points (schools, hospitals) as overlays.

OPTIONAL "PROJECT 0" — PROJECTION & CARTOGRAPHY PRACTICE (NATURAL EARTH)

Aim
Warm-up exercise to ensure the environment and your mapping workflow are solid. Create world/regional maps with different projections and styling; label capitals; add graticules; export high-res figures.

Datasets
• Natural Earth Admin 0/1, populated places, oceans, rivers (https://www.naturalearthdata.com/)

Workflow highlights
• Read shapefiles, set CRS, reproject to 3–4 projections (e.g., Robinson, Equal Earth, Lambert Conformal Conic for a region).
• Style polygons and lines; add scale bars, north arrows, and attribution.
• Export print-quality PNG/SVG.

Deliverables
• A single notebook and 3–4 figure exports demonstrating projection and cartography basics.

GENERAL REPORTING & REPRODUCIBILITY NOTES
• Every project's README should list: dataset names, versions/dates, URLs, licenses, spatial/temporal coverage, CRS, and any filters used.
• Keep "data/raw" immutable; anything edited goes into "data/interim" or "processed."
• Save final maps at consistent sizes (e.g., 300 dpi) and include legends and captions that stand on their own.
• Include a "Known limitations" section in each README.
• Credit and cite data providers exactly as requested on their sites.

NEXT STEPS AFTER PHASE 1 (NON-ML)
• Add interactivity using lightweight tools (e.g., folium or kepler.gl) while keeping static exports as the canonical results.
• Introduce simple spatial statistics (e.g., Moran's I, Geary's C) for clustering/hotspot diagnostics, clearly labeled as exploratory.
• Begin assembling a cross-project "atlas" README that links to each project's outputs and summarizes key insights.
