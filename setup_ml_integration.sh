#!/bin/bash

# GeoSpatialAI ML Model Integration Setup Script
# ==============================================
# Automated setup for Conservation AI Platform
# 
# This script installs dependencies, downloads models,
# and initializes the ML integration system.
#
# Author: GeoSpatialAI Development Team
# Date: August 21, 2025
# Version: 1.0.0

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# System information
SYSTEM_NAME="GeoSpatialAI Conservation AI Platform"
VERSION="1.0.0"
SETUP_LOG="ml_integration_setup.log"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$SETUP_LOG"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$SETUP_LOG"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$SETUP_LOG"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$SETUP_LOG"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python_version() {
    print_status "Checking Python version..."
    
    if command_exists python3; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        print_status "Python version: $PYTHON_VERSION"
        
        # Check if version is 3.8 or higher
        if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'; then
            print_success "Python version is compatible"
            return 0
        else
            print_error "Python 3.8+ required. Current version: $PYTHON_VERSION"
            return 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.8+"
        return 1
    fi
}

# Function to check system requirements
check_system_requirements() {
    print_status "Checking system requirements..."
    
    # Check available memory
    if command_exists free; then
        MEMORY_GB=$(free -g | awk '/^Mem:/{print $2}')
        print_status "Available memory: ${MEMORY_GB}GB"
        
        if [ "$MEMORY_GB" -lt 4 ]; then
            print_warning "Recommended minimum 4GB RAM. Current: ${MEMORY_GB}GB"
        fi
    fi
    
    # Check disk space
    if command_exists df; then
        DISK_SPACE=$(df -h . | awk 'NR==2 {print $4}')
        print_status "Available disk space: $DISK_SPACE"
    fi
    
    # Check for GPU (optional)
    if command_exists nvidia-smi; then
        print_status "NVIDIA GPU detected"
        nvidia-smi --query-gpu=name,memory.total --format=csv,noheader | tee -a "$SETUP_LOG"
    else
        print_warning "No NVIDIA GPU detected. Will use CPU for inference."
    fi
}

# Function to activate existing virtual environment
activate_virtual_environment() {
    print_status "Using existing virtual environment..."
    
    if [ -d ".venv" ]; then
        print_status "Found existing .venv environment"
        source .venv/bin/activate
        print_success "Virtual environment activated"
    else
        print_status "Creating new virtual environment..."
        python3 -m venv .venv
        source .venv/bin/activate
        print_success "Virtual environment created and activated"
    fi
    
    # Upgrade pip
    pip install --upgrade pip
    print_success "pip upgraded to latest version"
}

# Function to install Python dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Install base requirements first
    if [ -f "requirements.txt" ]; then
        print_status "Installing base requirements..."
        pip install -r requirements.txt
        print_success "Base requirements installed"
    fi
    
    # Install ML integration requirements
    if [ -f "requirements_ml_integration.txt" ]; then
        print_status "Installing ML integration requirements..."
        pip install -r requirements_ml_integration.txt
        print_success "ML integration requirements installed"
    else
        print_warning "requirements_ml_integration.txt not found. Installing core packages..."
        
        # Install core ML packages
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
        pip install ultralytics
        pip install librosa
        pip install opencv-python
        pip install transformers
        pip install segment-anything-py
        pip install tensorflow
        pip install click
        pip install pyyaml
        
        print_success "Core ML packages installed"
    fi
}

# Function to download model checkpoints
download_models() {
    print_status "Downloading ML model checkpoints..."
    
    # Create models directory
    mkdir -p ml_model_integration/models/checkpoints
    
    # Download YOLOv8 model
    print_status "Downloading YOLOv8 model..."
    python3 -c "
from ultralytics import YOLO
import os
os.makedirs('ml_model_integration/models/checkpoints', exist_ok=True)
model = YOLO('yolov8n.pt')
print('✅ YOLOv8 model downloaded successfully')
" | tee -a "$SETUP_LOG"
    
    # Create placeholder for other models
    print_status "Setting up model directories..."
    mkdir -p ml_model_integration/models/checkpoints/birdnet
    mkdir -p ml_model_integration/models/checkpoints/sam
    mkdir -p ml_model_integration/models/checkpoints/prithvi
    
    print_success "Model directories created"
}

# Function to create project structure
create_project_structure() {
    print_status "Creating project structure..."
    
    # Create main directories
    mkdir -p ml_model_integration/{data/{input,output,processed},results/{wildlife,acoustic,habitat,integrated},logs,cache}
    mkdir -p ml_model_integration/models/{checkpoints,configs,custom}
    mkdir -p ml_model_integration/phase2_madagascar_specialization
    mkdir -p ml_model_integration/phase3_production_deployment
    
    # Create data subdirectories
    mkdir -p ml_model_integration/data/madagascar/{species,boundaries,elevation,protected_areas}
    
    print_success "Project structure created"
}

# Function to initialize configuration
initialize_configuration() {
    print_status "Initializing system configuration..."
    
    # Run Python initialization
    python3 -c "
import sys
sys.path.append('ml_model_integration')
from ml_model_integration import initialize_ml_system

# Initialize system with default configuration
orchestrator = initialize_ml_system()
if orchestrator:
    print('✅ ML integration system initialized successfully')
else:
    print('❌ Failed to initialize ML integration system')
    sys.exit(1)
" | tee -a "$SETUP_LOG"
}

