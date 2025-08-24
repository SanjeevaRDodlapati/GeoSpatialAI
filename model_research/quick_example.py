"""
Quick Example: PRITHVI Earth Observation Analysis

This script demonstrates basic usage of the PRITHVI framework for
conservation area monitoring and change detection.
"""

import sys
from pathlib import Path

# Add the model_research directory to Python path
sys.path.append(str(Path(__file__).parent))

from models.prithvi import create_change_detection_model
from analysis.inference import create_inference_engine
from data.global_data import global_data_manager

def main():
    print("🌍 PRITHVI Earth Observation - Quick Example")
    print("=" * 50)
    
    # 1. Initialize the system
    print("1. Initializing PRITHVI model...")
    engine = create_inference_engine()
    
    model_info = engine.model.get_model_info()
    print(f"   Model: {model_info['model_name']}")
    print(f"   Parameters: {model_info['total_parameters']:,}")
    print(f"   Device: {engine.device}")
    print()
    
    # 2. Show available data
    print("2. Available conservation areas:")
    areas = list(global_data_manager.conservation_areas.keys())[:5]
    for i, area in enumerate(areas, 1):
        area_info = global_data_manager.get_conservation_area(area)
        print(f"   {i}. {area_info.name} ({area_info.country})")
    print(f"   ... and {len(global_data_manager.conservation_areas) - 5} more areas")
    print()
    
    # 3. Quick analysis example
    print("3. Running quick analysis on Masoala National Park...")
    results = engine.analyze_conservation_area("masoala_np", num_samples=5)
    
    # Display results
    analysis = results['analysis_results']
    print(f"   Area: {results['area_name']}")
    print(f"   Change detected: {analysis['change_detected_samples']}/{results['num_samples']} samples")
    print(f"   Change rate: {analysis['change_detection_rate']:.1%}")
    print(f"   Average confidence: {analysis['average_confidence']:.3f}")
    print(f"   Analysis time: {results['total_analysis_time_ms']:.1f}ms")
    print()
    
    # 4. Performance stats
    print("4. Performance statistics:")
    stats = engine.get_performance_stats()
    print(f"   Total inferences: {stats['total_inferences']}")
    print(f"   Average time: {stats['average_inference_time_ms']:.1f}ms")
    print(f"   Throughput: {stats['throughput_per_second']:.1f} images/sec")
    print()
    
    # 5. Global summary
    print("5. Global data summary:")
    summary = global_data_manager.get_summary_statistics()
    print(f"   Conservation areas: {summary['total_conservation_areas']}")
    print(f"   Total protected area: {summary['total_protected_area_km2']:,.0f} km²")
    print(f"   Satellite sources: {summary['satellite_sources']}")
    print()
    
    print("✅ Quick example completed successfully!")
    print("\nNext steps:")
    print("• Run full analysis: python main_prithvi_analysis.py --analyze masoala_np")
    print("• Global analysis: python main_prithvi_analysis.py --global")
    print("• List all areas: python main_prithvi_analysis.py --list-areas")

if __name__ == "__main__":
    main()
