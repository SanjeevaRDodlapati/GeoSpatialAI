# Contributing to GeoSpatialAI 🌍

Thank you for your interest in contributing to the GeoSpatialAI conservation technology platform! We welcome contributions from researchers, educators, students, and conservation practitioners.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Types of Contributions](#types-of-contributions)
- [Development Process](#development-process)
- [Project Structure](#project-structure)
- [Style Guidelines](#style-guidelines)
- [Submitting Contributions](#submitting-contributions)
- [Community](#community)

## 🤝 Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ with conda or pip
- Git for version control
- Basic knowledge of geospatial analysis and Python
- Familiarity with Jupyter notebooks

### Setup Development Environment
```bash
# Clone the repository
git clone https://github.com/SanjeevaRDodlapati/GeoSpatialAI.git
cd GeoSpatialAI

# Create and activate environment
conda create -n geospatial python=3.10
conda activate geospatial

# Install dependencies
pip install -r requirements.txt

# Test your setup
python test_environment.py
```

## 🎯 Types of Contributions

We welcome several types of contributions:

### 📚 Educational Content
- **New tutorials** for additional geospatial techniques
- **Enhanced documentation** and explanations
- **Interactive examples** and exercises
- **Regional adaptations** for different geographic areas

### 🔬 Research Applications
- **New conservation methods** and algorithms
- **Data source integrations** (APIs, datasets)
- **Validation studies** and performance improvements
- **Scientific paper implementations**

### 🛠️ Technical Improvements
- **Code optimization** and performance improvements
- **Bug fixes** and error handling
- **Testing frameworks** and validation scripts
- **Accessibility** and usability enhancements

### 🌍 Data and Examples
- **New datasets** with proper licensing
- **Real-world case studies** from different regions
- **Validation data** for testing and benchmarking
- **Example outputs** and visualizations

## 🔄 Development Process

### 1. Issue Discussion
- Check existing [issues](https://github.com/SanjeevaRDodlapati/GeoSpatialAI/issues) first
- Create a new issue to discuss major changes
- Use appropriate issue templates
- Get feedback before starting work

### 2. Fork and Branch
```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/yourusername/GeoSpatialAI.git
cd GeoSpatialAI

# Create a feature branch
git checkout -b feature/your-feature-name
```

### 3. Development Guidelines
- Follow the existing project structure
- Write clear, commented code
- Include documentation for new features
- Test your changes thoroughly

### 4. Commit Standards
```bash
# Use descriptive commit messages
git commit -m "Add species distribution modeling tutorial

- Implement MaxEnt-style modeling approach
- Include uncertainty quantification
- Add validation with held-out data
- Generate interactive maps with Folium"
```

## 🏗️ Project Structure

Understanding our project organization:

```
GeoSpatialAI/
├── projects/                    # Phase 1: Foundation Projects
│   ├── project_0_cartography_practice/
│   ├── project_1_census_analysis/
│   └── ...
├── applications/                # Phase 2: Advanced Applications
│   ├── real_time_monitoring/
│   ├── predictive_modeling/
│   └── ...
├── docs/                       # Documentation (if adding)
├── tests/                      # Testing scripts
└── examples/                   # Additional examples
```

### Adding New Projects
When contributing new projects:

1. **Create project directory** with consistent naming
2. **Include README.md** with project description
3. **Organize subdirectories**: `notebooks/`, `data/`, `outputs/`
4. **Document prerequisites** and learning outcomes
5. **Provide example outputs** or expected results

## 📝 Style Guidelines

### Jupyter Notebooks
- **Clear markdown headers** for each section
- **Explanatory text** between code cells
- **Comments in code** explaining methodology
- **Consistent naming** for variables and functions
- **Remove output** before committing (or provide clean versions)

### Python Code
```python
# Use descriptive variable names
species_data = gpd.read_file('species_occurrences.geojson')

# Include docstrings for functions
def calculate_species_richness(occurrence_data, grid_size=1000):
    """
    Calculate species richness within grid cells.
    
    Parameters:
    -----------
    occurrence_data : GeoDataFrame
        Species occurrence points with 'species' column
    grid_size : int
        Grid cell size in meters
        
    Returns:
    --------
    GeoDataFrame : Grid with species richness values
    """
```

### Documentation
- **Clear explanations** of methodologies
- **References to scientific literature** when appropriate
- **Step-by-step instructions** for complex procedures
- **Prerequisites** and skill level indicators

## 🔍 Submitting Contributions

### Pull Request Process

1. **Update documentation** for any new features
2. **Include tests** or validation for new functionality
3. **Update README.md** if adding major features
4. **Ensure compatibility** across different operating systems

### Pull Request Template
When submitting a PR, include:

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix
- [ ] New tutorial/project
- [ ] Enhancement to existing project
- [ ] Documentation update
- [ ] Research application

## Testing
- [ ] Tested on macOS/Windows/Linux
- [ ] All notebooks execute without errors
- [ ] Generated expected outputs
- [ ] Verified with different datasets

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Documentation updated
- [ ] No breaking changes to existing projects
```

### Review Process
- All contributions require review
- Maintainers will provide constructive feedback
- Address review comments promptly
- Be patient - educational content requires thorough review

## 🌟 Community Guidelines

### Educational Focus
This project prioritizes:
- **Learning progression** from beginner to advanced
- **Real-world applications** in conservation
- **Reproducible science** and best practices
- **Accessibility** for diverse audiences

### Collaboration Principles
- **Respectful communication** in all interactions
- **Constructive feedback** and suggestions
- **Credit attribution** for all contributors
- **Open science** values and practices

### Getting Help
- **Issues**: Technical problems and bug reports
- **Discussions**: General questions and brainstorming
- **Email**: For sensitive or private matters
- **Documentation**: Check existing docs first

## 🎓 Recognition

Contributors will be acknowledged in:
- Project documentation and README
- Research publications (for significant contributions)
- Conference presentations and talks
- Community showcase features

## 📚 Resources for Contributors

### Learning Resources
- [GeoPandas Documentation](https://geopandas.org/)
- [Rasterio User Guide](https://rasterio.readthedocs.io/)
- [Cartopy Documentation](https://scitools.org.uk/cartopy/)
- [Conservation Biology Principles](https://conbio.onlinelibrary.wiley.com/)

### Development Tools
- [Jupyter Lab](https://jupyterlab.readthedocs.io/) for development
- [nbstripout](https://github.com/kynan/nbstripout) for clean commits
- [Pre-commit](https://pre-commit.com/) for code quality
- [pytest](https://pytest.org/) for testing

---

## 🌍 Let's Build Better Conservation Technology Together!

Your contributions help advance open science, education, and real-world conservation impact. Thank you for being part of this community!

For questions about contributing, please open an issue or reach out to the maintainers.

**Happy coding and conserving!** 🌿🐾🗺️