# Function to run system tests
run_system_tests() {
    print_status "Running system tests..."
    
    python3 -c "
import sys
sys.path.append('ml_model_integration')

try:
    from ml_model_integration.conservation_ai_orchestrator import run_phase1_implementation_test
    
    # Run Phase 1 tests
    orchestrator = run_phase1_implementation_test()
    
    if orchestrator:
        print('✅ Phase 1 foundation models test passed')
    else:
        print('❌ Phase 1 foundation models test failed')
        sys.exit(1)
        
except Exception as e:
    print(f'❌ System test failed: {e}')
    sys.exit(1)
" | tee -a "$SETUP_LOG"
}

# Function to create sample data
create_sample_data() {
    print_status "Creating sample data and configurations..."
    
    # Create sample configuration
    cat > ml_model_integration/sample_config.yaml << EOF
# Sample Configuration for GeoSpatialAI ML Integration
system:
  name: "Conservation AI Platform"
  version: "1.0.0"
  deployment_mode: "development"

models:
  wildlife_detection:
    confidence_threshold: 0.6
    model_type: "yolov8n"
  acoustic_monitoring:
    confidence_threshold: 0.7
    sample_rate: 48000
  habitat_segmentation:
    model_type: "vit_h"

madagascar_specialization:
  endemic_species_priority: true
  conservation_status_filtering: true
EOF
    
    # Create sample Madagascar species list
    cat > ml_model_integration/data/madagascar/species/endemic_species.json << EOF
{
  "mammals": [
    {"species": "Lemur catta", "common_name": "Ring-tailed Lemur", "status": "Endangered"},
    {"species": "Indri indri", "common_name": "Indri", "status": "Critically Endangered"},
    {"species": "Propithecus verreauxi", "common_name": "Verreaux's Sifaka", "status": "Vulnerable"}
  ],
  "birds": [
    {"species": "Vanga curvirostris", "common_name": "Hook-billed Vanga", "status": "Least Concern"},
    {"species": "Coua caerulea", "common_name": "Blue Coua", "status": "Least Concern"},
    {"species": "Mesitornis variegatus", "common_name": "White-breasted Mesite", "status": "Vulnerable"}
  ],
  "reptiles": [
    {"species": "Brookesia micra", "common_name": "Nosy Hara Leaf Chameleon", "status": "Near Threatened"},
    {"species": "Uroplatus phantasticus", "common_name": "Satanic Leaf-tailed Gecko", "status": "Least Concern"}
  ]
}
EOF
    
    print_success "Sample data and configurations created"
}

# Function to display final instructions
display_final_instructions() {
    echo ""
    echo "=============================================="
    echo -e "${GREEN}🎉 Setup Complete!${NC}"
    echo "=============================================="
    echo ""
    echo -e "${BLUE}$SYSTEM_NAME v$VERSION${NC}"
    echo "Conservation AI Platform is ready for use!"
    echo ""
    echo "🚀 Quick Start:"
    echo "  1. Activate virtual environment: source .venv/bin/activate"
    echo "  2. Check system status: python3 -m ml_model_integration status"
    echo "  3. Run demo: python3 -m ml_model_integration demo"
    echo ""
    echo "📚 Available Commands:"
    echo "  • python3 -m ml_model_integration init     # Initialize system"
    echo "  • python3 -m ml_model_integration status   # Check status"
    echo "  • python3 -m ml_model_integration analyze  # Analyze data"
    echo "  • python3 -m ml_model_integration batch    # Batch processing"
    echo ""
    echo "📁 Key Directories:"
    echo "  • ml_model_integration/data/input/          # Input data"
    echo "  • ml_model_integration/results/             # Analysis results"
    echo "  • ml_model_integration/models/checkpoints/  # Model files"
    echo ""
    echo "📋 Documentation:"
    echo "  • ML_MODEL_INTEGRATION_PLAN.md  # Comprehensive plan"
    echo "  • README.md                     # General documentation"
    echo "  • $SETUP_LOG               # Setup log"
    echo ""
    echo "🌍 Next Steps for Madagascar Conservation:"
    echo "  1. Add your conservation data to ml_model_integration/data/input/"
    echo "  2. Configure Madagascar-specific settings in config.yaml"
    echo "  3. Run comprehensive analysis on your datasets"
    echo "  4. Proceed to Phase 2: Madagascar specialization"
    echo ""
    echo "✅ Happy Conservation Analysis! 🌿🦎🐦"
}

# Main setup function
main() {
    echo "=============================================="
    echo -e "${BLUE}🌍 $SYSTEM_NAME v$VERSION${NC}"
    echo "=============================================="
    echo "ML Model Integration Setup"
    echo ""
    echo "This script will:"
    echo "  ✓ Check system requirements"
    echo "  ✓ Create virtual environment"
    echo "  ✓ Install dependencies"
    echo "  ✓ Download ML models"
    echo "  ✓ Initialize configuration"
    echo "  ✓ Run system tests"
    echo ""
    echo "Setup log: $SETUP_LOG"
    echo ""
    
    # Start setup log
    echo "GeoSpatialAI ML Integration Setup - $(date)" > "$SETUP_LOG"
    
    # Run setup steps
    print_status "Starting setup process..."
    
    check_python_version || exit 1
    check_system_requirements
    activate_virtual_environment
    install_dependencies
    create_project_structure
    download_models
    create_sample_data
    initialize_configuration
    run_system_tests
    
    print_success "All setup steps completed successfully!"
    
    display_final_instructions
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
