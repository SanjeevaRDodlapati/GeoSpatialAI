#!/bin/bash
# Geospatial Environment Activation Script

echo "🌍 Activating Geospatial Data Analysis Environment"
echo "================================================="

# Navigate to project directory
cd "$(dirname "$0")"
PROJECT_DIR=$(pwd)
echo "📁 Project Directory: $PROJECT_DIR"

# Check if conda geo_env is available and activate it
if conda env list | grep -q "geo_env"; then
    echo "🐍 Activating conda geo_env environment..."
    # Note: This script should be run with: source activate_env.sh
    # For direct activation, use: conda activate geo_env
    echo "   Run: conda activate geo_env"
    
    # Check if already activated
    if [[ "$CONDA_DEFAULT_ENV" == "geo_env" ]]; then
        echo "✅ geo_env environment already active"
    else
        echo "⚠️  Please run: conda activate geo_env"
    fi
else
    echo "❌ Conda geo_env environment not found!"
    echo "Please create it with: conda create -n geo_env python=3.9"
    exit 1
fi

# Display environment info
echo "🐍 Python: $(which python)"
echo "📦 Python Version: $(python --version)"

# Verify conda environment is properly activated
if [[ "$CONDA_DEFAULT_ENV" == "geo_env" ]]; then
    echo "✅ Conda environment properly activated: $CONDA_DEFAULT_ENV"
else
    echo "⚠️  Warning: Expected geo_env, currently using: $CONDA_DEFAULT_ENV"
fi

# Check if Jupyter is available
if command -v jupyter &> /dev/null; then
    echo "📓 Jupyter available: $(which jupyter)"
    echo ""
    echo "🚀 Ready to start! You can now:"
    echo "   • Run 'jupyter notebook' to start Jupyter"
    echo "   • Run 'jupyter lab' for JupyterLab"
    echo "   • Navigate to 'projects/project_0_cartography_practice/notebooks/'"
    echo "   • Select 'Geospatial Python' kernel in Jupyter"
    echo ""
else
    echo "❌ Jupyter not found in PATH"
fi

echo "================================================="
echo "Environment ready! 🎉"
