# 🌍 GeoSpatial Conservation AI Platform

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 📋 Overview

A comprehensive geospatial AI platform for biodiversity conservation and environmental monitoring. Provides real-time monitoring, species distribution modeling, and conservation analytics.

## 📁 Repository Structure

```
GeoSpatialAI/
├── src/                              # Core application code
│   ├── api/                          # API integrations (GBIF, NASA, eBird)
│   ├── web/                          # Web server and interface
│   └── utils/                        # Utilities and configuration
├── web/                              # Frontend assets
│   ├── templates/                    # HTML templates
│   └── static/                       # CSS, JS, images
├── tests/                            # Test suite
├── config/                           # Configuration files
├── docs/                             # Documentation
├── projects/                         # Educational projects (10 projects)
├── applications/                     # Real-world applications
├── models/                           # ML models storage
└── archive/                          # Legacy files
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- 8GB+ RAM recommended
- Internet connection for API access

### Installation

1. **Clone repository**
```bash
git clone https://github.com/SanjeevaRDodlapati/GeoSpatialAI.git
cd GeoSpatialAI
```

2. **Setup environment**
```bash
# Using conda (recommended)
conda env create -f config/conda_environment.yml
conda activate geo_env

# OR using pip
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure API keys**
```bash
cp config/env_template.env .env
# Edit .env with your API keys
```

4. **Test installation**
```bash
python test_environment.py
```

### Launch Platform

**Start web server:**
```bash
conda activate geo_env
python src/web/server.py
```

**Access dashboard:** Open `http://localhost:8000`

## 🎯 Key Features

- **Real-time Environmental Monitoring**: IoT sensors & satellite data
- **Species Distribution Modeling**: ML-powered biodiversity analysis  
- **Conservation Analytics**: Data-driven decision support
- **Interactive Dashboards**: Web-based visualization tools
- **API Integrations**: GBIF, NASA, eBird, climate APIs

## 🛠️ Core Technologies

- **Geospatial**: GeoPandas, Rasterio, Folium
- **ML/AI**: TensorFlow, Scikit-learn, YOLOv8
- **Visualization**: Plotly, Matplotlib, Streamlit
- **Web**: Flask, HTML/CSS/JavaScript

## 📚 Documentation

- **Setup Guide**: `docs/setup/INSTALLATION.md`
- **User Guide**: `docs/user_guide/`
- **API Documentation**: `docs/technical/`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Submit pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📧 Contact

- **Email**: s.dodlapati@outlook.com
- **Issues**: [GitHub Issues](https://github.com/SanjeevaRDodlapati/GeoSpatialAI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/SanjeevaRDodlapati/GeoSpatialAI/discussions)

---

**🎯 A production-ready conservation technology platform for real-world impact!** 🌿🤖
