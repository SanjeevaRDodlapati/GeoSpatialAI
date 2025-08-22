#!/bin/bash
# Quick Environment Check Script
# Run this to verify your development environment is properly set up

echo "🔍 ENVIRONMENT DIAGNOSTIC TOOL"
echo "================================"

# Check current directory
echo "📁 Current Directory: $(pwd)"

# Check if we're in the right directory
if [ ! -f "test_environment.py" ]; then
    echo "❌ Not in GeoSpatialAI project directory"
    echo "   Please cd to the project root directory"
    exit 1
fi

# Check Python interpreter
echo "🐍 Current Python: $(which python)"
echo "📦 Python Version: $(python --version)"

# Check virtual environment
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Virtual Environment Active: $VIRTUAL_ENV"
    if [[ "$VIRTUAL_ENV" == *".venv"* ]]; then
        echo "✅ Using project virtual environment"
    else
        echo "⚠️  Using different virtual environment"
    fi
else
    echo "❌ No virtual environment active"
    echo "   Run: source .venv/bin/activate"
fi

# Check if .venv exists
if [ -d ".venv" ]; then
    echo "✅ Virtual environment directory exists"
    # Test with explicit path
    echo ""
    echo "🧪 Testing with project Python:"
    ./.venv/bin/python -c "import geopandas; print('✅ GeoPandas:', geopandas.__version__)" 2>/dev/null || echo "❌ GeoPandas not available"
    ./.venv/bin/python -c "import streamlit; print('✅ Streamlit:', streamlit.__version__)" 2>/dev/null || echo "❌ Streamlit not available"
else
    echo "❌ Virtual environment directory not found"
    echo "   Run: python -m venv .venv"
fi

echo ""
echo "🎯 RECOMMENDATION:"
if [ -d ".venv" ] && [[ "$VIRTUAL_ENV" == *".venv"* ]]; then
    echo "✅ Environment looks good! Run: python test_environment.py"
elif [ -d ".venv" ]; then
    echo "🔧 Activate virtual environment: source .venv/bin/activate"
    echo "   Then run: python test_environment.py"
else
    echo "🔧 Create and activate virtual environment:"
    echo "   python -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
fi

echo "================================"
