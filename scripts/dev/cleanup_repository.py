#!/usr/bin/env python3
"""
🧹 Repository Cleanup Automation Script
======================================
Automates the reorganization of GeoSpatialAI repository structure.
"""

import os
import shutil
from pathlib import Path
import json
from datetime import datetime

class RepositoryCleanup:
    """Automates repository cleanup and reorganization"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.backup_path = self.repo_path / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.cleanup_log = []
    
    def log_action(self, action: str, details: str = ""):
        """Log cleanup actions"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        }
        self.cleanup_log.append(entry)
        print(f"✅ {action}: {details}")
    
    def create_backup(self):
        """Create backup of current state"""
        print(f"📦 Creating backup at {self.backup_path}")
        
        # Create backup directory
        self.backup_path.mkdir(exist_ok=True)
        
        # Backup critical files
        critical_files = [
            "dashboard_real_map.html",
            "traced_web_server.py", 
            "working_real_api_wrappers.py",
            "test_global_capability.py",
            ".env"
        ]
        
        for file in critical_files:
            if (self.repo_path / file).exists():
                shutil.copy2(self.repo_path / file, self.backup_path / file)
                self.log_action("BACKUP", f"Backed up {file}")
    
    def create_directory_structure(self):
        """Create the new directory structure"""
        directories = [
            "src/api",
            "src/web", 
            "src/analysis",
            "src/utils",
            "web/templates",
            "web/static/css",
            "web/static/js", 
            "web/static/images",
            "web/demos",
            "tests/unit",
            "tests/integration", 
            "tests/fixtures",
            "scripts",
            "docs/user_guide",
            "docs/developer",
            "docs/project_history/phase_reports",
            "docs/project_history/summaries",
            "docs/project_history/guides",
            "docs/project_history/old_dashboards",
            "docs/project_history/archived_files",
            "docs/assets",
            "configs",
            "deployment/docker",
            "deployment/kubernetes", 
            "deployment/logs/deployment_summaries",
            "data/cache",
            "data/processed",
            "data/temp",
            "logs"
        ]
        
        for dir_path in directories:
            full_path = self.repo_path / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            self.log_action("CREATE_DIR", dir_path)
        
        # Create __init__.py files for Python packages
        init_files = [
            "src/__init__.py",
            "src/api/__init__.py", 
            "src/web/__init__.py",
            "src/analysis/__init__.py",
            "src/utils/__init__.py"
        ]
        
        for init_file in init_files:
            (self.repo_path / init_file).touch()
            self.log_action("CREATE_INIT", init_file)
    
    def migrate_files(self):
        """Migrate files to new structure"""
        
        migrations = {
            # Core source files
            "working_real_api_wrappers.py": "src/api/conservation_apis.py",
            "traced_web_server.py": "src/web/server.py",
            "api_wrappers.py": "docs/project_history/archived_files/legacy_wrappers.py",
            
            # Web templates
            "dashboard_real_map.html": "web/templates/dashboard.html",
            "dashboard_complete.html": "docs/project_history/old_dashboards/dashboard_complete.html",
            "dashboard_step1.html": "docs/project_history/old_dashboards/dashboard_step1.html", 
            "dashboard_step2.html": "docs/project_history/old_dashboards/dashboard_step2.html",
            "debug_test.html": "web/demos/debug_interface.html",
            "templates/conservation_dashboard.html": "docs/project_history/old_dashboards/conservation_dashboard.html",
            
            # Test files
            "test_global_capability.py": "tests/integration/test_global_capability.py",
            "test_final_system.py": "tests/integration/test_final_system.py",
            "test_real_api_connections.py": "tests/integration/test_real_api_connections.py",
            "verify_real_apis.py": "tests/integration/verify_real_apis.py",
            "test_environment.py": "scripts/verify_environment.py",
            
            # Scripts
            "simple_conservation_demo.py": "scripts/simple_conservation_demo.py",
            "frontend_triggering_demo.py": "scripts/frontend_triggering_demo.py",
            "conservation_web_interface.py": "scripts/conservation_web_interface.py",
            "web_demo_server.py": "web/demos/simple_server.py",
            "api_key_setup_guide.py": "scripts/setup_api_keys.py",
            "fix_real_apis.py": "scripts/fix_real_apis.py",
            
            # Configuration
            "api_keys_template.env": "configs/api_keys_template.env",
            
            # Documentation 
            "GLOBAL_SYSTEM_README.md": "docs/user_guide/getting_started.md",
            "GLOBAL_TRANSFORMATION_SUMMARY.md": "docs/project_history/transformation_summary.md",
            "SYSTEM_REVIEW.md": "docs/developer/system_architecture.md",
            
            # Archive unused
            "system_status_report.py": "docs/project_history/archived_files/system_status_report.py",
            "Untitled.ipynb": "docs/project_history/archived_files/Untitled.ipynb"
        }
        
        for source, destination in migrations.items():
            source_path = self.repo_path / source
            dest_path = self.repo_path / destination
            
            if source_path.exists():
                # Create destination directory if needed
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Move file
                shutil.move(str(source_path), str(dest_path))
                self.log_action("MIGRATE", f"{source} → {destination}")
            else:
                self.log_action("SKIP", f"{source} (not found)")
    
    def migrate_documentation(self):
        """Migrate documentation files to organized structure"""
        
        doc_migrations = {
            # Phase reports
            "PHASE1_COMPLETION_SUMMARY.md": "docs/project_history/phase_reports/",
            "PHASE1_PROJECT_DESCRIPTIONS.md": "docs/project_history/phase_reports/",
            "PHASE2_COMPLETION_REPORT.md": "docs/project_history/phase_reports/",
            "PHASE2_MADAGASCAR_SPECIALIZATION.md": "docs/project_history/phase_reports/",
            "PHASE3A_COMPLETION_SUMMARY.md": "docs/project_history/phase_reports/",
            "PHASE3_ROADMAP.md": "docs/project_history/phase_reports/",
            "PHASE4A_STEP_BY_STEP_IMPLEMENTATION.md": "docs/project_history/phase_reports/",
            "PHASE4_AI_AGENT_TECHNICAL_PLAN.md": "docs/project_history/phase_reports/",
            
            # Summaries
            "COMPLETE_REAL_WORLD_INTEGRATION_SUMMARY.md": "docs/project_history/summaries/",
            "DEMONSTRATION_COMPLETE_SUMMARY.md": "docs/project_history/summaries/",
            "INTERFACE_TESTING_REPORT.md": "docs/project_history/summaries/",
            "EVALUATION_FEEDBACK_ANALYSIS_REPORT.md": "docs/project_history/summaries/",
            "REALTIME_INTEGRATION_COMPLETION.md": "docs/project_history/summaries/",
            
            # Guides
            "API_ACCESS_GUIDE.md": "docs/project_history/guides/",
            "API_CONFIGURATION_SUMMARY.md": "docs/project_history/guides/",
            "FRONTEND_DEMONSTRATION_GUIDE.md": "docs/project_history/guides/",
            "REAL_WORLD_DATA_TRIGGERING_GUIDE.md": "docs/project_history/guides/",
            "ENVIRONMENT_MIGRATION_GUIDE.md": "docs/project_history/guides/",
            "FRONTEND_INTERFACE_DESIGN_PLAN.md": "docs/project_history/guides/",
            "INTERACTIVE_FRONTEND_IMPLEMENTATION_PLAN.md": "docs/project_history/guides/",
            "ML_MODEL_INTEGRATION_PLAN.md": "docs/project_history/guides/",
            "PUBLIC_DATASET_INTEGRATION_STRATEGY.md": "docs/project_history/guides/",
            "AI_AGENT_APPLICATIONS_ROADMAP.md": "docs/project_history/guides/",
            "AGENTIC_AI_COMPLETION_GUIDE.md": "docs/project_history/guides/",
            "AGENT_DEMO_EXAMPLES.md": "docs/project_history/guides/"
        }
        
        for source, dest_dir in doc_migrations.items():
            source_path = self.repo_path / source
            dest_path = self.repo_path / dest_dir / source
            
            if source_path.exists():
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source_path), str(dest_path))
                self.log_action("MIGRATE_DOC", f"{source} → {dest_dir}")
    
    def migrate_deployment_files(self):
        """Migrate deployment-related files"""
        
        # Move deployment summaries
        deployment_pattern = "deployment_summary_*.json"
        deployment_files = list(self.repo_path.glob(deployment_pattern))
        
        dest_dir = self.repo_path / "deployment/logs/deployment_summaries"
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        for file in deployment_files:
            dest_file = dest_dir / file.name
            shutil.move(str(file), str(dest_file))
            self.log_action("MIGRATE_DEPLOY", f"{file.name} → deployment/logs/deployment_summaries/")
    
    def update_imports_and_paths(self):
        """Update import statements and file paths in migrated files"""
        
        # Update main server file
        server_file = self.repo_path / "src/web/server.py"
        if server_file.exists():
            content = server_file.read_text()
            
            # Update imports
            content = content.replace(
                "from working_real_api_wrappers import",
                "from ..api.conservation_apis import"
            )
            
            # Update template path
            content = content.replace(
                "'dashboard_real_map.html'",
                "'../../web/templates/dashboard.html'"
            )
            
            server_file.write_text(content)
            self.log_action("UPDATE_IMPORTS", "Updated server.py imports and paths")
    
    def create_new_main_files(self):
        """Create new main application files"""
        
        # Create setup.py
        setup_py = self.repo_path / "setup.py"
        setup_content = '''#!/usr/bin/env python3
"""Setup script for Global Conservation AI"""

from setuptools import setup, find_packages

setup(
    name="global-conservation-ai",
    version="2.0.0",
    description="Global Conservation AI System for real-time biodiversity monitoring",
    author="Sanjeeva Dodlapati",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.8.0",
        "requests>=2.28.0",
        "python-dotenv>=0.19.0",
    ],
    entry_points={
        "console_scripts": [
            "conservation-ai=web.server:main",
        ],
    },
)
'''
        setup_py.write_text(setup_content)
        self.log_action("CREATE", "setup.py")
        
        # Create main application runner
        main_py = self.repo_path / "src/main.py"
        main_content = '''#!/usr/bin/env python3
"""Main application entry point for Global Conservation AI"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.web.server import run_server

if __name__ == "__main__":
    run_server()
'''
        main_py.write_text(main_content)
        self.log_action("CREATE", "src/main.py")
    
    def generate_cleanup_report(self):
        """Generate cleanup report"""
        
        report = {
            "cleanup_timestamp": datetime.now().isoformat(),
            "backup_location": str(self.backup_path),
            "actions_performed": self.cleanup_log,
            "summary": {
                "total_actions": len(self.cleanup_log),
                "files_migrated": len([a for a in self.cleanup_log if a["action"] == "MIGRATE"]),
                "directories_created": len([a for a in self.cleanup_log if a["action"] == "CREATE_DIR"]),
                "documentation_organized": len([a for a in self.cleanup_log if a["action"] == "MIGRATE_DOC"])
            }
        }
        
        report_file = self.repo_path / "cleanup_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log_action("REPORT", f"Cleanup report saved to {report_file}")
        
        return report
    
    def run_cleanup(self):
        """Execute the complete cleanup process"""
        
        print("🧹 Starting Global Conservation AI Repository Cleanup")
        print("=" * 60)
        
        try:
            # Phase 1: Backup and setup
            self.create_backup()
            self.create_directory_structure()
            
            # Phase 2: File migration
            self.migrate_files()
            self.migrate_documentation()
            self.migrate_deployment_files()
            
            # Phase 3: Update and fix
            self.update_imports_and_paths()
            self.create_new_main_files()
            
            # Phase 4: Report
            report = self.generate_cleanup_report()
            
            print("\\n" + "=" * 60)
            print("🎉 Repository cleanup completed successfully!")
            print(f"📊 Summary:")
            print(f"   • Total actions: {report['summary']['total_actions']}")
            print(f"   • Files migrated: {report['summary']['files_migrated']}")
            print(f"   • Directories created: {report['summary']['directories_created']}")
            print(f"   • Documentation files organized: {report['summary']['documentation_organized']}")
            print(f"📦 Backup created at: {self.backup_path}")
            print(f"📋 Full report: cleanup_report.json")
            
            print("\\n🚀 Next steps:")
            print("   1. Test the application: python src/main.py")
            print("   2. Run tests: python -m pytest tests/")
            print("   3. Update README.md with new structure")
            print("   4. Commit changes to git")
            
        except Exception as e:
            print(f"❌ Error during cleanup: {e}")
            print(f"🔄 Restore from backup: {self.backup_path}")
            raise

def main():
    """Main function to run cleanup"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Clean up and reorganize GeoSpatialAI repository")
    parser.add_argument("--repo-path", default=".", help="Path to repository (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print("This would reorganize the repository structure...")
        # TODO: Implement dry run logic
        return
    
    cleanup = RepositoryCleanup(args.repo_path)
    cleanup.run_cleanup()

if __name__ == "__main__":
    main()
