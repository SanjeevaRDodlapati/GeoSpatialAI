# 📊 Project 1: Census Analysis & Demographic Mapping

**Complete Tutorial Series: State to County-Level Analysis with Machine Learning**

This project provides a comprehensive tutorial series for analyzing US demographic data using Census APIs, geospatial analysis, and machine learning techniques. Progress from basic state-level mapping to advanced county-level clustering with health integration.

## 🚀 **Quick Start - Run in Google Colab**

Click any badge below to open the notebook directly in Google Colab:

### 📈 Project 1a: State-Level Foundation
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SanjeevaRDodlapati/GeoSpatialAI/blob/main/projects/project_1_census_analysis/notebooks/02a_census_state_level_analysis.ipynb)

**Skill Level:** Foundation | **Time:** 1-2 hours  
Master Census API basics, create choropleth maps, analyze state-level demographic patterns.

### 🤖 Project 1b: County-Level Machine Learning
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SanjeevaRDodlapati/GeoSpatialAI/blob/main/projects/project_1_census_analysis/notebooks/02b_census_county_level_deep_dive.ipynb)

**Skill Level:** Advanced | **Time:** 3-4 hours  
Apply ML clustering, PCA analysis, spatial autocorrelation (LISA) to 3,100+ counties.

### 🏥 Project 1c: Health Integration & Policy
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SanjeevaRDodlapati/GeoSpatialAI/blob/main/projects/project_1_census_analysis/notebooks/02c_health_integration_policy_analysis.ipynb)

**Skill Level:** Expert | **Time:** 4-5 hours  
Integrate CDC health data, environmental justice analysis, policy-ready dashboards.

---

## 📚 **Tutorial Progression**

### **Phase 1: Foundation (Project 1a)**
- US Census API setup and authentication
- State-level demographic data acquisition
- Basic choropleth mapping with GeoPandas
- Statistical analysis and correlation studies
- Professional map design and color theory

### **Phase 2: Advanced Analysis (Project 1b)**
- County-level data (3,100+ counties)
- Machine learning clustering (K-means, Hierarchical, DBSCAN)
- Principal Component Analysis (PCA)
- Spatial autocorrelation analysis (LISA - Local Moran's I)
- Interactive visualizations with Plotly and Folium

### **Phase 3: Real-World Application (Project 1c)**
- CDC WONDER health data integration
- Environmental justice analysis
- Policy-ready visualizations and dashboards
- Research-quality outputs
- Actionable recommendations

---

## 🎯 **Learning Objectives**

By completing this project series, you will:

### **Technical Skills**
- ✅ Master US Census API for demographic data
- ✅ Apply machine learning to geospatial data
- ✅ Perform spatial autocorrelation analysis
- ✅ Create interactive maps and dashboards
- ✅ Integrate multiple data sources (Census + Health)

### **Analytical Skills**
- ✅ Identify demographic clusters and patterns
- ✅ Analyze spatial relationships and hot spots
- ✅ Correlate health outcomes with demographics
- ✅ Apply environmental justice frameworks
- ✅ Generate policy-relevant insights

### **Professional Skills**
- ✅ Create research-quality visualizations
- ✅ Build stakeholder-ready dashboards
- ✅ Write actionable policy recommendations
- ✅ Present complex geospatial analysis
- ✅ Integrate multiple analytical approaches

---

## 📊 **Key Datasets**

- **US Census Bureau**: American Community Survey (ACS) 5-year estimates
- **Census TIGER/Line**: Administrative boundaries (states, counties)
- **CDC WONDER**: Mortality and health outcome data
- **Demographics**: Population, income, education, housing, employment
- **Health Indicators**: Mortality rates, health disparities

---

## 🛠️ **Technical Requirements**

### **Required Packages**
```bash
# Core geospatial
geopandas
folium
contextily

# Machine learning
scikit-learn
plotly

# Spatial analysis
libpysal
esda

# Visualization
matplotlib
seaborn
mapclassify
```

### **Environment Setup**

#### Option 1: Google Colab (Recommended)
- No setup required! Packages install automatically
- Free GPU/TPU access available
- Click any Colab badge above to start

#### Option 2: Local Environment
```bash
# Clone repository
git clone https://github.com/SanjeevaRDodlapati/GeoSpatialAI.git
cd GeoSpatialAI

# Create conda environment
conda env create -f environment_geo.yml
conda activate geo_env

# Or install with pip
pip install -r requirements.txt
```

---

## 📈 **Project Outcomes**

### **Visualizations Created**
- **Professional choropleth maps** showing demographic patterns
- **Interactive dashboards** with multiple variable exploration
- **Machine learning cluster maps** identifying county typologies
- **Spatial autocorrelation maps** showing geographic clustering
- **Health disparity visualizations** for policy analysis

### **Analysis Outputs**
- **Demographic cluster identification** across US counties
- **Spatial pattern analysis** with statistical significance
- **Health outcome correlations** with demographic factors
- **Environmental justice assessments** identifying vulnerable areas
- **Policy recommendations** based on data-driven insights

### **Skills Gained**
- **Professional geospatial analysis** capabilities
- **Machine learning** applied to geographic data
- **Spatial statistics** and autocorrelation analysis
- **Public health data integration** and analysis
- **Policy-relevant research** skills

---

## 🎓 **Target Audience**

- **GIS Analysts** seeking to integrate machine learning
- **Data Scientists** interested in geospatial applications
- **Public Health Researchers** working with spatial data
- **Policy Analysts** requiring demographic insights
- **Graduate Students** in geography, public policy, or data science

---

## 📝 **Citation**

If you use this tutorial series in your research or teaching, please cite:

```
Dodlapati, S. R. (2025). Census Analysis & Demographic Mapping Tutorial Series. 
GeoSpatialAI Project. GitHub. https://github.com/SanjeevaRDodlapati/GeoSpatialAI
```

---

## 📞 **Support**

- **Issues**: Open an issue on GitHub for technical problems
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Documentation**: Check the docs/ folder for additional resources

**Ready to explore American demographics with data science? Click a Colab badge above to start! 🚀**
