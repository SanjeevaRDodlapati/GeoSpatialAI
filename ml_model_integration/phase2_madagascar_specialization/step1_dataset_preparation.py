#!/usr/bin/env python3
"""
Madagascar Dataset Preparation Pipeline
=======================================

Step 1 of Phase 2: Prepare and organize Madagascar-specific datasets for 
specialized model training.

Author: Madagascar Conservation AI Team
Date: August 2025
"""

import os
import sys
import logging
import json
import requests
import zipfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from PIL import Image
import cv2

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MadagascarDatasetPreparer:
    """Prepare Madagascar-specific datasets for conservation AI training."""
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.phase2_path = self.base_path / "ml_model_integration" / "phase2_madagascar_specialization"
        self.datasets_path = self.phase2_path / "datasets"
        
        # Dataset URLs and sources (simulated - would be real URLs)
        self.data_sources = {
            "madagascar_wildlife": {
                "description": "Camera trap images from Madagascar national parks",
                "source": "Madagascar National Parks + iNaturalist",
                "expected_samples": 15000,
                "species_count": 20
            },
            "lemur_species": {
                "description": "Comprehensive lemur species image database",
                "source": "Lemur Portal + Duke Lemur Center",
                "expected_samples": 25000,
                "species_count": 108
            },
            "bird_audio": {
                "description": "Madagascar endemic bird recordings",
                "source": "Xeno-canto + Macaulay Library",
                "expected_samples": 8000,
                "species_count": 250
            },
            "ecosystem_satellite": {
                "description": "Satellite imagery for ecosystem segmentation",
                "source": "Sentinel-2 + Landsat 8",
                "expected_samples": 5000,
                "ecosystem_types": 12
            }
        }
        
        # Madagascar species information
        self.madagascar_species = self.load_madagascar_species_database()
        
    def load_madagascar_species_database(self) -> Dict:
        """Load comprehensive Madagascar species database."""
        species_db = {
            "wildlife": {
                "Indri_indri": {"common": "Indri", "status": "CR", "habitat": "Rainforest", "activity": "Diurnal"},
                "Propithecus_diadema": {"common": "Diademed Sifaka", "status": "CR", "habitat": "Rainforest", "activity": "Diurnal"},
                "Lemur_catta": {"common": "Ring-tailed Lemur", "status": "EN", "habitat": "Spiny Forest", "activity": "Diurnal"},
                "Eulemur_macaco": {"common": "Black Lemur", "status": "VU", "habitat": "Dry Forest", "activity": "Cathemeral"},
                "Microcebus_murinus": {"common": "Gray Mouse Lemur", "status": "LC", "habitat": "Dry Forest", "activity": "Nocturnal"},
                "Daubentonia_madagascariensis": {"common": "Aye-aye", "status": "EN", "habitat": "Rainforest", "activity": "Nocturnal"},
                "Cryptoprocta_ferox": {"common": "Fossa", "status": "VU", "habitat": "Forest", "activity": "Cathemeral"},
                "Tenrec_ecaudatus": {"common": "Tailless Tenrec", "status": "LC", "habitat": "Various", "activity": "Nocturnal"},
                "Setifer_setosus": {"common": "Greater Hedgehog Tenrec", "status": "LC", "habitat": "Dry Forest", "activity": "Nocturnal"},
                "Hemicentetes_semispinosus": {"common": "Lowland Streaked Tenrec", "status": "LC", "habitat": "Rainforest", "activity": "Diurnal"},
                "Brookesia_micra": {"common": "Leaf Chameleon", "status": "NT", "habitat": "Dry Forest", "activity": "Diurnal"},
                "Furcifer_pardalis": {"common": "Panther Chameleon", "status": "LC", "habitat": "Coastal", "activity": "Diurnal"},
                "Uroplatus_fimbriatus": {"common": "Leaf-tail Gecko", "status": "VU", "habitat": "Rainforest", "activity": "Nocturnal"},
                "Anas_melleri": {"common": "Meller's Duck", "status": "EN", "habitat": "Wetland", "activity": "Diurnal"},
                "Tachybaptus_pelzelnii": {"common": "Madagascar Grebe", "status": "VU", "habitat": "Wetland", "activity": "Diurnal"},
                "Lophotibis_cristata": {"common": "Madagascar Crested Ibis", "status": "NT", "habitat": "Wetland", "activity": "Diurnal"},
                "Monias_benschi": {"common": "Subdesert Mesite", "status": "VU", "habitat": "Spiny Forest", "activity": "Diurnal"},
                "Coua_caerulea": {"common": "Blue Coua", "status": "LC", "habitat": "Rainforest", "activity": "Diurnal"},
                "Vanga_curvirostris": {"common": "Hook-billed Vanga", "status": "LC", "habitat": "Dry Forest", "activity": "Diurnal"},
                "Neodrepanis_coruscans": {"common": "Sunbird Asity", "status": "NT", "habitat": "Rainforest", "activity": "Diurnal"}
            },
            "ecosystems": {
                "Spiny_Forest": {"region": "South", "threats": ["Deforestation", "Agriculture"], "area_km2": 17000},
                "Dry_Deciduous_Forest": {"region": "West", "threats": ["Logging", "Fires"], "area_km2": 20000},
                "Eastern_Rainforest": {"region": "East", "threats": ["Slash-burn", "Mining"], "area_km2": 11000},
                "Central_Highland": {"region": "Central", "threats": ["Agriculture", "Erosion"], "area_km2": 18000},
                "Mangrove": {"region": "Coast", "threats": ["Aquaculture", "Development"], "area_km2": 3000},
                "Coastal_Dune": {"region": "Coast", "threats": ["Tourism", "Development"], "area_km2": 1000},
                "Agricultural_Land": {"region": "Various", "threats": ["Expansion", "Chemicals"], "area_km2": 35000},
                "Urban_Area": {"region": "Various", "threats": ["Expansion", "Pollution"], "area_km2": 2000},
                "Water_Body": {"region": "Various", "threats": ["Pollution", "Overfishing"], "area_km2": 5000},
                "Degraded_Forest": {"region": "Various", "threats": ["Continued_degradation"], "area_km2": 15000},
                "Grassland": {"region": "Central", "threats": ["Overgrazing", "Fires"], "area_km2": 10000},
                "Rocky_Outcrop": {"region": "Various", "threats": ["Mining", "Tourism"], "area_km2": 3000}
            }
        }
        
        logger.info(f"📋 Loaded Madagascar species database:")
        logger.info(f"   🦅 Wildlife species: {len(species_db['wildlife'])}")
        logger.info(f"   🌿 Ecosystem types: {len(species_db['ecosystems'])}")
        
        return species_db
    
    def create_directory_structure(self) -> None:
        """Create organized directory structure for Madagascar datasets."""
        logger.info("🏗️ Creating Madagascar dataset directory structure...")
        
        # Main dataset directories
        directories = [
            # Wildlife images
            self.datasets_path / "madagascar_wildlife_images" / "train" / "images",
            self.datasets_path / "madagascar_wildlife_images" / "train" / "labels",
            self.datasets_path / "madagascar_wildlife_images" / "val" / "images",
            self.datasets_path / "madagascar_wildlife_images" / "val" / "labels",
            self.datasets_path / "madagascar_wildlife_images" / "test" / "images",
            self.datasets_path / "madagascar_wildlife_images" / "test" / "labels",
            
            # Lemur species
            self.datasets_path / "lemur_identification" / "train",
            self.datasets_path / "lemur_identification" / "val",
            self.datasets_path / "lemur_identification" / "test",
            
            # Bird audio
            self.datasets_path / "endemic_bird_audio" / "train",
            self.datasets_path / "endemic_bird_audio" / "val",
            self.datasets_path / "endemic_bird_audio" / "test",
            
            # Ecosystem boundaries
            self.datasets_path / "ecosystem_boundaries" / "images",
            self.datasets_path / "ecosystem_boundaries" / "masks",
            self.datasets_path / "ecosystem_boundaries" / "metadata",
            
            # Camera trap data
            self.datasets_path / "camera_trap_data" / "raw",
            self.datasets_path / "camera_trap_data" / "processed",
            self.datasets_path / "camera_trap_data" / "annotations",
            
            # Satellite imagery
            self.datasets_path / "satellite_imagery" / "sentinel2",
            self.datasets_path / "satellite_imagery" / "landsat8",
            self.datasets_path / "satellite_imagery" / "labels"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"✅ Created: {directory}")
    
    def create_species_subdirectories(self) -> None:
        """Create species-specific subdirectories for lemur identification."""
        logger.info("🦎 Creating lemur species subdirectories...")
        
        lemur_species = [
            "Lemur_catta", "Eulemur_albifrons", "Eulemur_cinereiceps", "Eulemur_collaris",
            "Eulemur_coronatus", "Eulemur_flavifrons", "Eulemur_fulvus", "Eulemur_macaco",
            "Eulemur_mongoz", "Eulemur_rubriventer", "Eulemur_rufifrons", "Eulemur_rufus",
            "Eulemur_sanfordi", "Varecia_rubra", "Varecia_variegata", "Indri_indri",
            "Propithecus_candidus", "Propithecus_coquereli", "Propithecus_coronatus",
            "Propithecus_deckenii", "Propithecus_diadema", "Propithecus_edwardsi",
            "Propithecus_perrieri", "Propithecus_tattersalli", "Propithecus_verreauxi",
            "Avahi_betsileo", "Avahi_cleesei", "Avahi_laniger", "Avahi_occidentalis",
            "Microcebus_berthae", "Microcebus_bongolavensis", "Microcebus_griseorufus",
            "Microcebus_lehilahytsara", "Microcebus_murinus", "Microcebus_rufus",
            "Mirza_coquereli", "Cheirogaleus_major", "Cheirogaleus_medius",
            "Allocebus_trichotis", "Phaner_furcifer", "Lepilemur_dorsalis",
            "Lepilemur_edwardsi", "Lepilemur_leucopus", "Lepilemur_mustelinus",
            "Lepilemur_ruficaudatus", "Lepilemur_septentrionalis", "Daubentonia_madagascariensis"
        ]
        
        for split in ['train', 'val', 'test']:
            split_path = self.datasets_path / "lemur_identification" / split
            for species in lemur_species:
                species_dir = split_path / species
                species_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"✅ Created subdirectories for {len(lemur_species)} lemur species")
    
    def generate_sample_data(self) -> None:
        """Generate sample data for demonstration and testing."""
        logger.info("📊 Generating sample Madagascar conservation data...")
        
        # Generate sample wildlife detection annotations
        self.generate_wildlife_annotations()
        
        # Generate sample ecosystem metadata
        self.generate_ecosystem_metadata()
        
        # Generate sample audio metadata
        self.generate_audio_metadata()
        
        # Generate dataset statistics
        self.generate_dataset_statistics()
    
    def generate_wildlife_annotations(self) -> None:
        """Generate sample YOLO format annotations for wildlife detection."""
        logger.info("🦅 Generating wildlife detection annotations...")
        
        for split in ['train', 'val', 'test']:
            labels_dir = self.datasets_path / "madagascar_wildlife_images" / split / "labels"
            
            # Generate sample annotation files
            for i in range(10):  # Sample annotations
                annotation_file = labels_dir / f"madagascar_wildlife_{i:04d}.txt"
                
                # Generate random bounding boxes for demonstration
                annotations = []
                num_objects = np.random.randint(0, 4)  # 0-3 objects per image
                
                for j in range(num_objects):
                    species_id = np.random.randint(0, 20)  # 20 species
                    x_center = np.random.uniform(0.1, 0.9)
                    y_center = np.random.uniform(0.1, 0.9)
                    width = np.random.uniform(0.1, 0.3)
                    height = np.random.uniform(0.1, 0.3)
                    
                    annotations.append(f"{species_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
                
                with open(annotation_file, 'w') as f:
                    f.write('\n'.join(annotations))
        
        logger.info("✅ Wildlife detection annotations generated")
    
    def generate_ecosystem_metadata(self) -> None:
        """Generate ecosystem segmentation metadata."""
        logger.info("🌿 Generating ecosystem metadata...")
        
        metadata_dir = self.datasets_path / "ecosystem_boundaries" / "metadata"
        
        ecosystem_metadata = {
            "dataset_info": {
                "name": "Madagascar Ecosystem Segmentation",
                "version": "1.0",
                "description": "Satellite imagery with ecosystem boundary annotations",
                "total_images": 5000,
                "image_size": [1024, 1024],
                "channels": ["Red", "Green", "Blue", "NIR", "SWIR1", "SWIR2"],
                "spatial_resolution": "10m"
            },
            "ecosystem_classes": self.madagascar_species["ecosystems"],
            "annotation_format": "polygon_masks",
            "data_splits": {
                "train": 0.7,
                "val": 0.2,
                "test": 0.1
            }
        }
        
        metadata_file = metadata_dir / "ecosystem_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(ecosystem_metadata, f, indent=2)
        
        logger.info(f"✅ Ecosystem metadata saved: {metadata_file}")
    
    def generate_audio_metadata(self) -> None:
        """Generate bird audio dataset metadata."""
        logger.info("🎵 Generating bird audio metadata...")
        
        for split in ['train', 'val', 'test']:
            split_dir = self.datasets_path / "endemic_bird_audio" / split
            
            audio_metadata = {
                "dataset_info": {
                    "split": split,
                    "sample_rate": 22050,
                    "duration_seconds": 3.0,
                    "format": "wav",
                    "quality": "16-bit"
                },
                "species_list": [
                    "Coua_caerulea", "Vanga_curvirostris", "Neodrepanis_coruscans",
                    "Tylas_eduardi", "Calicalicus_madagascariensis", "Leptopterus_chabert",
                    "Xenopirostris_xenopirostris", "Oriolia_bernieri", "Hypositta_corallirostris",
                    "Atelornis_pittoides", "Brachypteracias_leptosomus", "Monias_benschi",
                    "Mesitornis_variegatus", "Leptosomus_discolor", "Anas_melleri",
                    "Tachybaptus_pelzelnii", "Lophotibis_cristata", "Threskiornis_bernieri",
                    "Ardeola_idae", "Circus_maillardi"
                ],
                "recording_locations": [
                    "Andasibe-Mantadia", "Ranomafana", "Masoala", "Ankarafantsika",
                    "Zombitse-Vohibasia", "Andohahela", "Marojejy", "Amber Mountain"
                ]
            }
            
            metadata_file = split_dir / f"{split}_audio_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(audio_metadata, f, indent=2)
        
        logger.info("✅ Bird audio metadata generated")
    
    def generate_dataset_statistics(self) -> None:
        """Generate comprehensive dataset statistics."""
        logger.info("📈 Generating dataset statistics...")
        
        statistics = {
            "madagascar_conservation_datasets": {
                "creation_date": "2025-08-22",
                "purpose": "Conservation AI model specialization",
                "geographic_focus": "Madagascar",
                "conservation_priority": "Endemic species protection"
            },
            "datasets": {
                "wildlife_detection": {
                    "total_images": 15000,
                    "species_count": 20,
                    "annotation_format": "YOLO",
                    "primary_habitats": ["Rainforest", "Dry Forest", "Spiny Forest"],
                    "data_sources": ["Camera traps", "Field surveys", "iNaturalist"],
                    "splits": {"train": 10500, "val": 3000, "test": 1500}
                },
                "lemur_classification": {
                    "total_images": 25000,
                    "species_count": 108,
                    "genera_count": 15,
                    "annotation_format": "Species labels",
                    "behavioral_features": True,
                    "conservation_status": True,
                    "splits": {"train": 17500, "val": 5000, "test": 2500}
                },
                "bird_audio": {
                    "total_recordings": 8000,
                    "species_count": 250,
                    "endemic_families": ["Vangidae", "Bernieridae", "Mesitornithidae"],
                    "recording_duration": "3-10 seconds",
                    "sample_rate": "22050 Hz",
                    "splits": {"train": 5600, "val": 1600, "test": 800}
                },
                "ecosystem_segmentation": {
                    "total_images": 5000,
                    "ecosystem_types": 12,
                    "image_size": "1024x1024",
                    "spatial_resolution": "10m",
                    "satellite_sources": ["Sentinel-2", "Landsat-8"],
                    "annotation_format": "Polygon masks",
                    "splits": {"train": 3500, "val": 1000, "test": 500}
                }
            },
            "conservation_impact": {
                "protected_areas_covered": 30,
                "endemic_species_focus": 128,
                "threatened_species_priority": 85,
                "habitat_types_monitored": 12,
                "anti_poaching_coverage": "Real-time",
                "biodiversity_assessment": "Automated"
            }
        }
        
        stats_file = self.datasets_path / "madagascar_dataset_statistics.json"
        with open(stats_file, 'w') as f:
            json.dump(statistics, f, indent=2)
        
        logger.info(f"✅ Dataset statistics saved: {stats_file}")
    
    def create_data_loading_utilities(self) -> None:
        """Create data loading and preprocessing utilities."""
        logger.info("🔧 Creating data loading utilities...")
        
        utils_dir = self.datasets_path / "utils"
        utils_dir.mkdir(exist_ok=True)
        
        # Create data loader utility
        data_loader_code = '''#!/usr/bin/env python3
"""
Madagascar Dataset Loading Utilities
===================================

Utilities for loading and preprocessing Madagascar conservation datasets.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd
from PIL import Image
import torch
from torch.utils.data import Dataset
import albumentations as A

class MadagascarWildlifeDataset(Dataset):
    """Dataset for Madagascar wildlife detection."""
    
    def __init__(self, data_dir: str, split: str = 'train', transform=None):
        self.data_dir = Path(data_dir)
        self.split = split
        self.transform = transform
        self.load_annotations()
    
    def load_annotations(self):
        """Load YOLO format annotations."""
        self.annotations = []
        labels_dir = self.data_dir / self.split / "labels"
        
        for label_file in labels_dir.glob("*.txt"):
            self.annotations.append({
                'image_path': self.data_dir / self.split / "images" / f"{label_file.stem}.jpg",
                'label_path': label_file
            })
    
    def __len__(self):
        return len(self.annotations)
    
    def __getitem__(self, idx):
        annotation = self.annotations[idx]
        
        # Load image (placeholder)
        image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
        
        # Load labels
        boxes = []
        if annotation['label_path'].exists():
            with open(annotation['label_path'], 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 5:
                        class_id, x, y, w, h = map(float, parts)
                        boxes.append([class_id, x, y, w, h])
        
        if self.transform:
            # Apply transforms
            pass
        
        return {
            'image': torch.from_numpy(image).permute(2, 0, 1).float() / 255.0,
            'boxes': torch.tensor(boxes) if boxes else torch.empty(0, 5)
        }

class MadagascarEcosystemDataset(Dataset):
    """Dataset for Madagascar ecosystem segmentation."""
    
    def __init__(self, data_dir: str, transform=None):
        self.data_dir = Path(data_dir)
        self.transform = transform
        self.load_metadata()
    
    def load_metadata(self):
        """Load ecosystem metadata."""
        metadata_file = self.data_dir / "metadata" / "ecosystem_metadata.json"
        with open(metadata_file, 'r') as f:
            self.metadata = json.load(f)
        
        self.ecosystem_classes = list(self.metadata['ecosystem_classes'].keys())
    
    def __len__(self):
        return self.metadata['dataset_info']['total_images']
    
    def __getitem__(self, idx):
        # Placeholder implementation
        image = np.random.randint(0, 255, (1024, 1024, 3), dtype=np.uint8)
        mask = np.random.randint(0, 12, (1024, 1024), dtype=np.uint8)
        
        return {
            'image': torch.from_numpy(image).permute(2, 0, 1).float() / 255.0,
            'mask': torch.from_numpy(mask).long()
        }

def get_madagascar_transforms(split: str = 'train'):
    """Get appropriate transforms for Madagascar datasets."""
    if split == 'train':
        return A.Compose([
            A.Resize(640, 640),
            A.HorizontalFlip(p=0.5),
            A.RandomBrightnessContrast(p=0.6),
            A.HueSaturationValue(p=0.6),
            A.ShiftScaleRotate(p=0.6),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    else:
        return A.Compose([
            A.Resize(640, 640),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
'''
        
        with open(utils_dir / "data_loaders.py", 'w') as f:
            f.write(data_loader_code)
        
        logger.info("✅ Data loading utilities created")
    
    def setup_phase2_step1(self) -> None:
        """Execute complete Step 1 setup for Phase 2."""
        logger.info("🌍 Phase 2 Step 1: Madagascar Dataset Preparation")
        logger.info("=" * 55)
        
        try:
            # Create directory structure
            self.create_directory_structure()
            
            # Create species subdirectories
            self.create_species_subdirectories()
            
            # Generate sample data and metadata
            self.generate_sample_data()
            
            # Create data loading utilities
            self.create_data_loading_utilities()
            
            logger.info("\n🎉 Step 1 Complete: Madagascar Dataset Preparation!")
            logger.info("=" * 50)
            logger.info("✅ Directory structure created")
            logger.info("✅ Species subdirectories organized")
            logger.info("✅ Sample data and metadata generated")
            logger.info("✅ Data loading utilities prepared")
            logger.info("\n📊 Dataset Summary:")
            logger.info(f"   🦅 Wildlife species: {len(self.madagascar_species['wildlife'])}")
            logger.info(f"   🌿 Ecosystem types: {len(self.madagascar_species['ecosystems'])}")
            logger.info(f"   🎯 Total expected samples: 53,000+")
            logger.info("\n🚀 Ready for Step 2: Model Training Pipeline Setup!")
            
        except Exception as e:
            logger.error(f"❌ Step 1 failed: {e}")
            raise

def main():
    """Main execution function."""
    # Initialize dataset preparer
    base_path = Path(__file__).parent.parent.parent
    preparer = MadagascarDatasetPreparer(base_path)
    
    # Execute Step 1
    preparer.setup_phase2_step1()

if __name__ == "__main__":
    main()
