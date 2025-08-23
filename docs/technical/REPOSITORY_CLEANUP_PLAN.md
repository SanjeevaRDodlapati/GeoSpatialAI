# 🧹 Repository Cleanup Action Plan

## Phase 1: Immediate Cleanup (Priority 1)

### 1.1 📁 Create New Directory Structure

```bash
# Create main source directories
mkdir -p src/{api,web,analysis,utils}
mkdir -p web/{templates,static/{css,js,images},demos}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p scripts
mkdir -p docs/{user_guide,developer,project_history,assets}
mkdir -p configs
mkdir -p deployment/{docker,kubernetes,logs/deployment_summaries}
mkdir -p data/{cache,processed,temp}
mkdir -p logs
```

### 1.2 🗂️ File Consolidation & Migration

#### **Core Source Files**
```bash
# API Integration
mv working_real_api_wrappers.py → src/api/conservation_apis.py
mv api_wrappers.py → src/api/legacy_wrappers.py (for reference)

# Web Interface
mv traced_web_server.py → src/web/server.py
mv fixed_web_server.py → src/web/legacy_server.py (archive)

# Analysis Modules
# Extract analysis functions from existing files into:
# - src/analysis/conservation_analyzer.py
# - src/analysis/threat_scanner.py
# - src/analysis/species_monitor.py
```

#### **Web Templates**
```bash
# Primary Dashboard
mv dashboard_real_map.html → web/templates/dashboard.html

# Archive Others
mkdir -p docs/project_history/old_dashboards
mv dashboard_complete.html → docs/project_history/old_dashboards/
mv dashboard_step1.html → docs/project_history/old_dashboards/
mv dashboard_step2.html → docs/project_history/old_dashboards/
mv debug_test.html → web/demos/debug_interface.html
mv templates/conservation_dashboard.html → docs/project_history/old_dashboards/
```

#### **Test Files**
```bash
mv test_global_capability.py → tests/integration/
mv test_final_system.py → tests/integration/
mv test_real_api_connections.py → tests/integration/
mv verify_real_apis.py → tests/integration/
mv test_environment.py → scripts/verify_environment.py
```

#### **Demo & Utility Scripts**
```bash
mv simple_conservation_demo.py → scripts/
mv frontend_triggering_demo.py → scripts/
mv conservation_web_interface.py → scripts/
mv web_demo_server.py → web/demos/
mv api_key_setup_guide.py → scripts/setup_api_keys.py
mv fix_real_apis.py → scripts/
```

#### **Configuration Files**
```bash
mv api_keys_template.env → configs/
cp .env → configs/development.env.example
```

#### **Documentation Reorganization**
```bash
# Core Documentation
mv GLOBAL_SYSTEM_README.md → docs/user_guide/getting_started.md
mv GLOBAL_TRANSFORMATION_SUMMARY.md → docs/project_history/

# Project History
mkdir -p docs/project_history/{phase_reports,summaries,guides}
mv PHASE*.md → docs/project_history/phase_reports/
mv *_SUMMARY.md → docs/project_history/summaries/
mv *_GUIDE.md → docs/project_history/guides/
mv DEMONSTRATION_*.md → docs/project_history/summaries/
mv INTERFACE_*.md → docs/project_history/summaries/
mv API_*.md → docs/project_history/guides/

# System Documentation
mv SYSTEM_REVIEW.md → docs/developer/system_architecture.md
mv CONTRIBUTING.md → docs/developer/contributing.md
```

#### **Deployment Files**
```bash
mkdir -p deployment/logs/deployment_summaries
mv deployment_summary_*.json → deployment/logs/deployment_summaries/
```

#### **Archive Unused Files**
```bash
mkdir -p docs/project_history/archived_files
mv system_status_report.py → docs/project_history/archived_files/
mv Untitled.ipynb → docs/project_history/archived_files/
```

## Phase 2: Code Refactoring (Priority 2)

### 2.1 🔧 Create Modular API Clients

#### **src/api/base_client.py**
```python
from abc import ABC, abstractmethod
import aiohttp
import os
from typing import Optional, Dict, Any

class BaseAPIClient(ABC):
    \"\"\"Base class for all API clients\"\"\"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    @abstractmethod
    async def fetch_data(self, **kwargs) -> Dict[str, Any]:
        \"\"\"Fetch data from the API\"\"\"
        pass
```

#### **src/api/gbif_client.py**
```python
from .base_client import BaseAPIClient
from typing import Dict, Any, Optional

class GBIFClient(BaseAPIClient):
    \"\"\"GBIF API client for species occurrence data\"\"\"
    
    BASE_URL = \"https://api.gbif.org/v1/occurrence/search\"
    
    def __init__(self):
        super().__init__()  # GBIF doesn't require API key
    
    async def fetch_species_data(self, lat: float, lng: float, 
                                radius_km: int = 10) -> Dict[str, Any]:
        \"\"\"Fetch species occurrence data for location\"\"\"
        params = {
            'decimalLatitude': lat,
            'decimalLongitude': lng,
            'radius': radius_km * 1000,
            'limit': 20
        }
        
        async with self.session.get(self.BASE_URL, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f\"GBIF API error: {response.status}\")
```

### 2.2 🌐 Refactor Web Server

