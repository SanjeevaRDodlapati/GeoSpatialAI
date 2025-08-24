"""
Advanced Unified Dashboard with Enhanced Navigation
==================================================

Enhanced version with sidebar navigation, breadcrumbs, and full-screen modes.

Author: GeoSpatialAI Development Team
Date: August 24, 2025
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import logging

# Import existing classes
from conservation_data_visualizer import ConservationDataVisualizer
from metadata_visualization_system import MetadataVisualizationSystem

logger = logging.getLogger(__name__)

class AdvancedUnifiedDashboard:
    """
    Advanced unified dashboard with enhanced navigation, sidebar menu,
    breadcrumbs, full-screen modes, and responsive design.
    """
    
    def __init__(self):
        self.conservation_viz = ConservationDataVisualizer()
        self.metadata_viz = MetadataVisualizationSystem()
        
        self.dashboard_sections = {
            "overview": {
                "title": "Global Overview",
                "icon": "fas fa-globe",
                "description": "Comprehensive global conservation data statistics",
                "subsections": [
                    {"id": "global_metrics", "title": "Global Metrics", "icon": "fas fa-chart-bar"},
                    {"id": "database_comparison", "title": "Database Comparison", "icon": "fas fa-database"},
                    {"id": "coverage_maps", "title": "Coverage Maps", "icon": "fas fa-map"}
                ]
            },
            "intelligence": {
                "title": "Metadata Intelligence",
                "icon": "fas fa-brain",
                "description": "AI-powered database analysis and selection",
                "subsections": [
                    {"id": "capabilities", "title": "Database Capabilities", "icon": "fas fa-cogs"},
                    {"id": "selection_ai", "title": "Intelligent Selection", "icon": "fas fa-magic"},
                    {"id": "quality_matrix", "title": "Quality Analysis", "icon": "fas fa-star"}
                ]
            },
            "conservation": {
                "title": "Conservation Analysis",
                "icon": "fas fa-leaf",
                "description": "Real-world conservation area performance",
                "subsections": [
                    {"id": "areas_analysis", "title": "Protected Areas", "icon": "fas fa-shield-alt"},
                    {"id": "biodiversity", "title": "Biodiversity Patterns", "icon": "fas fa-paw"},
                    {"id": "threats_assessment", "title": "Threats Assessment", "icon": "fas fa-exclamation-triangle"}
                ]
            },
            "research": {
                "title": "Research Tools",
                "icon": "fas fa-microscope",
                "description": "Research strategy optimization and planning",
                "subsections": [
                    {"id": "strategy_optimizer", "title": "Strategy Optimizer", "icon": "fas fa-target"},
                    {"id": "data_planner", "title": "Data Collection Planner", "icon": "fas fa-calendar-alt"},
                    {"id": "collaboration", "title": "Collaboration Hub", "icon": "fas fa-users"}
                ]
            },
            "monitoring": {
                "title": "Real-time Monitoring",
                "icon": "fas fa-satellite",
                "description": "Live data monitoring and alerts",
                "subsections": [
                    {"id": "live_feeds", "title": "Live Data Feeds", "icon": "fas fa-rss"},
                    {"id": "alerts_system", "title": "Alert System", "icon": "fas fa-bell"},
                    {"id": "performance", "title": "Performance Dashboard", "icon": "fas fa-tachometer-alt"}
                ]
            }
        }
    
    def generate_advanced_dashboard(self) -> str:
        """Generate the advanced unified dashboard."""
        
        logger.info("🎨 Generating advanced unified dashboard...")
        
        # Generate all visualizations
        visualizations = self._generate_all_visualizations()
        
        # Load metadata
        metadata = self.metadata_viz.metadata
        
        # Create HTML
        html_content = self._create_advanced_html(visualizations, metadata)
        
        # Save dashboard
        dashboard_file = Path("advanced_unified_dashboard.html")
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"✅ Advanced dashboard saved to: {dashboard_file}")
        return str(dashboard_file)
    
    def _generate_all_visualizations(self):
        """Generate all visualizations for the dashboard."""
        
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
            
        except Exception as e:
            logger.error(f"⚠️ Some visualizations may not be available: {e}")
        
        return visualizations
    
    def _create_advanced_html(self, visualizations, metadata):
        """Create the complete advanced HTML structure."""
        
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
    <title>🌍 Advanced Conservation Intelligence Platform</title>
    
    <!-- External Libraries -->
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        /* Enhanced Global Styles */
        :root {{
            --primary-gradient: linear-gradient(135deg, #2E8B57 0%, #4682B4 100%);
            --secondary-gradient: linear-gradient(135deg, #FF6347 0%, #FFD700 100%);
            --success-gradient: linear-gradient(135deg, #32CD32 0%, #228B22 100%);
            --danger-gradient: linear-gradient(135deg, #FF4444 0%, #CC0000 100%);
            --sidebar-width: 280px;
            --header-height: 80px;
            --transition-speed: 0.3s;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            overflow-x: hidden;
        }}
        
        /* Header */
        .header {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: var(--header-height);
            background: var(--primary-gradient);
            color: white;
            z-index: 1000;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            padding: 0 20px;
        }}
        
        .header-left {{
            display: flex;
            align-items: center;
        }}
        
        .sidebar-toggle {{
            background: none;
            border: none;
            color: white;
            font-size: 1.2rem;
            margin-right: 20px;
            padding: 8px;
            border-radius: 4px;
            transition: all var(--transition-speed);
        }}
        
        .sidebar-toggle:hover {{
            background: rgba(255,255,255,0.1);
        }}
        
        .header-title {{
            font-size: 1.5rem;
            font-weight: bold;
        }}
        
        .header-right {{
            margin-left: auto;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .header-stats {{
            display: flex;
            gap: 20px;
            font-size: 0.9rem;
        }}
        
        .header-stat {{
            text-align: center;
        }}
        
        .header-stat-value {{
            font-weight: bold;
            font-size: 1.1rem;
        }}
        
        .header-stat-label {{
            opacity: 0.8;
            font-size: 0.8rem;
        }}
        
        /* Sidebar */
        .sidebar {{
            position: fixed;
            top: var(--header-height);
            left: 0;
            width: var(--sidebar-width);
            height: calc(100vh - var(--header-height));
            background: white;
            box-shadow: 4px 0 20px rgba(0,0,0,0.1);
            transform: translateX(-100%);
            transition: transform var(--transition-speed);
            z-index: 999;
            overflow-y: auto;
        }}
        
        .sidebar.open {{
            transform: translateX(0);
        }}
        
        .sidebar-header {{
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }}
        
        .sidebar-title {{
            font-size: 1.1rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }}
        
        .sidebar-subtitle {{
            font-size: 0.9rem;
            color: #6c757d;
        }}
        
        .sidebar-nav {{
            padding: 0;
        }}
        
        .nav-section {{
            margin-bottom: 10px;
        }}
        
        .nav-section-title {{
            padding: 15px 20px 10px;
            font-size: 0.9rem;
            font-weight: bold;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .nav-item {{
            border: none;
            margin: 0;
        }}
        
        .nav-link {{
            display: flex;
            align-items: center;
            padding: 12px 20px;
            color: #2c3e50;
            text-decoration: none;
            border-left: 4px solid transparent;
            transition: all var(--transition-speed);
        }}
        
        .nav-link:hover {{
            background: #f8f9fa;
            color: #2E8B57;
            border-left-color: #2E8B57;
        }}
        
        .nav-link.active {{
            background: linear-gradient(90deg, rgba(46, 139, 87, 0.1) 0%, transparent 100%);
            color: #2E8B57;
            border-left-color: #2E8B57;
            font-weight: 500;
        }}
        
        .nav-icon {{
            width: 20px;
            margin-right: 12px;
            text-align: center;
        }}
        
        .nav-text {{
            flex: 1;
        }}
        
        .nav-badge {{
            background: #e74c3c;
            color: white;
            border-radius: 10px;
            padding: 2px 8px;
            font-size: 0.7rem;
            font-weight: bold;
        }}
        
        /* Main Content */
        .main-content {{
            margin-top: var(--header-height);
            margin-left: 0;
            transition: margin-left var(--transition-speed);
            min-height: calc(100vh - var(--header-height));
            background: white;
        }}
        
        .main-content.sidebar-open {{
            margin-left: var(--sidebar-width);
        }}
        
        /* Breadcrumb */
        .breadcrumb-container {{
            background: #f8f9fa;
            padding: 15px 30px;
            border-bottom: 1px solid #dee2e6;
        }}
        
        .breadcrumb {{
            background: none;
            margin: 0;
            padding: 0;
        }}
        
        .breadcrumb-item a {{
            color: #6c757d;
            text-decoration: none;
        }}
        
        .breadcrumb-item a:hover {{
            color: #2E8B57;
        }}
        
        .breadcrumb-item.active {{
            color: #2c3e50;
            font-weight: 500;
        }}
        
        /* Content Area */
        .content-area {{
            padding: 30px;
        }}
        
        .content-header {{
            margin-bottom: 30px;
        }}
        
        .content-title {{
            font-size: 2rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        
        .content-description {{
            color: #6c757d;
            font-size: 1.1rem;
        }}
        
        .content-actions {{
            margin-top: 20px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        
        /* Visualization Cards */
        .viz-card {{
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            overflow: hidden;
            transition: all var(--transition-speed);
        }}
        
        .viz-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        }}
        
        .viz-card-header {{
            background: var(--primary-gradient);
            color: white;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .viz-card-title {{
            font-size: 1.3rem;
            font-weight: bold;
            margin: 0;
        }}
        
        .viz-card-actions {{
            display: flex;
            gap: 10px;
        }}
        
        .viz-action-btn {{
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.9rem;
            transition: all var(--transition-speed);
        }}
        
        .viz-action-btn:hover {{
            background: rgba(255,255,255,0.3);
        }}
        
        .viz-card-body {{
            padding: 0;
            min-height: 500px;
        }}
        
        .plot-container {{
            width: 100%;
            height: 500px;
            padding: 20px;
        }}
        
        /* Action Buttons */
        .btn-primary-gradient {{
            background: var(--primary-gradient);
            border: none;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: 500;
            transition: all var(--transition-speed);
        }}
        
        .btn-primary-gradient:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(46, 139, 87, 0.3);
        }}
        
        .btn-success-gradient {{
            background: var(--success-gradient);
            border: none;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: 500;
            transition: all var(--transition-speed);
        }}
        
        .btn-success-gradient:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(50, 205, 50, 0.3);
        }}
        
        /* Loading States */
        .loading-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255,255,255,0.9);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10;
        }}
        
        .spinner {{
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #2E8B57;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        /* Fullscreen Mode */
        .fullscreen-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: white;
            z-index: 2000;
            display: none;
        }}
        
        .fullscreen-overlay.active {{
            display: block;
        }}
        
        .fullscreen-header {{
            background: var(--primary-gradient);
            color: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .fullscreen-content {{
            height: calc(100vh - 60px);
            padding: 20px;
        }}
        
        .fullscreen-plot {{
            width: 100%;
            height: 100%;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .sidebar {{
                width: 100%;
            }}
            
            .main-content.sidebar-open {{
                margin-left: 0;
            }}
            
            .header-stats {{
                display: none;
            }}
            
            .content-area {{
                padding: 20px 15px;
            }}
            
            .viz-card-header {{
                padding: 15px;
            }}
            
            .viz-card-title {{
                font-size: 1.1rem;
            }}
        }}
        
        /* Overlay for mobile sidebar */
        .sidebar-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            z-index: 998;
            display: none;
        }}
        
        .sidebar-overlay.show {{
            display: block;
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="header-left">
            <button class="sidebar-toggle" onclick="toggleSidebar()">
                <i class="fas fa-bars"></i>
            </button>
            <h1 class="header-title">🌍 Conservation Intelligence Platform</h1>
        </div>
        <div class="header-right">
            <div class="header-stats">
                <div class="header-stat">
                    <div class="header-stat-value">{total_records/1e9:.1f}B</div>
                    <div class="header-stat-label">GBIF Records</div>
                </div>
                <div class="header-stat">
                    <div class="header-stat-value">{countries_covered}</div>
                    <div class="header-stat-label">Countries</div>
                </div>
                <div class="header-stat">
                    <div class="header-stat-value">{inaturalist_obs/1e6:.0f}M</div>
                    <div class="header-stat-label">iNaturalist</div>
                </div>
            </div>
            <button class="btn btn-sm btn-outline-light" onclick="refreshDashboard()">
                <i class="fas fa-sync-alt"></i>
            </button>
            <button class="btn btn-sm btn-outline-light" onclick="showHelp()">
                <i class="fas fa-question-circle"></i>
            </button>
        </div>
    </header>
    
    <!-- Sidebar Overlay (Mobile) -->
    <div class="sidebar-overlay" onclick="closeSidebar()"></div>
    
    <!-- Sidebar -->
    <nav class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <div class="sidebar-title">Navigation</div>
            <div class="sidebar-subtitle">Conservation Data Intelligence</div>
        </div>
        
        <div class="sidebar-nav">
"""
        
        # Add sidebar navigation
        for section_id, section in self.dashboard_sections.items():
            html_content += f"""
            <div class="nav-section">
                <div class="nav-section-title">{section['title']}</div>
"""
            for subsection in section['subsections']:
                html_content += f"""
                <a href="#" class="nav-link" data-section="{section_id}" data-subsection="{subsection['id']}" 
                   onclick="navigateToSection('{section_id}', '{subsection['id']}')">
                    <i class="nav-icon {subsection['icon']}"></i>
                    <span class="nav-text">{subsection['title']}</span>
                </a>
"""
            html_content += """
            </div>
"""
        
        html_content += """
        </div>
    </nav>
    
    <!-- Main Content -->
    <main class="main-content" id="mainContent">
        <!-- Breadcrumb -->
        <div class="breadcrumb-container">
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb" id="breadcrumb">
                    <li class="breadcrumb-item"><a href="#" onclick="navigateHome()">Home</a></li>
                    <li class="breadcrumb-item active" id="currentSection">Global Overview</li>
                </ol>
            </nav>
        </div>
        
        <!-- Content Area -->
        <div class="content-area">
            <div class="content-header">
                <h2 class="content-title" id="contentTitle">Global Conservation Data Overview</h2>
                <p class="content-description" id="contentDescription">
                    Comprehensive analysis of global conservation databases and biodiversity patterns.
                </p>
                <div class="content-actions">
                    <button class="btn btn-primary-gradient" onclick="exportCurrentView()">
                        <i class="fas fa-download"></i> Export Data
                    </button>
                    <button class="btn btn-success-gradient" onclick="shareCurrentView()">
                        <i class="fas fa-share"></i> Share View
                    </button>
                    <button class="btn btn-outline-secondary" onclick="printCurrentView()">
                        <i class="fas fa-print"></i> Print
                    </button>
                </div>
            </div>
            
            <!-- Dynamic Content Container -->
            <div id="dynamicContent">
                <!-- Global Overview Section (Default) -->
                <div class="viz-card">
                    <div class="viz-card-header">
                        <h3 class="viz-card-title">
                            <i class="fas fa-chart-bar"></i> Global Database Overview
                        </h3>
                        <div class="viz-card-actions">
                            <button class="viz-action-btn" onclick="fullscreenPlot('database_overview')">
                                <i class="fas fa-expand"></i>
                            </button>
                            <button class="viz-action-btn" onclick="downloadPlot('database_overview')">
                                <i class="fas fa-download"></i>
                            </button>
                        </div>
                    </div>
                    <div class="viz-card-body">
                        <div class="plot-container" id="database_overview"></div>
                    </div>
                </div>
                
                <div class="viz-card">
                    <div class="viz-card-header">
                        <h3 class="viz-card-title">
                            <i class="fas fa-map"></i> Global Coverage Map
                        </h3>
                        <div class="viz-card-actions">
                            <button class="viz-action-btn" onclick="fullscreenPlot('country_coverage_map')">
                                <i class="fas fa-expand"></i>
                            </button>
                            <button class="viz-action-btn" onclick="downloadPlot('country_coverage_map')">
                                <i class="fas fa-download"></i>
                            </button>
                        </div>
                    </div>
                    <div class="viz-card-body">
                        <div class="plot-container" id="country_coverage_map"></div>
                    </div>
                </div>
            </div>
        </div>
    </main>
    
    <!-- Fullscreen Overlay -->
    <div class="fullscreen-overlay" id="fullscreenOverlay">
        <div class="fullscreen-header">
            <h3 id="fullscreenTitle">Fullscreen View</h3>
            <button class="btn btn-outline-light" onclick="closeFullscreen()">
                <i class="fas fa-times"></i> Close
            </button>
        </div>
        <div class="fullscreen-content">
            <div class="fullscreen-plot" id="fullscreenPlot"></div>
        </div>
    </div>
    
    <script>
        // Global Variables
        let sidebarOpen = false;
        let currentSection = 'overview';
        let currentSubsection = 'global_metrics';
        let visualizations = {{}};
        
        // Initialize Dashboard
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('🚀 Initializing Advanced Conservation Dashboard...');
            
            // Load all visualizations
            loadAllVisualizations();
            
            // Set initial navigation state
            updateActiveNavigation();
            
            console.log('✅ Dashboard initialized successfully!');
        }});
        
        // Sidebar Functions
        function toggleSidebar() {{
            sidebarOpen = !sidebarOpen;
            const sidebar = document.getElementById('sidebar');
            const mainContent = document.getElementById('mainContent');
            const overlay = document.querySelector('.sidebar-overlay');
            
            if (sidebarOpen) {{
                sidebar.classList.add('open');
                mainContent.classList.add('sidebar-open');
                overlay.classList.add('show');
            }} else {{
                sidebar.classList.remove('open');
                mainContent.classList.remove('sidebar-open');
                overlay.classList.remove('show');
            }}
        }}
        
        function closeSidebar() {{
            sidebarOpen = false;
            document.getElementById('sidebar').classList.remove('open');
            document.getElementById('mainContent').classList.remove('sidebar-open');
            document.querySelector('.sidebar-overlay').classList.remove('show');
        }}
        
        // Navigation Functions
        function navigateToSection(section, subsection) {{
            currentSection = section;
            currentSubsection = subsection;
            
            updateBreadcrumb(section, subsection);
            updateContentHeader(section, subsection);
            updateActiveNavigation();
            loadSectionContent(section, subsection);
            
            // Close sidebar on mobile
            if (window.innerWidth <= 768) {{
                closeSidebar();
            }}
        }}
        
        function navigateHome() {{
            navigateToSection('overview', 'global_metrics');
        }}
        
        function updateBreadcrumb(section, subsection) {{
            const breadcrumb = document.getElementById('breadcrumb');
            const sectionInfo = getSectionInfo(section, subsection);
            
            breadcrumb.innerHTML = `
                <li class="breadcrumb-item"><a href="#" onclick="navigateHome()">Home</a></li>
                <li class="breadcrumb-item"><a href="#" onclick="navigateToSection('${{section}}', '${{subsection}}')">${{sectionInfo.sectionTitle}}</a></li>
                <li class="breadcrumb-item active">${{sectionInfo.subsectionTitle}}</li>
            `;
        }}
        
        function updateContentHeader(section, subsection) {{
            const sectionInfo = getSectionInfo(section, subsection);
            document.getElementById('contentTitle').textContent = sectionInfo.subsectionTitle;
            document.getElementById('contentDescription').textContent = sectionInfo.description;
        }}
        
        function updateActiveNavigation() {{
            document.querySelectorAll('.nav-link').forEach(link => {{
                link.classList.remove('active');
            }});
            
            const activeLink = document.querySelector(`[data-section="${{currentSection}}"][data-subsection="${{currentSubsection}}"]`);
            if (activeLink) {{
                activeLink.classList.add('active');
            }}
        }}
        
        function getSectionInfo(section, subsection) {{
            const sections = {json.dumps(self.dashboard_sections, indent=12)};
            
            const sectionData = sections[section];
            const subsectionData = sectionData.subsections.find(s => s.id === subsection);
            
            return {{
                sectionTitle: sectionData.title,
                subsectionTitle: subsectionData.title,
                description: sectionData.description
            }};
        }}
        
        function loadSectionContent(section, subsection) {{
            const content = document.getElementById('dynamicContent');
            
            // Show loading
            content.innerHTML = `
                <div class="viz-card">
                    <div class="viz-card-body">
                        <div class="loading-overlay">
                            <div class="spinner"></div>
                            <span class="ms-3">Loading ${{getSectionInfo(section, subsection).subsectionTitle}}...</span>
                        </div>
                    </div>
                </div>
            `;
            
            // Simulate loading and then show appropriate content
            setTimeout(() => {{
                showSectionContent(section, subsection);
            }}, 500);
        }}
        
        function showSectionContent(section, subsection) {{
            const content = document.getElementById('dynamicContent');
            
            // Create content based on section and subsection
            let contentHTML = '';
            
            switch(section) {{
                case 'overview':
                    contentHTML = createOverviewContent(subsection);
                    break;
                case 'intelligence':
                    contentHTML = createIntelligenceContent(subsection);
                    break;
                case 'conservation':
                    contentHTML = createConservationContent(subsection);
                    break;
                case 'research':
                    contentHTML = createResearchContent(subsection);
                    break;
                case 'monitoring':
                    contentHTML = createMonitoringContent(subsection);
                    break;
            }}
            
            content.innerHTML = contentHTML;
            
            // Re-plot visualizations for this section
            replotVisualizationsForSection(section, subsection);
        }}
        
        function createOverviewContent(subsection) {{
            switch(subsection) {{
                case 'global_metrics':
                    return `
                        <div class="viz-card">
                            <div class="viz-card-header">
                                <h3 class="viz-card-title"><i class="fas fa-chart-bar"></i> Global Database Overview</h3>
                                <div class="viz-card-actions">
                                    <button class="viz-action-btn" onclick="fullscreenPlot('database_overview')">
                                        <i class="fas fa-expand"></i>
                                    </button>
                                </div>
                            </div>
                            <div class="viz-card-body">
                                <div class="plot-container" id="database_overview"></div>
                            </div>
                        </div>
                    `;
                case 'database_comparison':
                    return `
                        <div class="viz-card">
                            <div class="viz-card-header">
                                <h3 class="viz-card-title"><i class="fas fa-database"></i> Database Capabilities Matrix</h3>
                                <div class="viz-card-actions">
                                    <button class="viz-action-btn" onclick="fullscreenPlot('capabilities_matrix')">
                                        <i class="fas fa-expand"></i>
                                    </button>
                                </div>
                            </div>
                            <div class="viz-card-body">
                                <div class="plot-container" id="capabilities_matrix"></div>
                            </div>
                        </div>
                    `;
                case 'coverage_maps':
                    return `
                        <div class="viz-card">
                            <div class="viz-card-header">
                                <h3 class="viz-card-title"><i class="fas fa-map"></i> Global Coverage Map</h3>
                                <div class="viz-card-actions">
                                    <button class="viz-action-btn" onclick="fullscreenPlot('country_coverage_map')">
                                        <i class="fas fa-expand"></i>
                                    </button>
                                </div>
                            </div>
                            <div class="viz-card-body">
                                <div class="plot-container" id="country_coverage_map"></div>
                            </div>
                        </div>
                    `;
            }}
        }}
        
        function createIntelligenceContent(subsection) {{
            return `
                <div class="viz-card">
                    <div class="viz-card-header">
                        <h3 class="viz-card-title"><i class="fas fa-brain"></i> Intelligent Selection Workflow</h3>
                        <div class="viz-card-actions">
                            <button class="viz-action-btn" onclick="fullscreenPlot('selection_workflow')">
                                <i class="fas fa-expand"></i>
                            </button>
                        </div>
                    </div>
                    <div class="viz-card-body">
                        <div class="plot-container" id="selection_workflow"></div>
                    </div>
                </div>
            `;
        }}
        
        function createConservationContent(subsection) {{
            return `
                <div class="viz-card">
                    <div class="viz-card-header">
                        <h3 class="viz-card-title"><i class="fas fa-leaf"></i> Conservation Areas Analysis</h3>
                        <div class="viz-card-actions">
                            <button class="viz-action-btn" onclick="fullscreenPlot('conservation_analysis')">
                                <i class="fas fa-expand"></i>
                            </button>
                        </div>
                    </div>
                    <div class="viz-card-body">
                        <div class="plot-container" id="conservation_analysis"></div>
                    </div>
                </div>
            `;
        }}
        
        function createResearchContent(subsection) {{
            return `
                <div class="viz-card">
                    <div class="viz-card-header">
                        <h3 class="viz-card-title"><i class="fas fa-microscope"></i> Research Strategy Comparison</h3>
                        <div class="viz-card-actions">
                            <button class="viz-action-btn" onclick="fullscreenPlot('strategy_comparison')">
                                <i class="fas fa-expand"></i>
                            </button>
                        </div>
                    </div>
                    <div class="viz-card-body">
                        <div class="plot-container" id="strategy_comparison"></div>
                    </div>
                </div>
            `;
        }}
        
        function createMonitoringContent(subsection) {{
            return `
                <div class="viz-card">
                    <div class="viz-card-header">
                        <h3 class="viz-card-title"><i class="fas fa-satellite"></i> Real-time Monitoring Dashboard</h3>
                        <div class="viz-card-actions">
                            <button class="viz-action-btn">
                                <i class="fas fa-play"></i> Start Monitoring
                            </button>
                        </div>
                    </div>
                    <div class="viz-card-body">
                        <div class="plot-container">
                            <div style="text-align: center; padding: 50px; color: #6c757d;">
                                <i class="fas fa-satellite fa-3x mb-3"></i>
                                <h4>Real-time Monitoring</h4>
                                <p>Live conservation data monitoring will be displayed here.</p>
                                <button class="btn btn-primary-gradient">Start Live Feed</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }}
        
        function loadAllVisualizations() {{
            console.log('📊 Loading all visualizations...');
"""
        
        # Add JavaScript for plotting visualizations
        for viz_key, figure in visualizations.items():
            if figure:
                fig_json = figure.to_json()
                html_content += f"""
            
            // Load {viz_key}
            try {{
                visualizations['{viz_key}'] = {fig_json};
                if (document.getElementById('{viz_key}')) {{
                    Plotly.newPlot('{viz_key}', visualizations['{viz_key}'].data, visualizations['{viz_key}'].layout, {{responsive: true}});
                    console.log('✅ Loaded {viz_key}');
                }}
            }} catch (error) {{
                console.error('❌ Error loading {viz_key}:', error);
            }}
"""
        
        html_content += """
        }
        
        function replotVisualizationsForSection(section, subsection) {
            // Re-plot visualizations that are now visible
            setTimeout(() => {
                Object.keys(visualizations).forEach(vizKey => {
                    const element = document.getElementById(vizKey);
                    if (element && visualizations[vizKey]) {
                        Plotly.newPlot(vizKey, visualizations[vizKey].data, visualizations[vizKey].layout, {responsive: true});
                    }
                });
            }, 100);
        }
        
        // Fullscreen Functions
        function fullscreenPlot(plotId) {
            const overlay = document.getElementById('fullscreenOverlay');
            const title = document.getElementById('fullscreenTitle');
            const plotContainer = document.getElementById('fullscreenPlot');
            
            title.textContent = `Fullscreen: ${plotId.replace('_', ' ').toUpperCase()}`;
            overlay.classList.add('active');
            
            if (visualizations[plotId]) {
                Plotly.newPlot('fullscreenPlot', visualizations[plotId].data, visualizations[plotId].layout, {responsive: true});
            }
        }
        
        function closeFullscreen() {
            document.getElementById('fullscreenOverlay').classList.remove('active');
        }
        
        // Utility Functions
        function refreshDashboard() {
            location.reload();
        }
        
        function showHelp() {
            alert('🎯 Conservation Intelligence Platform Help\\n\\n• Use the sidebar to navigate between sections\\n• Click the expand icon to view plots in fullscreen\\n• Use the action buttons to export or share views\\n• All visualizations are interactive - hover, zoom, and click to explore!');
        }
        
        function exportCurrentView() {
            alert('📊 Export functionality will download the current analysis data.');
        }
        
        function shareCurrentView() {
            if (navigator.share) {
                navigator.share({
                    title: 'Conservation Intelligence Platform',
                    text: 'Check out this conservation data analysis!',
                    url: window.location.href
                });
            } else {
                navigator.clipboard.writeText(window.location.href);
                alert('🔗 URL copied to clipboard!');
            }
        }
        
        function printCurrentView() {
            window.print();
        }
        
        function downloadPlot(plotId) {
            if (document.getElementById(plotId)) {
                Plotly.downloadImage(plotId, {
                    format: 'png',
                    width: 1200,
                    height: 800,
                    filename: plotId
                });
            }
        }
        
        // Responsive handling
        window.addEventListener('resize', function() {
            setTimeout(function() {
                Plotly.Plots.resize();
            }, 100);
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case 'b':
                        e.preventDefault();
                        toggleSidebar();
                        break;
                    case 'h':
                        e.preventDefault();
                        navigateHome();
                        break;
                    case 'r':
                        e.preventDefault();
                        refreshDashboard();
                        break;
                }
            }
            
            if (e.key === 'Escape') {
                closeFullscreen();
                closeSidebar();
            }
        });
    </script>
</body>
</html>
"""
        
        return html_content

def main():
    """Generate the advanced unified dashboard."""
    
    print("🎨 ADVANCED UNIFIED DASHBOARD GENERATOR")
    print("=" * 60)
    
    dashboard = AdvancedUnifiedDashboard()
    
    # Generate dashboard
    dashboard_file = dashboard.generate_advanced_dashboard()
    
    print(f"\n✅ ADVANCED DASHBOARD COMPLETE!")
    print(f"📊 Dashboard saved to: {dashboard_file}")
    
    print(f"\n🎯 ADVANCED FEATURES:")
    print(f"   • 🗂️  Collapsible sidebar navigation with sections")
    print(f"   • 🍞 Breadcrumb navigation")
    print(f"   • 🖥️  Fullscreen visualization mode")
    print(f"   • 📱 Responsive design for all devices")
    print(f"   • ⌨️  Keyboard shortcuts (Ctrl+B, Ctrl+H, Ctrl+R)")
    print(f"   • 🎨 Professional gradient styling")
    print(f"   • 📊 Interactive visualization cards")
    print(f"   • 🔄 Dynamic content loading")
    
    print(f"\n🚀 Experience the next-level conservation data platform!")

if __name__ == "__main__":
    main()
