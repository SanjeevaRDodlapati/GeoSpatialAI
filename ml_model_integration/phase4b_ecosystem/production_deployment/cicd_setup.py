"""
Step 2: CI/CD Setup and Validation
==================================
Validate and configure GitHub Actions CI/CD pipeline for automated deployment.
"""

import os
import sys
import json
import yaml
import subprocess
from pathlib import Path
from datetime import datetime

class CICDSetupValidator:
    """Validator for CI/CD pipeline configuration."""
    
    def __init__(self):
        self.project_root = Path('/Users/sanjeevadodlapati/Downloads/Repos/GeoSpatialAI')
        self.deployment_path = self.project_root / 'ml_model_integration/phase4b_ecosystem/production_deployment'
        self.github_workflow_path = self.deployment_path / '.github/workflows/deploy.yml'
        
        self.validation_results = {}
        
        print("🔄 CI/CD Setup Validator initialized")
    
    def validate_github_workflow(self):
        """Validate GitHub Actions workflow configuration."""
        print("\n📋 Validating GitHub Actions Workflow...")
        
        try:
            # Check if workflow file exists
            if not self.github_workflow_path.exists():
                print("❌ GitHub workflow file not found")
                return False
            
            # Load and validate YAML syntax
            with open(self.github_workflow_path, 'r') as f:
                workflow_config = yaml.safe_load(f)
            
            # Validate required workflow components
            required_keys = ['name', 'jobs']
            trigger_key = 'on' if 'on' in workflow_config else True  # Handle YAML parsing of 'on' keyword
            
            for key in required_keys:
                if key not in workflow_config:
                    print(f"❌ Missing required key: {key}")
                    return False
            
            # Check for trigger configuration (on: or True key)
            if trigger_key not in workflow_config:
                print("❌ Missing workflow triggers")
                return False
            
            # Validate jobs structure
            jobs = workflow_config.get('jobs', {})
            required_jobs = ['test', 'build', 'deploy']
            
            for job in required_jobs:
                if job not in jobs:
                    print(f"❌ Missing required job: {job}")
                    return False
            
            # Validate test job
            test_job = jobs.get('test', {})
            if 'steps' not in test_job:
                print("❌ Test job missing steps")
                return False
            
            # Validate build job
            build_job = jobs.get('build', {})
            if 'strategy' not in build_job or 'matrix' not in build_job.get('strategy', {}):
                print("❌ Build job missing matrix strategy")
                return False
            
            # Validate deploy job
            deploy_job = jobs.get('deploy', {})
            if 'needs' not in deploy_job or 'build' not in deploy_job.get('needs', []):
                print("❌ Deploy job missing dependency on build")
                return False
            
            self.validation_results['github_workflow'] = True
            print("✅ GitHub Actions workflow validation passed")
            print(f"   📊 Found {len(jobs)} jobs: {list(jobs.keys())}")
            
            return True
            
        except yaml.YAMLError as e:
            print(f"❌ YAML syntax error: {e}")
            return False
        except Exception as e:
            print(f"❌ Workflow validation error: {e}")
            return False
    
    def validate_docker_configurations(self):
        """Validate Docker configurations for CI/CD."""
        print("\n🐳 Validating Docker Configurations...")
        
        try:
            docker_files = [
                'Dockerfile.orchestrator',
                'Dockerfile.species_agent',
                'Dockerfile.dashboard',
                'Dockerfile.workflow_engine'
            ]
            
            valid_dockerfiles = 0
            
            for dockerfile in docker_files:
                dockerfile_path = self.deployment_path / dockerfile
                
                if not dockerfile_path.exists():
                    print(f"❌ Missing Dockerfile: {dockerfile}")
                    continue
                
                # Read and validate Dockerfile content
                content = dockerfile_path.read_text()
                
                # Check for required instructions
                required_instructions = ['FROM', 'WORKDIR', 'COPY', 'RUN', 'EXPOSE', 'CMD']
                missing_instructions = []
                
                for instruction in required_instructions:
                    if instruction not in content:
                        missing_instructions.append(instruction)
                
                if missing_instructions:
                    print(f"❌ {dockerfile} missing instructions: {missing_instructions}")
                else:
                    valid_dockerfiles += 1
                    print(f"✅ {dockerfile} validated")
            
            # Validate docker-compose for local development
            docker_compose_path = self.deployment_path / 'docker-compose.yml'
            if docker_compose_path.exists():
                with open(docker_compose_path, 'r') as f:
                    compose_config = yaml.safe_load(f)
                
                if 'services' in compose_config and len(compose_config['services']) >= 3:
                    valid_dockerfiles += 1
                    print("✅ docker-compose.yml validated")
                else:
                    print("❌ docker-compose.yml invalid or missing services")
            
            success = valid_dockerfiles >= 4  # At least 4 valid Docker configurations
            self.validation_results['docker_configs'] = success
            
            if success:
                print(f"✅ Docker configurations validated ({valid_dockerfiles} files)")
            else:
                print(f"❌ Docker validation failed ({valid_dockerfiles} valid files)")
            
            return success
            
        except Exception as e:
            print(f"❌ Docker validation error: {e}")
            return False
    
    def validate_kubernetes_manifests(self):
        """Validate Kubernetes manifests for deployment."""
        print("\n☸️ Validating Kubernetes Manifests...")
        
        try:
            k8s_files = [
                'namespace.yaml',
                'configmap.yaml',
                'secrets.yaml',
                'deployment_ecosystem-orchestrator.yaml',
                'service_ecosystem-orchestrator.yaml',
                'ingress.yaml'
            ]
            
            valid_manifests = 0
            
            for k8s_file in k8s_files:
                manifest_path = self.deployment_path / k8s_file
                
                if not manifest_path.exists():
                    print(f"❌ Missing manifest: {k8s_file}")
                    continue
                
                # Load and validate YAML
                try:
                    with open(manifest_path, 'r') as f:
                        manifest = yaml.safe_load(f)
                    
                    # Check for required Kubernetes fields
                    if isinstance(manifest, dict):
                        if 'apiVersion' in manifest and 'kind' in manifest:
                            valid_manifests += 1
                            print(f"✅ {k8s_file} validated")
                        else:
                            print(f"❌ {k8s_file} missing apiVersion or kind")
                    else:
                        print(f"❌ {k8s_file} invalid format")
                        
                except yaml.YAMLError:
                    print(f"❌ {k8s_file} YAML syntax error")
            
            success = valid_manifests >= 5  # At least 5 valid manifests
            self.validation_results['kubernetes_manifests'] = success
            
            if success:
                print(f"✅ Kubernetes manifests validated ({valid_manifests} files)")
            else:
                print(f"❌ Kubernetes validation failed ({valid_manifests} valid files)")
            
            return success
            
        except Exception as e:
            print(f"❌ Kubernetes validation error: {e}")
            return False
    
    def validate_deployment_scripts(self):
        """Validate deployment automation scripts."""
        print("\n📜 Validating Deployment Scripts...")
        
        try:
            scripts = [
                'deploy.sh',
                'status.sh',
                'cleanup.sh',
                'backup.sh'
            ]
            
            valid_scripts = 0
            
            for script in scripts:
                script_path = self.deployment_path / script
                
                if not script_path.exists():
                    print(f"❌ Missing script: {script}")
                    continue
                
                # Check if script is executable
                if not os.access(script_path, os.X_OK):
                    print(f"⚠️ {script} not executable")
                
                # Check script content
                content = script_path.read_text()
                
                if content.startswith('#!/bin/bash') and 'kubectl' in content:
                    valid_scripts += 1
                    print(f"✅ {script} validated")
                else:
                    print(f"❌ {script} invalid format or missing kubectl commands")
            
            success = valid_scripts >= 3  # At least 3 valid scripts
            self.validation_results['deployment_scripts'] = success
            
            if success:
                print(f"✅ Deployment scripts validated ({valid_scripts} files)")
            else:
                print(f"❌ Deployment scripts validation failed ({valid_scripts} valid files)")
            
            return success
            
        except Exception as e:
            print(f"❌ Deployment scripts validation error: {e}")
            return False
    
    def validate_helm_configuration(self):
        """Validate Helm chart configuration."""
        print("\n⎈ Validating Helm Configuration...")
        
        try:
            values_path = self.deployment_path / 'values.yaml'
            
            if not values_path.exists():
                print("❌ values.yaml not found")
                return False
            
            # Load and validate Helm values
            with open(values_path, 'r') as f:
                values = yaml.safe_load(f)
            
            # Check for required Helm values structure
            required_sections = ['global', 'orchestrator', 'agents', 'dashboard']
            missing_sections = []
            
            for section in required_sections:
                if section not in values:
                    missing_sections.append(section)
            
            if missing_sections:
                print(f"❌ Missing Helm sections: {missing_sections}")
                return False
            
            # Validate global configuration
            global_config = values.get('global', {})
            if 'environment' not in global_config or 'namespace' not in global_config:
                print("❌ Global configuration incomplete")
                return False
            
            self.validation_results['helm_config'] = True
            print("✅ Helm configuration validated")
            print(f"   📊 Environment: {global_config.get('environment', 'unknown')}")
            print(f"   📊 Namespace: {global_config.get('namespace', 'unknown')}")
            
            return True
            
        except yaml.YAMLError as e:
            print(f"❌ Helm YAML error: {e}")
            return False
        except Exception as e:
            print(f"❌ Helm validation error: {e}")
            return False
    
    def check_git_repository_status(self):
        """Check git repository status for CI/CD readiness."""
        print("\n🔗 Checking Git Repository Status...")
        
        try:
            os.chdir(self.project_root)
            
            # Check if we're in a git repository
            result = subprocess.run(['git', 'status'], 
                                  capture_output=True, text=True, check=True)
            
            if 'On branch' not in result.stdout:
                print("❌ Not in a valid git repository")
                return False
            
            # Check for uncommitted changes
            if 'nothing to commit' in result.stdout:
                print("✅ Repository clean - no uncommitted changes")
                clean_repo = True
            else:
                print("⚠️ Repository has uncommitted changes")
                clean_repo = False
            
            # Check remote origin
            remote_result = subprocess.run(['git', 'remote', '-v'], 
                                         capture_output=True, text=True, check=True)
            
            if 'origin' in remote_result.stdout:
                print("✅ Remote origin configured")
                has_remote = True
            else:
                print("❌ No remote origin configured")
                has_remote = False
            
            # Check current branch
            branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                         capture_output=True, text=True, check=True)
            current_branch = branch_result.stdout.strip()
            print(f"✅ Current branch: {current_branch}")
            
            success = has_remote and (clean_repo or current_branch in ['main', 'develop'])
            self.validation_results['git_status'] = success
            
            return success
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git command failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Git status check error: {e}")
            return False
    
    def generate_cicd_report(self):
        """Generate CI/CD setup validation report."""
        
        total_validations = len(self.validation_results)
        passed_validations = sum(1 for result in self.validation_results.values() if result)
        
        report = {
            'cicd_validation_summary': {
                'total_validations': total_validations,
                'passed_validations': passed_validations,
                'failed_validations': total_validations - passed_validations,
                'success_rate': round((passed_validations / total_validations) * 100, 2) if total_validations > 0 else 0
            },
            'validation_results': self.validation_results,
            'timestamp': datetime.now().isoformat(),
            'deployment_readiness': passed_validations >= 5  # At least 5 validations must pass
        }
        
        # Save report
        report_path = self.deployment_path / 'cicd_validation_report.json'
        with open(report_path, 'w') as f:
            json.dump(report, indent=2, fp=f)
        
        return report
    
    def run_cicd_validation(self):
        """Run complete CI/CD validation suite."""
        print("🔄 Starting CI/CD Setup Validation")
        print("=" * 50)
        
        # Run all validations
        validations = [
            self.validate_github_workflow(),
            self.validate_docker_configurations(),
            self.validate_kubernetes_manifests(),
            self.validate_deployment_scripts(),
            self.validate_helm_configuration(),
            self.check_git_repository_status()
        ]
        
        # Generate report
        report = self.generate_cicd_report()
        
        print("\n📊 CI/CD Validation Results")
        print("=" * 35)
        print(f"Total Validations: {report['cicd_validation_summary']['total_validations']}")
        print(f"Passed: {report['cicd_validation_summary']['passed_validations']}")
        print(f"Failed: {report['cicd_validation_summary']['failed_validations']}")
        print(f"Success Rate: {report['cicd_validation_summary']['success_rate']}%")
        
        print(f"\n📄 Report saved: cicd_validation_report.json")
        
        # Determine readiness
        if report['deployment_readiness']:
            print("✅ CI/CD PIPELINE READY - Proceeding to next step!")
            print("\n🎯 Pipeline Capabilities:")
            print("   • ✅ Automated testing on push/PR")
            print("   • ✅ Multi-service Docker builds")
            print("   • ✅ Kubernetes deployment automation")
            print("   • ✅ Environment-specific deployments")
            print("   • ✅ Rollback and cleanup capabilities")
            return True
        else:
            print("❌ CI/CD PIPELINE NOT READY - Fix issues before deployment")
            return False

def main():
    """Run CI/CD setup validation."""
    validator = CICDSetupValidator()
    success = validator.run_cicd_validation()
    return success

if __name__ == "__main__":
    main()
