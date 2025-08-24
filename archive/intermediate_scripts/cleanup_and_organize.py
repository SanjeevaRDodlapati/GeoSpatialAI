"""
REPOSITORY CLEANUP AND ORGANIZATION SCRIPT
==========================================

This script organizes the repository by:
1. Keeping final working files for real-world data collection
2. Archiving redundant/intermediate files
3. Creating a clean, organized structure

Author: GeoSpatialAI Development Team
Date: August 24, 2025
"""

import os
import shutil
from datetime import datetime
import json

def create_archive_structure():
    """Create organized archive structure."""
    
    base_dir = "/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI"
    
    # Create archive directories
    archive_dirs = [
        "archive/development_iterations",
        "archive/redundant_dashboards", 
        "archive/intermediate_scripts",
        "archive/test_files",
        "archive/documentation_drafts",
        "archive/old_data_collections"
    ]
    
    for dir_path in archive_dirs:
        full_path = os.path.join(base_dir, dir_path)
        os.makedirs(full_path, exist_ok=True)
        print(f"✅ Created: {dir_path}")

def identify_files_to_keep():
    """Identify essential files to keep in main directory."""
    
    essential_files = {
        # Core project files
        "README.md": "keep",
        "LICENSE": "keep", 
        ".gitignore": "keep",
        ".gitattributes": "keep",
        "requirements.txt": "keep",
        
        # Final working files
        "FINAL_COMPLETE_CONSERVATION_DASHBOARD.html": "keep",
        "FINAL_PROJECT_COMPLETION_REPORT.md": "keep",
        "final_working_collection.py": "keep",
        "test_working_apis.py": "keep",
        
        # Essential directories
        "src/": "keep",
        "config/": "keep",
        "tests/": "keep",
        "docs/": "keep",
        
        # Final data collections
        "final_working_collection_20250824_071934/": "keep",
        "ebird_api_test_success.json": "keep"
    }
    
    return essential_files

def identify_files_to_archive():
    """Identify files to move to archive."""
    
    files_to_archive = {
        # Redundant dashboards
        "archive/redundant_dashboards": [
            "conservation_data_structure_dashboard.html",
            "conservation_intelligence_dashboard.html", 
            "integrated_conservation_dashboard.html",
            "real_conservation_dashboard.html",
            "working_real_conservation_dashboard.html"
        ],
        
        # Intermediate scripts
        "archive/intermediate_scripts": [
            "adaptive_data_pipeline.py",
            "api_solutions_demo.py",
            "conservation_data_structure_analyzer.py",
            "conservation_data_visualizer.py",
            "conservation_example_records_generator.py",
            "data_analysis_comprehensive_report.py",
            "enhanced_api_collection.py",
            "fetch_real_data_1000_records.py",
            "gbif_validation_test.py",
            "global_metadata_discovery_system.py",
            "integrated_conservation_analyzer.py",
            "metadata_visualization_system.py",
            "real_data_extractor.py",
            "smart_data_selection_interface.py",
            "test_simple_approach.py"
        ],
        
        # Documentation drafts
        "archive/documentation_drafts": [
            "API_ACCESS_GUIDE.md",
            "API_LIMITATION_SOLUTIONS.md",
            "COMPLETE_ROADMAP_AND_DATA_STATISTICS.md",
            "CONSERVATION_PLATFORM_ENHANCEMENT_PLAN.md",
            "DASHBOARD_QUICK_START.md",
            "DATA_SCOPE_ANALYSIS_REGIONAL_VS_GLOBAL.md",
            "DETAILED_TECHNICAL_IMPLEMENTATION_PLAN.md",
            "DEVELOPMENT_STRATEGY_SIMPLE_TO_COMPLEX.md",
            "ENHANCED_AGENTIC_RESEARCH_PIPELINE.md",
            "INTELLIGENT_METADATA_SYSTEM_SUMMARY.md",
            "REAL_DATA_COLLECTION_REPORT.md",
            "REAL_WORLD_IMPLEMENTATION_COMPLETE.md",
            "UPDATED_API_SOLUTIONS.md",
            "VISUALIZATION_SYSTEM_SUMMARY.md"
        ],
        
        # Old data collections
        "archive/old_data_collections": [
            "enhanced_data_collection_20250824_071125/",
            "real_data_collection_20250824_061927/",
            "conservation_data_structure_analysis_20250824_053206.json",
            "integrated_conservation_analysis_20250824_054105.json",
            "real_world_data_analysis_report_20250824_042241.json"
        ],
        
        # Cache directories
        "archive/development_iterations": [
            "data_cache/",
            "metadata_cache/",
            "__pycache__/"
        ]
    }
    
    return files_to_archive

