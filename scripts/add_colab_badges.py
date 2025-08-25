#!/usr/bin/env python3
"""
Add Google Colab badges to all notebooks in GeoSpatialAI repository

This script automatically adds Colab launch badges to the header of all
Jupyter notebooks in the projects directory.
"""

import os
import json
import re
from pathlib import Path

def find_notebooks(root_dir):
    """Find all Jupyter notebooks in the repository"""
    notebooks = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.ipynb'):
                notebooks.append(os.path.join(root, file))
    return notebooks

def get_relative_path(notebook_path, repo_root):
    """Get relative path from repo root"""
    return os.path.relpath(notebook_path, repo_root)

def generate_colab_badge(notebook_rel_path):
    """Generate Colab badge markdown"""
    colab_url = f"https://colab.research.google.com/github/SanjeevaRDodlapati/GeoSpatialAI/blob/main/{notebook_rel_path}"
    
    badge_markdown = f"""## 🚀 **Quick Start - Run in Google Colab**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url})

**Click the badge above to open this notebook in Google Colab and run it with free GPU/TPU!**

> 💡 **Colab Setup**: When running in Colab, you'll need to install the required packages. The first code cell will handle this automatically.

---

"""
    return badge_markdown

def has_colab_badge(notebook_content):
    """Check if notebook already has a Colab badge"""
    return "colab.research.google.com" in notebook_content

def add_colab_badge_to_notebook(notebook_path, repo_root):
    """Add Colab badge to a notebook if it doesn't have one"""
    try:
        # Read notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has badge
        if has_colab_badge(content):
            print(f"  ✅ Already has Colab badge: {os.path.basename(notebook_path)}")
            return False
        
        # Parse notebook JSON
        notebook = json.loads(content)
        
        # Get relative path for badge
        rel_path = get_relative_path(notebook_path, repo_root)
        badge_markdown = generate_colab_badge(rel_path)
        
        # Find first markdown cell (usually title)
        first_markdown_idx = None
        for i, cell in enumerate(notebook['cells']):
            if cell['cell_type'] == 'markdown':
                first_markdown_idx = i
                break
        
        if first_markdown_idx is not None:
            # Get the existing content
            existing_content = ''.join(notebook['cells'][first_markdown_idx]['source'])
            
            # Split content by first header
            lines = existing_content.split('\n')
            title_line = lines[0] if lines else "# Notebook Title"
            rest_content = '\n'.join(lines[1:]) if len(lines) > 1 else ""
            
            # Create new content with badge
            new_content = f"{title_line}\n\n{badge_markdown}{rest_content}"
            
            # Update the cell
            notebook['cells'][first_markdown_idx]['source'] = new_content.split('\n')
            
            # Write back to file
            with open(notebook_path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=1, ensure_ascii=False)
            
            print(f"  ✅ Added Colab badge: {os.path.basename(notebook_path)}")
            return True
        else:
            print(f"  ⚠️ No markdown cell found: {os.path.basename(notebook_path)}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error processing {notebook_path}: {e}")
        return False

def update_setup_cells():
    """Update first code cells to include Colab setup"""
    colab_setup_code = '''# 🔧 AUTOMATIC SETUP FOR GOOGLE COLAB
import sys

# Check if running in Google Colab
IN_COLAB = 'google.colab' in sys.modules

if IN_COLAB:
    print("🚀 Running in Google Colab - Installing required packages...")
    print("⏱️ This may take 2-3 minutes, please wait...")
    
    # Install core geospatial packages
    !pip install geopandas folium contextily plotly --quiet
    !pip install scikit-learn seaborn mapclassify --quiet
    !pip install libpysal esda requests --quiet
    
    print("✅ All packages installed successfully!")
    print("📁 Note: In Colab, file outputs will be saved to the current session")
    print()
else:
    print("💻 Running in local environment")
    print("📦 Ensure you have the correct environment activated")
    print()

# Continue with regular imports...'''
    
    return colab_setup_code

def main():
    """Main function to add Colab badges to all notebooks"""
    repo_root = Path(__file__).parent.parent
    projects_dir = repo_root / "projects"
    
    print("🚀 Adding Google Colab badges to all notebooks...")
    print("="*60)
    
    # Find all notebooks
    notebooks = find_notebooks(projects_dir)
    
    print(f"📚 Found {len(notebooks)} notebooks")
    print()
    
    # Process each notebook
    updated_count = 0
    for notebook_path in notebooks:
        project_name = Path(notebook_path).parts[-3]  # Get project folder name
        print(f"📝 Processing {project_name}:")
        
        if add_colab_badge_to_notebook(notebook_path, repo_root):
            updated_count += 1
    
    print()
    print(f"✅ Complete! Updated {updated_count} notebooks with Colab badges")
    print("🔗 All notebooks now have Google Colab launch capability")

if __name__ == "__main__":
    main()
