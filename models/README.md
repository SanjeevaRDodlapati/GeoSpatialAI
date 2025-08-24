# 🤖 Models Directory

Unified directory structure for all machine learning models in the GeoSpatial Conservation AI Platform.

## 📁 Directory Structure

```
models/
├── checkpoints/                     # Binary model files (weights, trained models)
│   ├── yolov8n.pt                  # YOLOv8 Nano model for wildlife detection
│   ├── sam/                        # Segment Anything Model files
│   │   └── sam_vit_h.pth          # SAM ViT-H model weights (2.4GB)
│   └── madagascar_specialized/      # Madagascar-specific trained models
├── implementations/                 # Model implementation code (Python classes)
│   ├── __init__.py                 # Module initialization
│   ├── prithvi.py                  # PRITHVI foundation model implementation
│   ├── yolo_variants.py           # YOLOv8 variants and customizations
│   └── sam_variants.py            # SAM model variants
└── configs/                        # Model configuration files
    ├── yolo_config.yaml           # YOLOv8 training configurations
    ├── sam_config.yaml            # SAM model configurations
    └── madagascar_species.json    # Madagascar species mappings
```

## 🎯 Model Categories

### **Production Models (checkpoints/)**
- **YOLOv8**: Wildlife detection and classification
- **SAM**: Habitat segmentation and boundary detection
- **Specialized Models**: Madagascar-specific trained models

### **Model Implementations (implementations/)**
- **PRITHVI**: NASA-IBM foundation model for Earth observation
- **Custom Variants**: Platform-specific model modifications
- **Integration Code**: Model loading and inference utilities

### **Configuration Files (configs/)**
- **Training Configs**: Hyperparameters and training settings
- **Species Mappings**: Conservation-specific data mappings
- **Deployment Configs**: Production deployment settings

## 🔧 Usage

### **Loading Models with Centralized Paths**
```python
from src.utils.model_paths import get_yolo_path, get_sam_path, get_models_info

# Load YOLOv8 model
yolo_path = get_yolo_path()
model = YOLO(yolo_path)

# Load SAM model
sam_path = get_sam_path("vit_h")
sam = sam_model_registry["vit_h"](checkpoint=sam_path)

# Get all model information
info = get_models_info()
print(f"Models directory: {info['checkpoints_dir']}")
```

### **Using Model Implementations**
```python
from models.implementations.prithvi import create_prithvi_model

# Create PRITHVI model for change detection
model = create_prithvi_model()
```

## 📊 Model Specifications

| Model | Size | Purpose | Status | Location |
|-------|------|---------|--------|----------|
| **YOLOv8n** | 6MB | Wildlife detection | ✅ Production | `checkpoints/yolov8n.pt` |
| **SAM ViT-H** | 2.4GB | Habitat segmentation | ✅ Production | `checkpoints/sam/sam_vit_h.pth` |
| **PRITHVI** | Implementation | Earth observation | 🔬 Research | `implementations/prithvi.py` |

## 🔄 Migration from Previous Structure

This unified structure consolidates:
- Previous `/models/` (model weights) → `checkpoints/`
- Previous `/model_research/models/` (code) → `implementations/`

All existing code paths are maintained for backward compatibility through `src/utils/model_paths.py`.

## 🌿 Conservation Applications

### **Wildlife Monitoring**
- YOLOv8 for camera trap analysis
- SAM for habitat boundary mapping
- Species-specific model variants

### **Habitat Analysis**
- PRITHVI for Earth observation analysis
- SAM for ecosystem segmentation
- Change detection models

### **Real-time Monitoring**
- Optimized model checkpoints for field deployment
- Edge-compatible model formats
- Mobile-optimized variants

## 🚀 Future Enhancements

- **Madagascar Specialized Models**: Fine-tuned for endemic species
- **Multi-modal Integration**: Combined vision-audio-satellite models
- **Edge Deployment**: TensorFlow Lite and ONNX export formats
- **Model Versioning**: Systematic version control for model updates

---

*Part of the GeoSpatial Conservation AI Platform - Focused enhancement for production conservation impact*
