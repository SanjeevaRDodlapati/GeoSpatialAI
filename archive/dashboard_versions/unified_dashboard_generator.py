"""
Unified Conservation Data Dashboard
==================================

Single entry point dashboard with tabbed navigation for all conservation
data visualizations and analysis tools.

Author: GeoSpatialAI Development Team
Date: August 24, 2025
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import json
import numpy as np
from datetime import datetime
from pathlib import Path
import logging

# Import our existing visualization classes
from conservation_data_visualizer import ConservationDataVisualizer
from metadata_visualization_system import MetadataVisualizationSystem

logger = logging.getLogger(__name__)

class UnifiedDashboardGenerator:
    """
    Creates a unified dashboard with tabbed navigation for all conservation
    data visualizations and analysis tools.
    """
    
    def __init__(self):
        self.conservation_viz = ConservationDataVisualizer()
        self.metadata_viz = MetadataVisualizationSystem()
        
        # Dashboard configuration
        self.dashboard_config = {
            "title": "🌍 Global Conservation Data Intelligence Platform",
            "subtitle": "Comprehensive analysis and visualization of worldwide biodiversity databases",
            "tabs": self._define_dashboard_tabs(),
            "theme": self._define_dashboard_theme()
        }
    
    def _define_dashboard_tabs(self):
        """Define the structure and content of dashboard tabs."""
        return [
            {
                "id": "overview",
                "title": "📊 Global Overview",
                "icon": "🌍",
                "description": "Global database statistics and key metrics",
                "visualizations": [
                    {"type": "global_metrics_cards", "title": "Key Metrics"},
                    {"type": "database_overview", "title": "Database Comparison"},
                    {"type": "country_coverage_map", "title": "Global Data Coverage"}
                ]
            },
            {
                "id": "metadata",
                "title": "🔍 Metadata Intelligence",
                "icon": "🧠",
                "description": "Database capabilities and intelligent selection analysis",
                "visualizations": [
                    {"type": "capabilities_matrix", "title": "Database Capabilities Matrix"},
                    {"type": "selection_workflow", "title": "Intelligent Selection Workflow"},
                    {"type": "coverage_quality", "title": "Coverage vs Quality Analysis"}
                ]
            },
            {
                "id": "conservation",
                "title": "🏞️ Conservation Areas",
                "icon": "🌳",
                "description": "Real-world conservation area analysis and performance",
                "visualizations": [
                    {"type": "conservation_analysis", "title": "Conservation Areas Performance"},
                    {"type": "taxonomic_diversity", "title": "Taxonomic Diversity Analysis"},
                    {"type": "temporal_trends", "title": "Temporal Coverage Trends"}
                ]
            },
            {
                "id": "research",
                "title": "🎯 Research Strategies",
                "icon": "🔬",
                "description": "Research strategy comparison and recommendations",
                "visualizations": [
                    {"type": "strategy_comparison", "title": "Research Strategy Comparison"},
                    {"type": "recommendations", "title": "Research Recommendations"},
                    {"type": "quality_assessment", "title": "Data Quality Assessment"}
                ]
            },
            {
                "id": "interactive",
                "title": "🎮 Interactive Tools",
                "icon": "⚡",
                "description": "Interactive selection wizard and real-time analysis",
                "visualizations": [
                    {"type": "selection_wizard", "title": "Smart Data Selection Wizard"},
                    {"type": "parameter_optimizer", "title": "Parameter Optimization Tool"},
                    {"type": "real_time_monitor", "title": "Real-time Data Monitor"}
                ]
            }
        ]
    
    def _define_dashboard_theme(self):
        """Define the visual theme and styling for the dashboard."""
        return {
            "primary_color": "#2E8B57",      # Sea Green
            "secondary_color": "#4682B4",    # Steel Blue
            "accent_color": "#FF6347",       # Tomato
            "success_color": "#32CD32",      # Lime Green
            "warning_color": "#FFD700",      # Gold
            "background_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "card_background": "white",
            "text_primary": "#2c3e50",
            "text_secondary": "#7f8c8d"
        }
    
    def generate_unified_dashboard(self) -> str:
        """Generate the complete unified dashboard with tabbed navigation."""
        
        logger.info("🎨 Generating unified conservation data dashboard...")
        
        # Get all visualizations
        all_visualizations = self._generate_all_visualizations()
        
        # Load metadata for metrics
        metadata = self.metadata_viz.metadata
        
        # Generate HTML structure
        html_content = self._create_html_structure(all_visualizations, metadata)
        
        # Save dashboard
        dashboard_file = Path("unified_conservation_dashboard.html")
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"✅ Unified dashboard saved to: {dashboard_file}")
        return str(dashboard_file)
    
    def _generate_all_visualizations(self):
        """Generate all visualizations for the dashboard."""
        
        logger.info("📊 Generating all visualizations...")
        
        visualizations = {}
        
        try:
            # Conservation visualizations
            visualizations["database_overview"] = self.conservation_viz.create_global_database_overview()
            visualizations["country_coverage_map"] = self.conservation_viz.create_country_coverage_map()
            visualizations["taxonomic_diversity"] = self.conservation_viz.create_taxonomic_diversity_analysis()
            visualizations["conservation_analysis"] = self.conservation_viz.create_conservation_areas_analysis()
            visualizations["temporal_trends"] = self.conservation_viz.create_temporal_trends_analysis()
            visualizations["quality_assessment"] = self.conservation_viz.create_data_quality_assessment()
            visualizations["recommendations"] = self.conservation_viz.create_research_recommendations_dashboard()
            
            # Metadata visualizations
            visualizations["capabilities_matrix"] = self.metadata_viz.create_database_capabilities_matrix()
            visualizations["selection_workflow"] = self.metadata_viz.create_intelligent_selection_workflow()
            visualizations["coverage_quality"] = self.metadata_viz.create_coverage_vs_quality_analysis()
            visualizations["strategy_comparison"] = self.metadata_viz.create_research_strategy_comparison()
            
            logger.info(f"✅ Generated {len(visualizations)} visualizations")
            
        except Exception as e:
            logger.error(f"⚠️ Some visualizations may not be available: {e}")
        
        return visualizations
    
    def _create_html_structure(self, visualizations, metadata):
        """Create the complete HTML structure with tabbed navigation."""
        
        theme = self.dashboard_config["theme"]
        tabs = self.dashboard_config["tabs"]
        
        # Extract key metrics
        gbif_stats = metadata.get("databases", {}).get("gbif", {}).get("global_statistics", {})
        inaturalist_stats = metadata.get("databases", {}).get("inaturalist", {}).get("global_statistics", {})
        
        total_records = gbif_stats.get("total_occurrences", 3244938434)
        inaturalist_obs = inaturalist_stats.get("total_observations", 268746290)
        countries_covered = metadata.get("databases", {}).get("gbif", {}).get("country_coverage", {}).get("total_countries", 252)
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.dashboard_config["title"]}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <style>
        /* Global Styles */
        :root {{
            --primary-color: {theme["primary_color"]};
            --secondary-color: {theme["secondary_color"]};
            --accent-color: {theme["accent_color"]};
            --success-color: {theme["success_color"]};
            --warning-color: {theme["warning_color"]};
            --text-primary: {theme["text_primary"]};
            --text-secondary: {theme["text_secondary"]};
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: {theme["background_gradient"]};
            margin: 0;
            padding: 0;
            min-height: 100vh;
        }}
        
        /* Header Styles */
        .dashboard-header {{
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 20px 0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }}
        
        .dashboard-header::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 4s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 0.5; }}
            50% {{ transform: scale(1.1); opacity: 0.8; }}
        }}
        
        .header-content {{
            position: relative;
            z-index: 2;
            text-align: center;
        }}
        
        .header-title {{
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header-subtitle {{
            font-size: 1.1rem;
            opacity: 0.9;
            margin-bottom: 0;
        }}
        
        .header-timestamp {{
            font-size: 0.9rem;
            opacity: 0.7;
            margin-top: 10px;
        }}
        
        /* Metrics Cards */
        .metrics-section {{
            padding: 30px 0;
            background: rgba(255,255,255,0.1);
        }}
        
        .metric-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            height: 100%;
            border-left: 5px solid var(--primary-color);
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }}
        
        .metric-value {{
            font-size: 2.5rem;
            font-weight: bold;
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }}
        
        .metric-label {{
            color: var(--text-secondary);
            font-size: 0.95rem;
            font-weight: 500;
        }}
        
        .metric-icon {{
            font-size: 1.5rem;
            color: var(--primary-color);
            margin-bottom: 15px;
        }}
        
        /* Tab Navigation */
        .nav-tabs-container {{
            background: white;
            border-radius: 15px 15px 0 0;
            margin: 20px;
            margin-bottom: 0;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .nav-tabs {{
            border-bottom: none;
            background: #f8f9fa;
            padding: 0;
        }}
        
        .nav-tabs .nav-link {{
            border: none;
            border-radius: 0;
            padding: 20px 30px;
            color: var(--text-primary);
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
            background: transparent;
        }}
        
        .nav-tabs .nav-link:hover {{
            background: rgba(46, 139, 87, 0.1);
            color: var(--primary-color);
        }}
        
        .nav-tabs .nav-link.active {{
            background: var(--primary-color);
            color: white;
            transform: translateY(-2px);
        }}
        
        .nav-link .tab-icon {{
            font-size: 1.2rem;
            margin-right: 8px;
        }}
        
        .nav-link .tab-description {{
            display: block;
            font-size: 0.8rem;
            opacity: 0.8;
            margin-top: 5px;
        }}
        
        /* Tab Content */
        .tab-content-container {{
            background: white;
            margin: 0 20px 20px 20px;
            border-radius: 0 0 15px 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            min-height: 600px;
        }}
        
        .tab-pane {{
            padding: 30px;
        }}
        
        .visualization-section {{
            margin-bottom: 40px;
        }}
        
        .visualization-title {{
            color: var(--primary-color);
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--primary-color);
        }}
        
        .plot-container {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 20px;
            min-height: 500px;
        }}
        
        /* Interactive Tools Styles */
        .tool-card {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            border-left: 5px solid var(--accent-color);
        }}
        
        .tool-title {{
            color: var(--accent-color);
            font-size: 1.3rem;
            font-weight: bold;
            margin-bottom: 15px;
        }}
        
        .tool-description {{
            color: var(--text-secondary);
            margin-bottom: 20px;
        }}
        
        .btn-tool {{
            background: var(--accent-color);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        
        .btn-tool:hover {{
            background: #e55347;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 99, 71, 0.3);
        }}
        
        /* Loading Animation */
        .loading-spinner {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 200px;
        }}
        
        .spinner {{
            width: 50px;
            height: 50px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid var(--primary-color);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .header-title {{ font-size: 2rem; }}
            .nav-tabs .nav-link {{ padding: 15px 20px; }}
            .tab-pane {{ padding: 20px; }}
            .metric-value {{ font-size: 2rem; }}
        }}
        
        /* Footer */
        .dashboard-footer {{
            background: var(--text-primary);
            color: white;
            text-align: center;
            padding: 20px;
            margin-top: 40px;
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <header class="dashboard-header">
        <div class="container">
            <div class="header-content">
                <h1 class="header-title">{self.dashboard_config["title"]}</h1>
                <p class="header-subtitle">{self.dashboard_config["subtitle"]}</p>
                <p class="header-timestamp">
                    <i class="fas fa-clock"></i> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </p>
            </div>
        </div>
    </header>
    
    <!-- Key Metrics Section -->
    <section class="metrics-section">
        <div class="container">
            <div class="row g-4">
                <div class="col-md-3">
                    <div class="metric-card">
                        <div class="metric-icon">
                            <i class="fas fa-database"></i>
                        </div>
                        <div class="metric-value">{total_records/1e9:.1f}B</div>
                        <div class="metric-label">GBIF Records</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="metric-card">
                        <div class="metric-icon">
                            <i class="fas fa-globe"></i>
                        </div>
                        <div class="metric-value">{countries_covered}</div>
                        <div class="metric-label">Countries Covered</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="metric-card">
                        <div class="metric-icon">
                            <i class="fas fa-camera"></i>
                        </div>
                        <div class="metric-value">{inaturalist_obs/1e6:.0f}M</div>
                        <div class="metric-label">iNaturalist Observations</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="metric-card">
                        <div class="metric-icon">
                            <i class="fas fa-search"></i>
                        </div>
                        <div class="metric-value">5</div>
                        <div class="metric-label">Databases Integrated</div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Main Dashboard -->
    <div class="container-fluid">
        <!-- Tab Navigation -->
        <div class="nav-tabs-container">
            <ul class="nav nav-tabs" id="dashboardTabs" role="tablist">
"""
        
        # Add tab navigation
        for i, tab in enumerate(tabs):
            active_class = "active" if i == 0 else ""
            html_content += f"""
                <li class="nav-item" role="presentation">
                    <button class="nav-link {active_class}" id="{tab['id']}-tab" data-bs-toggle="tab" 
                            data-bs-target="#{tab['id']}-pane" type="button" role="tab" 
                            aria-controls="{tab['id']}-pane" aria-selected="{'true' if i == 0 else 'false'}">
                        <span class="tab-icon">{tab['icon']}</span>
                        {tab['title']}
                        <span class="tab-description">{tab['description']}</span>
                    </button>
                </li>
"""
        
        html_content += """
            </ul>
        </div>
        
        <!-- Tab Content -->
        <div class="tab-content-container">
            <div class="tab-content" id="dashboardTabContent">
"""
        
        # Add tab content
        for i, tab in enumerate(tabs):
            active_class = "show active" if i == 0 else ""
            html_content += f"""
                <div class="tab-pane fade {active_class}" id="{tab['id']}-pane" role="tabpanel" 
                     aria-labelledby="{tab['id']}-tab">
"""
            
            # Add visualizations for this tab
            if tab['id'] == 'interactive':
                # Special handling for interactive tools
                html_content += self._create_interactive_tools_content()
            else:
                # Regular visualizations
                for viz in tab['visualizations']:
                    viz_key = self._get_visualization_key(viz['type'])
                    if viz_key in visualizations:
                        html_content += f"""
                    <div class="visualization-section">
                        <h3 class="visualization-title">{viz['title']}</h3>
                        <div class="plot-container" id="{viz_key}"></div>
                    </div>
"""
                    else:
                        html_content += f"""
                    <div class="visualization-section">
                        <h3 class="visualization-title">{viz['title']}</h3>
                        <div class="plot-container">
                            <div class="loading-spinner">
                                <div class="spinner"></div>
                                <span class="ms-3">Loading {viz['title']}...</span>
                            </div>
                        </div>
                    </div>
"""
            
            html_content += """
                </div>
"""
        
        html_content += """
            </div>
        </div>
    </div>
    
    <!-- Footer -->
    <footer class="dashboard-footer">
        <div class="container">
            <p>&copy; 2025 Global Conservation Data Intelligence Platform | 
               Powered by GBIF, iNaturalist, eBird, IUCN, NASA FIRMS</p>
        </div>
    </footer>
    
    <script>
        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🚀 Initializing Conservation Data Dashboard...');
            
            // Initialize Bootstrap tabs
            var triggerTabList = [].slice.call(document.querySelectorAll('#dashboardTabs button'));
            triggerTabList.forEach(function (triggerEl) {
                var tabTrigger = new bootstrap.Tab(triggerEl);
                
                triggerEl.addEventListener('click', function (event) {
                    event.preventDefault();
                    tabTrigger.show();
                    
                    // Trigger plot resize for the active tab
                    setTimeout(function() {
                        Plotly.Plots.resize();
                    }, 100);
                });
            });
            
            // Load visualizations
            loadAllVisualizations();
            
            console.log('✅ Dashboard initialized successfully!');
        });
        
        function loadAllVisualizations() {
            console.log('📊 Loading all visualizations...');
"""
        
        # Add JavaScript for plotting
        for viz_key, figure in visualizations.items():
            if figure:
                fig_json = figure.to_json()
                html_content += f"""
            
            // Load {viz_key}
            try {{
                var {viz_key}_data = {fig_json};
                if (document.getElementById('{viz_key}')) {{
                    Plotly.newPlot('{viz_key}', {viz_key}_data.data, {viz_key}_data.layout, {{responsive: true}});
                    console.log('✅ Loaded {viz_key}');
                }}
            }} catch (error) {{
                console.error('❌ Error loading {viz_key}:', error);
            }}
"""
        
        html_content += """
            
            console.log('📊 All visualizations loaded!');
        }
        
        // Interactive tool functions
        function openSelectionWizard() {
            alert('🧙‍♂️ Selection Wizard will open the smart_data_selection_interface.py\\n\\nRun: python smart_data_selection_interface.py');
        }
        
        function openParameterOptimizer() {
            alert('⚙️ Parameter Optimizer\\n\\nThis tool helps optimize search parameters based on your research goals.');
        }
        
        function openRealTimeMonitor() {
            alert('📡 Real-time Monitor\\n\\nConnects to live APIs for real-time conservation data monitoring.');
        }
        
        // Utility functions
        window.addEventListener('resize', function() {
            setTimeout(function() {
                Plotly.Plots.resize();
            }, 100);
        });
    </script>
</body>
</html>
"""
        
        return html_content
    
    def _get_visualization_key(self, viz_type):
        """Map visualization type to the actual visualization key."""
        mapping = {
            "database_overview": "database_overview",
            "country_coverage_map": "country_coverage_map",
            "capabilities_matrix": "capabilities_matrix",
            "selection_workflow": "selection_workflow",
            "coverage_quality": "coverage_quality",
            "conservation_analysis": "conservation_analysis",
            "taxonomic_diversity": "taxonomic_diversity",
            "temporal_trends": "temporal_trends",
            "strategy_comparison": "strategy_comparison",
            "recommendations": "recommendations",
            "quality_assessment": "quality_assessment"
        }
        return mapping.get(viz_type, viz_type)
    
    def _create_interactive_tools_content(self):
        """Create content for the interactive tools tab."""
        return """
                    <div class="row">
                        <div class="col-md-4">
                            <div class="tool-card">
                                <h4 class="tool-title">
                                    <i class="fas fa-magic"></i> Smart Data Selection Wizard
                                </h4>
                                <p class="tool-description">
                                    Interactive wizard that guides you through optimal country and database selection 
                                    based on your research objectives.
                                </p>
                                <button class="btn btn-tool" onclick="openSelectionWizard()">
                                    <i class="fas fa-play"></i> Launch Wizard
                                </button>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="tool-card">
                                <h4 class="tool-title">
                                    <i class="fas fa-cogs"></i> Parameter Optimization Tool
                                </h4>
                                <p class="tool-description">
                                    Automatically optimizes search radius, record limits, and quality filters 
                                    based on regional characteristics and data availability.
                                </p>
                                <button class="btn btn-tool" onclick="openParameterOptimizer()">
                                    <i class="fas fa-tools"></i> Optimize Parameters
                                </button>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="tool-card">
                                <h4 class="tool-title">
                                    <i class="fas fa-satellite"></i> Real-time Data Monitor
                                </h4>
                                <p class="tool-description">
                                    Live monitoring of conservation databases with real-time updates, 
                                    alerts, and performance tracking.
                                </p>
                                <button class="btn btn-tool" onclick="openRealTimeMonitor()">
                                    <i class="fas fa-chart-line"></i> Start Monitoring
                                </button>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row mt-4">
                        <div class="col-12">
                            <div class="tool-card">
                                <h4 class="tool-title">
                                    <i class="fas fa-download"></i> Quick Actions
                                </h4>
                                <div class="row">
                                    <div class="col-md-3">
                                        <button class="btn btn-outline-primary w-100 mb-2" onclick="window.print()">
                                            <i class="fas fa-print"></i> Print Dashboard
                                        </button>
                                    </div>
                                    <div class="col-md-3">
                                        <button class="btn btn-outline-success w-100 mb-2" onclick="exportDashboard()">
                                            <i class="fas fa-file-export"></i> Export Data
                                        </button>
                                    </div>
                                    <div class="col-md-3">
                                        <button class="btn btn-outline-info w-100 mb-2" onclick="refreshData()">
                                            <i class="fas fa-sync"></i> Refresh Data
                                        </button>
                                    </div>
                                    <div class="col-md-3">
                                        <button class="btn btn-outline-warning w-100 mb-2" onclick="showHelp()">
                                            <i class="fas fa-question-circle"></i> Help & Guide
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
"""

def main():
    """Generate the unified conservation data dashboard."""
    
    print("🎨 UNIFIED CONSERVATION DATA DASHBOARD GENERATOR")
    print("=" * 60)
    
    generator = UnifiedDashboardGenerator()
    
    # Generate unified dashboard
    dashboard_file = generator.generate_unified_dashboard()
    
    print(f"\n✅ UNIFIED DASHBOARD COMPLETE!")
    print(f"📊 Dashboard saved to: {dashboard_file}")
    print(f"🌐 Single entry point with tabbed navigation for all visualizations")
    
    print(f"\n🎯 DASHBOARD FEATURES:")
    print(f"   • 📱 Responsive design with Bootstrap")
    print(f"   • 🗂️  Tabbed navigation (Overview, Metadata, Conservation, Research, Tools)")
    print(f"   • 📊 All visualizations integrated in one page")
    print(f"   • ⚡ Interactive tools and wizards")
    print(f"   • 🎨 Professional styling with animations")
    print(f"   • 📋 Key metrics dashboard")
    
    print(f"\n🚀 Ready to explore the complete conservation data landscape!")

if __name__ == "__main__":
    main()