#### **src/web/server.py**
```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from pathlib import Path
from .handlers import ConservationHandlers

class ConservationWebServer(BaseHTTPRequestHandler):
    \"\"\"Main web server for Global Conservation AI\"\"\"
    
    def __init__(self, *args, **kwargs):
        self.handlers = ConservationHandlers()
        self.template_dir = Path(__file__).parent.parent.parent / \"web\" / \"templates\"
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/' or self.path == '/dashboard':
            self.serve_dashboard()
        elif self.path.startswith('/api/'):
            self.handle_api_get()
        else:
            self.send_error(404)
    
    def serve_dashboard(self):
        \"\"\"Serve the main dashboard\"\"\"
        template_path = self.template_dir / \"dashboard.html\"
        with open(template_path, 'r') as f:
            content = f.read()
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content.encode())
```

### 2.3 📋 Configuration Management

#### **src/utils/config.py**
```python
import os
from pathlib import Path
from typing import Dict, Optional

class Config:
    \"\"\"Configuration management for the application\"\"\"
    
    def __init__(self, env_file: Optional[str] = None):
        self.env_file = env_file or self._find_env_file()
        self._load_environment()
    
    def _find_env_file(self) -> str:
        \"\"\"Find the appropriate .env file\"\"\"
        current_dir = Path(__file__).parent.parent.parent
        env_files = [
            current_dir / \".env\",
            current_dir / \"configs\" / \"development.env\",
            current_dir / \"configs\" / \"production.env\"
        ]
        
        for env_file in env_files:
            if env_file.exists():
                return str(env_file)
        
        raise FileNotFoundError(\"No environment file found\")
    
    def get_api_key(self, service: str) -> Optional[str]:
        \"\"\"Get API key for a specific service\"\"\"
        key_mapping = {
            'gbif': None,  # GBIF doesn't require API key
            'nasa_firms': 'NASA_FIRMS_MAP_KEY',
            'ebird': 'EBIRD_API_KEY',
            'sentinel': 'SENTINEL_HUB_API_KEY'
        }
        
        env_var = key_mapping.get(service.lower())
        return os.getenv(env_var) if env_var else None
```

## Phase 3: Testing & Documentation (Priority 3)

### 3.1 🧪 Test Suite Setup

#### **tests/unit/test_api_clients.py**
```python
import pytest
import asyncio
from src.api.gbif_client import GBIFClient

class TestGBIFClient:
    \"\"\"Test GBIF API client\"\"\"
    
    @pytest.mark.asyncio
    async def test_fetch_species_data(self):
        \"\"\"Test species data fetching\"\"\"
        async with GBIFClient() as client:
            data = await client.fetch_species_data(-18.9333, 48.4167)
            assert 'count' in data
            assert 'results' in data
            assert isinstance(data['count'], int)
```

#### **tests/integration/test_global_functionality.py**
```python
import pytest
from src.web.server import ConservationWebServer

class TestGlobalFunctionality:
    \"\"\"Test global conservation capabilities\"\"\"
    
    def test_global_coordinates(self):
        \"\"\"Test system works with global coordinates\"\"\"
        test_locations = [
            (-18.9369, 47.5222, \"Madagascar\"),
            (-3.4653, -62.2159, \"Amazon\"),
            (44.4280, -110.5885, \"Yellowstone\")
        ]
        
        for lat, lng, name in test_locations:
            # Test coordinate validation
            assert -90 <= lat <= 90
            assert -180 <= lng <= 180
```

### 3.2 📚 Documentation Updates

#### **docs/user_guide/getting_started.md**
```markdown
# Getting Started with Global Conservation AI

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/YourUsername/GeoSpatialAI.git
   cd GeoSpatialAI
   ```

2. **Set up environment**
   ```bash
   python scripts/setup_environment.py
   ```

3. **Configure API keys**
   ```bash
   python scripts/setup_api_keys.py
   ```

4. **Run the application**
   ```bash
   python -m src.web.server
   ```

## System Requirements
- Python 3.8+
- 8GB RAM minimum
- Internet connection for real-time data
```

## Phase 4: Advanced Features (Priority 4)

### 4.1 📊 Logging & Monitoring

#### **src/utils/logging.py**
```python
import logging
import sys
from pathlib import Path

def setup_logging(log_level: str = \"INFO\") -> logging.Logger:
    \"\"\"Set up application logging\"\"\"
    
    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).parent.parent.parent / \"logs\"
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / \"application.log\"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)
```

### 4.2 🐳 Containerization

#### **deployment/docker/Dockerfile**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gdal-bin \\
    libgdal-dev \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY web/ ./web/
COPY configs/ ./configs/

# Expose port
EXPOSE 8000

# Run application
CMD [\"python\", \"-m\", \"src.web.server\"]
```

## Benefits of This Cleanup

### ✅ **Immediate Benefits**
- Reduced root directory clutter (48 → 15 files)
- Clear separation of concerns
- Easier navigation and maintenance
- Professional project structure

### ✅ **Long-term Benefits**
- Scalable architecture
- Easy to add new features
- Better testing capabilities
- Simplified deployment
- Clear documentation structure

### ✅ **Development Benefits**
- Consistent code organization
- Reusable components
- Better error handling
- Comprehensive logging
- Professional development workflow

## Implementation Timeline

- **Week 1**: Phase 1 (File organization)
- **Week 2**: Phase 2 (Code refactoring)
- **Week 3**: Phase 3 (Testing & documentation)
- **Week 4**: Phase 4 (Advanced features)

This cleanup will transform the repository from a research project into a professional, maintainable codebase ready for production deployment.
