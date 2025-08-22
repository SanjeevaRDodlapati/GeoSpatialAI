# Environment Migration Guide
# ==========================
# Simple guide to transition from .venv to conda geo_env

## Current Setup Summary
- **Current Environment**: Mixed (.venv + conda base)
- **New Environment**: Dedicated conda environment (geo_env)
- **Benefits**: Cleaner dependency management, easier reproducibility

## Migration Steps

### 1. Create the New Conda Environment
```bash
# Run the automated setup
./setup_conda_env.sh

# Or create manually
conda env create -f environment_geo.yml
```

### 2. Activate New Environment
```bash
conda activate geo_env
```

### 3. Test the Environment
```bash
# Test core packages
python -c "
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import jupyter
import fastapi
print('✅ All core packages working!')
"
```

### 4. Update Development Workflows

#### For Jupyter Notebooks:
```bash
conda activate geo_env
jupyter lab
```

#### For Phase 4A AI Agents:
```bash
conda activate geo_env
cd ml_model_integration/phase4a_agents
python development_setup.py
```

#### For ML Model Integration:
```bash
conda activate geo_env
# All existing notebooks should work with the new environment
```

### 5. Optional: Remove Old .venv (after testing)
```bash
# Only after confirming everything works in geo_env
rm -rf .venv
```

## Package Versions Matched
The new environment includes all packages currently used:

### Core Scientific
- numpy==1.26.4
- pandas==2.2.2
- matplotlib==3.8.4
- plotly==5.22.0

### Geospatial
- geopandas==1.1.1
- rasterio==1.4.3
- shapely==2.1.1
- fiona==1.10.1
- pyproj==3.7.2

### ML/AI
- scikit-learn==1.4.2
- pytorch==2.2.2
- torchvision==0.17.2
- tensorflow==2.16.2

### Jupyter
- jupyterlab==4.0.11
- jupyter==1.0.0
- notebook==7.0.8

### Development
- pytest==7.4.4
- fastapi (latest)
- uvicorn (latest)
- pydantic==2.11.7

## Verification Commands

### Check Environment
```bash
conda activate geo_env
conda list | grep -E "(numpy|pandas|geopandas|jupyter|fastapi)"
```

### Test Notebooks
```bash
conda activate geo_env
jupyter lab
# Open any existing notebook and run a few cells
```

### Test Phase 4A Development
```bash
conda activate geo_env
cd ml_model_integration/phase4a_agents
python -c "
from mcp_foundation.simple_conservation_server import SimpleConservationServer
print('✅ Phase 4A imports working!')
"
```

## Benefits of New Setup

1. **Consistent Environment**: All team members get exactly the same packages
2. **Version Control**: Environment definition is in git
3. **Reproducibility**: Easy to recreate on new machines
4. **Isolation**: No conflicts with system Python or other projects
5. **Easy Updates**: Simple conda commands to add/update packages

## Troubleshooting

### If environment creation fails:
```bash
# Clean conda cache
conda clean --all

# Try creating with minimal packages first
conda create -n geo_env_test python=3.11 numpy pandas
conda activate geo_env_test
```

### If packages are missing:
```bash
# Install additional packages as needed
conda activate geo_env
conda install package_name
# or
pip install package_name
```

### If Jupyter kernels don't work:
```bash
conda activate geo_env
python -m ipykernel install --user --name geo_env --display-name "GeoSpatialAI"
```

## Next Steps After Migration

1. ✅ Activate geo_env
2. ✅ Test existing notebooks
3. ✅ Run Phase 4A development setup
4. ✅ Commit environment files to git
5. ✅ Update documentation with new setup instructions
