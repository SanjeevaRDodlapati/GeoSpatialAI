#!/bin/bash
# GeoSpatialAI Conda Environment Setup Script
# ==========================================
# Simple script to create and manage the geo_env conda environment

set -e  # Exit on any error

echo "🌿 GeoSpatialAI Conda Environment Setup"
echo "========================================"
echo ""

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Conda not found. Please install Anaconda or Miniconda first."
    exit 1
fi

echo "✅ Conda found: $(conda --version)"

# Function to create environment
create_environment() {
    echo ""
    echo "📦 Creating conda environment 'geo_env'..."
    echo "   This may take 5-10 minutes depending on your internet connection."
    echo ""
    
    if conda env list | grep -q "geo_env"; then
        echo "⚠️  Environment 'geo_env' already exists."
        read -p "   Do you want to remove and recreate it? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "🗑️  Removing existing environment..."
            conda env remove -n geo_env -y
        else
            echo "ℹ️  Keeping existing environment."
            return 0
        fi
    fi
    
    # Create environment from yml file
    conda env create -f environment_geo.yml
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Environment 'geo_env' created successfully!"
    else
        echo ""
        echo "❌ Failed to create environment. Check the error messages above."
        exit 1
    fi
}

# Function to activate environment
activate_environment() {
    echo ""
    echo "🔄 Activating conda environment 'geo_env'..."
    
    # For bash/zsh
    if [[ "$SHELL" == *"zsh"* ]]; then
        echo "   To activate in your current shell, run:"
        echo "   conda activate geo_env"
    elif [[ "$SHELL" == *"bash"* ]]; then
        echo "   To activate in your current shell, run:"
        echo "   conda activate geo_env"
    else
        echo "   To activate in your current shell, run:"
        echo "   conda activate geo_env"
    fi
}

# Function to test environment
test_environment() {
    echo ""
    echo "🧪 Testing environment installation..."
    
    # Activate environment and test key packages
    eval "$(conda shell.bash hook)"
    conda activate geo_env
    
    echo "   Testing core packages..."
    
    python -c "
import sys
print(f'✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')

# Test core scientific packages
try:
    import numpy as np
    print(f'✅ NumPy {np.__version__}')
except ImportError as e:
    print(f'❌ NumPy: {e}')

try:
    import pandas as pd
    print(f'✅ Pandas {pd.__version__}')
except ImportError as e:
    print(f'❌ Pandas: {e}')

try:
    import geopandas as gpd
    print(f'✅ GeoPandas {gpd.__version__}')
except ImportError as e:
    print(f'❌ GeoPandas: {e}')

try:
    import matplotlib.pyplot as plt
    print(f'✅ Matplotlib available')
except ImportError as e:
    print(f'❌ Matplotlib: {e}')

try:
    import plotly
    print(f'✅ Plotly {plotly.__version__}')
except ImportError as e:
    print(f'❌ Plotly: {e}')

try:
    import fastapi
    print(f'✅ FastAPI {fastapi.__version__}')
except ImportError as e:
    print(f'❌ FastAPI: {e}')

try:
    import jupyter
    print(f'✅ Jupyter available')
except ImportError as e:
    print(f'❌ Jupyter: {e}')

print('\\n🎉 Core packages test completed!')
"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Environment test passed!"
    else
        echo ""
        echo "❌ Environment test failed. Some packages may not be installed correctly."
    fi
}

# Function to show usage information
show_usage() {
    echo ""
    echo "🎯 GeoSpatialAI Environment Usage:"
    echo "=================================="
    echo ""
    echo "1. Activate environment:"
    echo "   conda activate geo_env"
    echo ""
    echo "2. Start Jupyter Lab:"
    echo "   jupyter lab"
    echo ""
    echo "3. Run Phase 4A AI agents:"
    echo "   cd ml_model_integration/phase4a_agents"
    echo "   python development_setup.py"
    echo ""
    echo "4. Deactivate environment:"
    echo "   conda deactivate"
    echo ""
    echo "5. Remove environment (if needed):"
    echo "   conda env remove -n geo_env"
    echo ""
}

# Main execution
main() {
    # Check if environment.yml exists
    if [ ! -f "environment_geo.yml" ]; then
        echo "❌ environment_geo.yml not found in current directory."
        echo "   Make sure you're in the GeoSpatialAI project root."
        exit 1
    fi
    
    # Ask user what they want to do
    echo "🎯 What would you like to do?"
    echo "1. Create new geo_env environment"
    echo "2. Test existing geo_env environment"
    echo "3. Show usage information"
    echo "4. Exit"
    echo ""
    
    read -p "Enter choice (1-4): " choice
    
    case $choice in
        1)
            create_environment
            activate_environment
            test_environment
            show_usage
            ;;
        2)
            if conda env list | grep -q "geo_env"; then
                test_environment
                show_usage
            else
                echo "❌ Environment 'geo_env' not found. Please create it first (option 1)."
            fi
            ;;
        3)
            show_usage
            ;;
        4)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please run the script again."
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
