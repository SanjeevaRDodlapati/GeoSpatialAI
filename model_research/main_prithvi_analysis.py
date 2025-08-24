"""
Main PRITHVI Analysis Application
Command-line interface for Earth observation analysis using PRITHVI models.
"""

import argparse
import logging
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add the model_research directory to Python path
sys.path.append(str(Path(__file__).parent))

from models.prithvi import create_change_detection_model, create_land_cover_model
from analysis.inference import InferenceEngine, create_inference_engine
from data.global_data import GlobalDataManager, global_data_manager
from visualization.plots import create_analysis_plots, save_performance_plot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PRITHVIAnalysisApp:
    """
    Main application class for PRITHVI Earth observation analysis.
    """
    
    def __init__(self):
        self.data_manager = global_data_manager
        self.inference_engine: Optional[InferenceEngine] = None
        self.results_dir = Path("outputs")
        self.results_dir.mkdir(exist_ok=True)
        
    def setup_model(self, model_type: str = "change_detection", device: str = "auto"):
        """Setup the PRITHVI model and inference engine."""
        logger.info(f"Setting up {model_type} model on {device}")
        
        if model_type == "change_detection":
            model = create_change_detection_model()
        elif model_type == "land_cover":
            model = create_land_cover_model()
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        self.inference_engine = InferenceEngine(model, device)
        logger.info(f"Model loaded with {model.get_parameter_count():,} parameters")
        
    def list_available_areas(self):
        """List all available conservation areas."""
        print("\nAvailable Conservation Areas:")
        print("=" * 50)
        
        areas = self.data_manager.conservation_areas
        for i, (key, area) in enumerate(areas.items(), 1):
            print(f"{i:2d}. {area.name}")
            print(f"    Country: {area.country}")
            print(f"    Ecosystem: {area.ecosystem_type}")
            print(f"    Area: {area.area_km2:,.0f} km²")
            print(f"    Key: {key}")
            print()
    
    def list_satellite_sources(self):
        """List all available satellite sources."""
        print("\nAvailable Satellite Sources:")
        print("=" * 40)
        
        sources = self.data_manager.satellite_sources
        for i, (key, source) in enumerate(sources.items(), 1):
            print(f"{i}. {source.name}")
            print(f"   Resolution: {source.resolution_m}m")
            print(f"   Revisit: {source.temporal_resolution_days} days")
            print(f"   Bands: {len(source.bands)}")
            print(f"   Key: {key}")
            print()
    
    def analyze_area(self, area_name: str, satellite_source: str = "sentinel2", 
                    num_samples: int = 10, save_results: bool = True):
        """Analyze a specific conservation area."""
        if not self.inference_engine:
            self.setup_model()
        
        logger.info(f"Starting analysis of {area_name}")
        
        try:
            # Run analysis
            results = self.inference_engine.analyze_conservation_area(
                area_name, satellite_source, num_samples
            )
            
            # Display results
            self._display_analysis_results(results)
            
            # Save results if requested
            if save_results:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"analysis_{area_name}_{timestamp}.json"
                filepath = self.results_dir / filename
                
                with open(filepath, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                
                logger.info(f"Results saved to {filepath}")
            
            return results
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return None
    
    def _display_analysis_results(self, results):
        """Display analysis results in a formatted way."""
        print(f"\n🌍 Analysis Results: {results['area_name']}")
        print("=" * 60)
        print(f"Country: {results['country']}")
        print(f"Ecosystem: {results['ecosystem_type']}")
        print(f"Satellite Source: {results['satellite_source']}")
        print(f"Samples Analyzed: {results['num_samples']}")
        print(f"Analysis Time: {results['total_analysis_time_ms']:.1f}ms")
        print()
        
        analysis = results['analysis_results']
        print("📊 Detection Results:")
        print(f"  Change Detected: {analysis['change_detected_samples']}/{results['num_samples']} samples")
        print(f"  Change Rate: {analysis['change_detection_rate']:.1%}")
        print(f"  Average Confidence: {analysis['average_confidence']:.3f}")
        print(f"  Confidence Range: {analysis['min_confidence']:.3f} - {analysis['max_confidence']:.3f}")
        print()
        
        if analysis['change_detection_rate'] > 0.3:
            print("⚠️  HIGH CHANGE ACTIVITY DETECTED - Requires attention!")
        elif analysis['change_detection_rate'] > 0.1:
            print("⚡ Moderate change activity detected")
        else:
            print("✅ Low change activity - Area appears stable")
        print()
    
    def run_global_analysis(self, num_samples: int = 5):
        """Run analysis on all priority conservation areas."""
        if not self.inference_engine:
            self.setup_model()
        
        logger.info("Starting global conservation analysis")
        
        priority_queue = self.data_manager.get_priority_analysis_queue()
        global_results = []
        
        print(f"\n🌎 Global Conservation Analysis")
        print("=" * 50)
        
        for i, (area_name, satellite_source, analysis_type) in enumerate(priority_queue, 1):
            print(f"\n[{i}/{len(priority_queue)}] Analyzing {area_name}...")
            
            try:
                results = self.inference_engine.analyze_conservation_area(
                    area_name, satellite_source, num_samples
                )
                results['analysis_type'] = analysis_type
                global_results.append(results)
                
                # Quick summary
                change_rate = results['analysis_results']['change_detection_rate']
                print(f"  Change Rate: {change_rate:.1%} ({'⚠️ HIGH' if change_rate > 0.3 else '✅ OK'})")
                
            except Exception as e:
                logger.error(f"Failed to analyze {area_name}: {e}")
                continue
        
        # Save global results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"global_analysis_{timestamp}.json"
        filepath = self.results_dir / filename
        
        global_summary = {
            "global_analysis_results": global_results,
            "summary_statistics": self._calculate_global_summary(global_results),
            "performance_stats": self.inference_engine.get_performance_stats(),
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(global_summary, f, indent=2, default=str)
        
        # Display global summary
        self._display_global_summary(global_summary)
        
        logger.info(f"Global analysis complete. Results saved to {filepath}")
        return global_summary
    
    def _calculate_global_summary(self, results):
        """Calculate summary statistics for global analysis."""
        if not results:
            return {}
        
        change_rates = [r['analysis_results']['change_detection_rate'] for r in results]
        confidences = [r['analysis_results']['average_confidence'] for r in results]
        
        high_change_areas = [r for r in results if r['analysis_results']['change_detection_rate'] > 0.3]
        
        return {
            "total_areas_analyzed": len(results),
            "average_change_rate": sum(change_rates) / len(change_rates),
            "high_change_areas": len(high_change_areas),
            "high_change_area_names": [r['area_name'] for r in high_change_areas],
            "average_confidence": sum(confidences) / len(confidences),
            "ecosystems_analyzed": list(set(r['ecosystem_type'] for r in results))
        }
    
    def _display_global_summary(self, summary):
        """Display global analysis summary."""
        stats = summary['summary_statistics']
        perf = summary['performance_stats']
        
        print(f"\n🌍 Global Analysis Summary")
        print("=" * 40)
        print(f"Areas Analyzed: {stats['total_areas_analyzed']}")
        print(f"Average Change Rate: {stats['average_change_rate']:.1%}")
        print(f"High Change Areas: {stats['high_change_areas']}")
        print(f"Average Confidence: {stats['average_confidence']:.3f}")
        print()
        
        if stats['high_change_areas'] > 0:
            print("⚠️  Areas requiring immediate attention:")
            for area in stats['high_change_area_names']:
                print(f"  • {area}")
            print()
        
        print(f"📈 Performance Statistics:")
        print(f"  Total Inferences: {perf['total_inferences']}")
        print(f"  Average Time: {perf['average_inference_time_ms']:.1f}ms")
        print(f"  Throughput: {perf['throughput_per_second']:.1f} images/sec")
        print(f"  Device: {perf['device']}")
        print()
    
    def show_performance_stats(self):
        """Show detailed performance statistics."""
        if not self.inference_engine:
            print("No inference engine loaded. Run an analysis first.")
            return
        
        stats = self.inference_engine.get_performance_stats()
        
        print("\n📊 Performance Statistics")
        print("=" * 30)
        print(f"Total Inferences: {stats['total_inferences']}")
        print(f"Total Time: {stats['total_time_ms']:.1f}ms")
        print(f"Average Time: {stats['average_inference_time_ms']:.1f}ms")
        print(f"Throughput: {stats['throughput_per_second']:.1f} images/sec")
        print(f"Device: {stats['device']}")
        print(f"Model Parameters: {stats['model_parameters']:,}")
        print()
        
        if stats['total_inferences'] > 0:
            print(f"Recent Performance (last 100 inferences):")
            print(f"  Average: {stats['recent_average_ms']:.1f}ms")
            print(f"  Range: {stats['recent_min_ms']:.1f} - {stats['recent_max_ms']:.1f}ms")

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="PRITHVI Earth Observation Analysis")
    parser.add_argument("--list-areas", action="store_true", help="List available conservation areas")
    parser.add_argument("--list-sources", action="store_true", help="List available satellite sources")
    parser.add_argument("--analyze", type=str, help="Analyze specific conservation area")
    parser.add_argument("--source", type=str, default="sentinel2", help="Satellite source to use")
    parser.add_argument("--samples", type=int, default=10, help="Number of samples to analyze")
    parser.add_argument("--global", action="store_true", help="Run global analysis on all priority areas")
    parser.add_argument("--model", type=str, default="change_detection", 
                       choices=["change_detection", "land_cover"], help="Model type to use")
    parser.add_argument("--device", type=str, default="auto", help="Device to use (auto, cpu, cuda, mps)")
    parser.add_argument("--stats", action="store_true", help="Show performance statistics")
    
    args = parser.parse_args()
    
    # Create application instance
    app = PRITHVIAnalysisApp()
    
    try:
        if args.list_areas:
            app.list_available_areas()
        elif args.list_sources:
            app.list_satellite_sources()
        elif args.analyze:
            app.setup_model(args.model, args.device)
            app.analyze_area(args.analyze, args.source, args.samples)
            app.show_performance_stats()
        elif getattr(args, 'global'):  # 'global' is a reserved keyword
            app.setup_model(args.model, args.device)
            app.run_global_analysis(args.samples)
        elif args.stats:
            app.show_performance_stats()
        else:
            # Interactive mode
            print("🌍 PRITHVI Earth Observation Analysis System")
            print("=" * 50)
            print("Available commands:")
            print("  --list-areas     : List conservation areas")
            print("  --list-sources   : List satellite sources")
            print("  --analyze AREA   : Analyze specific area")
            print("  --global         : Run global analysis")
            print("  --stats          : Show performance stats")
            print()
            print("Example: python main_prithvi_analysis.py --analyze masoala_np --samples 20")
            print("Example: python main_prithvi_analysis.py --global --samples 5")
            
    except KeyboardInterrupt:
        logger.info("Analysis interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
