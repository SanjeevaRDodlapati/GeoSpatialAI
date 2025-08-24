"""
Visualization and Plotting Utilities for PRITHVI Analysis
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from typing import Dict, List, Any, Optional
import pandas as pd
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_analysis_plots(results: Dict[str, Any], output_dir: str = "outputs/figures") -> None:
    """
    Create comprehensive plots for analysis results.
    
    Args:
        results: Analysis results dictionary
        output_dir: Directory to save plots
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    
    # Extract data
    individual_results = results.get('individual_results', [])
    if not individual_results:
        return
    
    confidences = [r['confidence'] for r in individual_results]
    predictions = [r['prediction'] for r in individual_results]
    inference_times = [r['inference_time_ms'] for r in individual_results]
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f"Analysis Results: {results['area_name']}", fontsize=16, fontweight='bold')
    
    # 1. Confidence distribution
    axes[0, 0].hist(confidences, bins=10, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Confidence Distribution')
    axes[0, 0].set_xlabel('Confidence Score')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].axvline(np.mean(confidences), color='red', linestyle='--', label=f'Mean: {np.mean(confidences):.3f}')
    axes[0, 0].legend()
    
    # 2. Prediction summary
    pred_counts = [predictions.count(0), predictions.count(1)]
    labels = ['No Change', 'Change Detected']
    colors = ['lightgreen', 'orange']
    axes[0, 1].pie(pred_counts, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    axes[0, 1].set_title('Change Detection Summary')
    
    # 3. Inference time distribution
    axes[1, 0].hist(inference_times, bins=10, alpha=0.7, color='lightcoral', edgecolor='black')
    axes[1, 0].set_title('Inference Time Distribution')
    axes[1, 0].set_xlabel('Time (ms)')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].axvline(np.mean(inference_times), color='blue', linestyle='--', 
                       label=f'Mean: {np.mean(inference_times):.1f}ms')
    axes[1, 0].legend()
    
    # 4. Confidence vs Time scatter
    colors_scatter = ['green' if p == 0 else 'red' for p in predictions]
    axes[1, 1].scatter(inference_times, confidences, c=colors_scatter, alpha=0.6)
    axes[1, 1].set_title('Confidence vs Inference Time')
    axes[1, 1].set_xlabel('Inference Time (ms)')
    axes[1, 1].set_ylabel('Confidence Score')
    
    # Add legend for scatter plot
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='green', label='No Change'),
                      Patch(facecolor='red', label='Change Detected')]
    axes[1, 1].legend(handles=legend_elements)
    
    plt.tight_layout()
    
    # Save plot
    area_name = results['area_name'].replace(' ', '_').lower()
    filename = f"analysis_{area_name}.png"
    plt.savefig(output_path / filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Analysis plots saved to {output_path / filename}")

def save_performance_plot(performance_stats: Dict[str, Any], output_dir: str = "outputs/figures") -> None:
    """
    Create performance visualization plots.
    
    Args:
        performance_stats: Performance statistics dictionary
        output_dir: Directory to save plots
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    
    # Create performance summary plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('PRITHVI Model Performance Statistics', fontsize=16, fontweight='bold')
    
    # Performance metrics
    metrics = ['Avg Time (ms)', 'Throughput (img/s)', 'Total Inferences']
    values = [
        performance_stats.get('average_inference_time_ms', 0),
        performance_stats.get('throughput_per_second', 0),
        performance_stats.get('total_inferences', 0)
    ]
    
    # Bar plot of key metrics
    bars = axes[0].bar(metrics[:2], values[:2], color=['lightblue', 'lightgreen'])
    axes[0].set_title('Performance Metrics')
    axes[0].set_ylabel('Value')
    
    # Add value labels on bars
    for bar, value in zip(bars, values[:2]):
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{value:.1f}', ha='center', va='bottom')
    
    # Device and model info
    device = performance_stats.get('device', 'Unknown')
    total_inferences = performance_stats.get('total_inferences', 0)
    model_params = performance_stats.get('model_parameters', 0)
    
    info_text = f"""Model Information:
    Device: {device}
    Parameters: {model_params:,}
    Total Inferences: {total_inferences}
    
    Recent Performance:
    Min: {performance_stats.get('recent_min_ms', 0):.1f}ms
    Max: {performance_stats.get('recent_max_ms', 0):.1f}ms
    Avg: {performance_stats.get('recent_average_ms', 0):.1f}ms"""
    
    axes[1].text(0.05, 0.95, info_text, transform=axes[1].transAxes, 
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    axes[1].set_xlim(0, 1)
    axes[1].set_ylim(0, 1)
    axes[1].axis('off')
    axes[1].set_title('System Information')
    
    plt.tight_layout()
    
    # Save plot
    filename = "performance_stats.png"
    plt.savefig(output_path / filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Performance plot saved to {output_path / filename}")

def create_global_summary_plot(global_results: List[Dict[str, Any]], output_dir: str = "outputs/figures") -> None:
    """
    Create global analysis summary plots.
    
    Args:
        global_results: List of analysis results for multiple areas
        output_dir: Directory to save plots
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    
    if not global_results:
        return
    
    # Extract data
    area_names = [r['area_name'] for r in global_results]
    change_rates = [r['analysis_results']['change_detection_rate'] for r in global_results]
    confidences = [r['analysis_results']['average_confidence'] for r in global_results]
    ecosystems = [r['ecosystem_type'] for r in global_results]
    
    # Create comprehensive global plot
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Global Conservation Area Analysis Summary', fontsize=16, fontweight='bold')
    
    # 1. Change detection rates by area
    colors = ['red' if rate > 0.3 else 'orange' if rate > 0.1 else 'green' for rate in change_rates]
    bars = axes[0, 0].bar(range(len(area_names)), change_rates, color=colors)
    axes[0, 0].set_title('Change Detection Rates by Area')
    axes[0, 0].set_ylabel('Change Detection Rate')
    axes[0, 0].set_xticks(range(len(area_names)))
    axes[0, 0].set_xticklabels([name[:15] + '...' if len(name) > 15 else name for name in area_names], 
                               rotation=45, ha='right')
    
    # Add threshold lines
    axes[0, 0].axhline(y=0.3, color='red', linestyle='--', alpha=0.7, label='High Alert (30%)')
    axes[0, 0].axhline(y=0.1, color='orange', linestyle='--', alpha=0.7, label='Moderate (10%)')
    axes[0, 0].legend()
    
    # 2. Ecosystem type distribution
    ecosystem_counts = pd.Series(ecosystems).value_counts()
    axes[0, 1].pie(ecosystem_counts.values, labels=ecosystem_counts.index, autopct='%1.1f%%', startangle=90)
    axes[0, 1].set_title('Ecosystem Type Distribution')
    
    # 3. Change rate vs confidence scatter
    scatter_colors = ['red' if rate > 0.3 else 'orange' if rate > 0.1 else 'green' for rate in change_rates]
    axes[1, 0].scatter(confidences, change_rates, c=scatter_colors, s=100, alpha=0.7)
    axes[1, 0].set_xlabel('Average Confidence')
    axes[1, 0].set_ylabel('Change Detection Rate')
    axes[1, 0].set_title('Confidence vs Change Rate')
    
    # Add threshold lines
    axes[1, 0].axhline(y=0.3, color='red', linestyle='--', alpha=0.5)
    axes[1, 0].axhline(y=0.1, color='orange', linestyle='--', alpha=0.5)
    
    # 4. Summary statistics
    high_change_count = sum(1 for rate in change_rates if rate > 0.3)
    moderate_change_count = sum(1 for rate in change_rates if 0.1 < rate <= 0.3)
    stable_count = sum(1 for rate in change_rates if rate <= 0.1)
    
    summary_text = f"""Global Analysis Summary:
    
Total Areas: {len(global_results)}
Average Change Rate: {np.mean(change_rates):.1%}
Average Confidence: {np.mean(confidences):.3f}

Alert Levels:
🔴 High Alert (>30%): {high_change_count} areas
🟡 Moderate (10-30%): {moderate_change_count} areas  
🟢 Stable (<10%): {stable_count} areas

Ecosystem Coverage:
{chr(10).join([f'• {eco}: {count} areas' for eco, count in ecosystem_counts.head().items()])}"""
    
    axes[1, 1].text(0.05, 0.95, summary_text, transform=axes[1, 1].transAxes,
                   verticalalignment='top', fontfamily='monospace',
                   bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    axes[1, 1].set_xlim(0, 1)
    axes[1, 1].set_ylim(0, 1)
    axes[1, 1].axis('off')
    axes[1, 1].set_title('Summary Statistics')
    
    plt.tight_layout()
    
    # Save plot
    filename = "global_analysis_summary.png"
    plt.savefig(output_path / filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Global summary plot saved to {output_path / filename}")

# Convenience functions
def quick_plot(results: Dict[str, Any]) -> None:
    """Quick plotting function for analysis results."""
    create_analysis_plots(results)

def plot_performance(engine) -> None:
    """Quick performance plotting."""
    stats = engine.get_performance_stats()
    save_performance_plot(stats)

if __name__ == "__main__":
    # Example usage
    print("Visualization utilities for PRITHVI analysis")
    print("Use create_analysis_plots() and save_performance_plot() functions")
