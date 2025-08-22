#!/bin/bash
# Geospatial Environment Activation Script

echo "🌍 Activating Geospatial Data Analysis Environment"
echo "================================================="

# Navigate to project directory
cd "$(dirname "$0")"
PROJECT_DIR=$(pwd)
echo "📁 Project Directory: $PROJECT_DIR"

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment (.venv) activated"
else
    echo "❌ Virtual environment (.venv) not found!"
    echo "Please run: python3 -m venv .venv"
    exit 1
fi

# Display environment info
echo "🐍 Python: $(which python)"
echo "📦 Python Version: $(python --version)"

# Verify virtual environment is properly activated
if [[ "$VIRTUAL_ENV" == *".venv"* ]]; then
    echo "✅ Virtual environment properly activated: $VIRTUAL_ENV"
else
    echo "⚠️  Warning: Virtual environment may not be properly activated"
    echo "   Current VIRTUAL_ENV: $VIRTUAL_ENV"
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
