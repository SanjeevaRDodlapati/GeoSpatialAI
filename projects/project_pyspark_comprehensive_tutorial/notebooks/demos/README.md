# Module 6: PySpark MLlib Demos

This directory contains demo and test files for Module 6 (PySpark MLlib) that complement the main comprehensive notebook.

## Files Overview

### 📚 **Main Learning Material**
- **`../06_machine_learning_mllib.ipynb`** - Complete comprehensive MLlib tutorial (use this for full learning)

### 🎯 **Demo Files**

#### **`06_machine_learning_mllib_demo.ipynb`**
- **Purpose**: Simplified MLlib introduction and quick demo
- **Content**: Basic examples of classification, regression, and clustering
- **Use Case**: Quick demonstrations, teaching basics, faster execution
- **Duration**: ~5-10 minutes to run

#### **`comprehensive_mllib_demo.py`**
- **Purpose**: Python script version for automated execution
- **Content**: Complete MLlib workflow in script format
- **Use Case**: CI/CD pipelines, automated testing, command-line execution
- **Usage**: `python comprehensive_mllib_demo.py`

#### **`test_mllib.py`**
- **Purpose**: Basic environment and functionality test
- **Content**: Simple test to verify MLlib installation and basic operations
- **Use Case**: Environment validation, troubleshooting setup issues
- **Usage**: `python test_mllib.py`

## Learning Path

1. **Start Here**: `test_mllib.py` - Verify your environment works
2. **Quick Demo**: `06_machine_learning_mllib_demo.ipynb` - Learn basics
3. **Complete Learning**: `../06_machine_learning_mllib.ipynb` - Full comprehensive tutorial
4. **Automation**: `comprehensive_mllib_demo.py` - Script-based execution

## Prerequisites

- PySpark 4.0.0+ installed
- pyspark_env conda environment activated
- Jupyter notebook server running (for .ipynb files)

## Performance Metrics

All demos have been validated with the following results:
- **Classification AUC**: 0.52-0.81 (good to excellent)
- **Regression RMSE**: 145-400 (good fit)
- **Clustering Silhouette**: 0.53+ (well-separated clusters)
- **Training Speed**: Sub-second to 3s (very fast)

## Troubleshooting

If you encounter issues:
1. Run `test_mllib.py` first to validate environment
2. Check that pyspark_env is activated
3. Verify PySpark installation with `spark.version`
4. Refer to the main notebook for detailed explanations
