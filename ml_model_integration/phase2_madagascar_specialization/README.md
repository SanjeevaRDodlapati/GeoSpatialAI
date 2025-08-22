# Phase 2: Madagascar Specialization & Transfer Learning

## 🎯 Overview
Phase 2 focuses on specializing the foundation models for Madagascar's unique biodiversity and conservation challenges.

## 🗂️ Directory Structure
```
phase2_madagascar_specialization/
├── datasets/                   # Specialized datasets
│   ├── madagascar_wildlife_images/
│   ├── endemic_bird_audio/
│   ├── ecosystem_boundaries/
│   └── lemur_identification/
├── models/                     # Specialized models
│   ├── yolov8_madagascar/
│   ├── birdnet_madagascar/
│   ├── sam_madagascar/
│   └── lemur_classifier/
├── training_pipelines/         # Training scripts
│   ├── yolov8_training/
│   ├── birdnet_training/
│   ├── sam_training/
│   └── lemur_training/
├── dataset_configs.json        # Dataset configurations
├── training_configs.json       # Training configurations
├── evaluation_config.json      # Evaluation framework
└── requirements_phase2.txt     # Additional dependencies
```

## 🚀 Getting Started

### 1. Install Phase 2 Dependencies
```bash
conda run -n base pip install -r requirements_phase2.txt
```

### 2. Data Preparation
```bash
python prepare_madagascar_datasets.py
```

### 3. Model Training
```bash
# YOLOv8 Madagascar Wildlife
python training_pipelines/yolov8_training/train_madagascar_wildlife.py

# BirdNET Madagascar Enhancement  
python training_pipelines/birdnet_training/train_madagascar_birds.py

# SAM Ecosystem Specialization
python training_pipelines/sam_training/train_madagascar_ecosystems.py

# Lemur Species Classifier
python training_pipelines/lemur_training/train_lemur_classifier.py
```

### 4. Evaluation and Benchmarking
```bash
python evaluate_specialized_models.py
```

## 📊 Expected Outcomes
- **YOLOv8 Madagascar**: >90% mAP on endemic species
- **BirdNET Enhancement**: >85% accuracy on Madagascar birds  
- **SAM Ecosystem**: >95% IoU on habitat segmentation
- **Lemur Classifier**: >92% accuracy on 108 species

## 🌟 Conservation Impact
- Real-time anti-poaching monitoring
- Automated biodiversity surveys
- Habitat change detection
- Species population tracking

Ready to begin Madagascar conservation AI specialization! 🦎🌿