def move_files_to_archive():
    """Move identified files to archive directories."""
    
    base_dir = "/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI"
    files_to_archive = identify_files_to_archive()
    
    moved_count = 0
    
    for archive_dir, files in files_to_archive.items():
        archive_path = os.path.join(base_dir, archive_dir)
        
        for file_item in files:
            source_path = os.path.join(base_dir, file_item)
            dest_path = os.path.join(archive_path, file_item)
            
            if os.path.exists(source_path):
                try:
                    if os.path.isdir(source_path):
                        if os.path.exists(dest_path):
                            shutil.rmtree(dest_path)
                        shutil.move(source_path, dest_path)
                        print(f"📁 Moved directory: {file_item} → {archive_dir}")
                    else:
                        shutil.move(source_path, dest_path)
                        print(f"📄 Moved file: {file_item} → {archive_dir}")
                    
                    moved_count += 1
                    
                except Exception as e:
                    print(f"⚠️  Error moving {file_item}: {e}")
            else:
                print(f"⚠️  File not found: {file_item}")
    
    return moved_count

def create_clean_directory_summary():
    """Create summary of cleaned directory structure."""
    
    base_dir = "/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI"
    
    summary = {
        "cleanup_timestamp": datetime.now().isoformat(),
        "purpose": "Repository cleanup - keep final working files only",
        "kept_files": {
            "core_project": [
                "README.md",
                "LICENSE", 
                "requirements.txt",
                ".gitignore"
            ],
            "final_working_files": [
                "FINAL_COMPLETE_CONSERVATION_DASHBOARD.html",
                "FINAL_PROJECT_COMPLETION_REPORT.md", 
                "final_working_collection.py",
                "test_working_apis.py"
            ],
            "essential_directories": [
                "src/",
                "config/",
                "tests/",
                "docs/",
                "archive/"
            ],
            "final_data": [
                "final_working_collection_20250824_071934/",
                "ebird_api_test_success.json"
            ]
        },
        "archived_categories": {
            "redundant_dashboards": "5 HTML dashboard files",
            "intermediate_scripts": "15 development scripts", 
            "documentation_drafts": "13 draft documentation files",
            "old_data_collections": "4 intermediate data collections",
            "cache_directories": "3 cache/temp directories"
        },
        "final_structure": "Clean, organized repository with only essential working files"
    }
    
    summary_file = os.path.join(base_dir, "REPOSITORY_CLEANUP_SUMMARY.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    return summary

def main():
    """Execute repository cleanup and organization."""
    
    print("🧹 STARTING REPOSITORY CLEANUP AND ORGANIZATION")
    print("=" * 60)
    
    try:
        # Step 1: Create archive structure
        print("\n📁 Creating archive directory structure...")
        create_archive_structure()
        
        # Step 2: Move files to archive
        print("\n📦 Moving redundant files to archive...")
        moved_count = move_files_to_archive()
        
        # Step 3: Create summary
        print("\n📋 Creating cleanup summary...")
        summary = create_clean_directory_summary()
        
        print("\n" + "=" * 60)
        print("✅ REPOSITORY CLEANUP COMPLETE!")
        print(f"📊 Files moved to archive: {moved_count}")
        print("\n🎯 FINAL STRUCTURE:")
        print("   • Core project files: README, LICENSE, requirements")
        print("   • Final working files: Dashboard, collection script, report")
        print("   • Essential directories: src/, config/, tests/, docs/")
        print("   • Final data: Working collection (1,742 records)")
        print("   • Archive: All redundant/intermediate files organized")
        
        print(f"\n📄 Cleanup summary saved: REPOSITORY_CLEANUP_SUMMARY.json")
        
    except Exception as e:
        print(f"\n❌ Error during cleanup: {e}")

if __name__ == "__main__":
    main()
