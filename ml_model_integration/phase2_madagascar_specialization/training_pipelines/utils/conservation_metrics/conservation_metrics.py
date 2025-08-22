#!/usr/bin/env python3
"""
Conservation-Specific Metrics for Madagascar AI Models
======================================================

Custom metrics that prioritize conservation impact and real-world effectiveness.
"""

import numpy as np
import torch
import torch.nn.functional as F
from typing import Dict, List, Tuple, Optional
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix
import pandas as pd

class ConservationMetrics:
    """Conservation-focused metrics for Madagascar AI models."""
    
    def __init__(self):
        # IUCN Red List status weights
        self.conservation_weights = {
            'CR': 5.0,  # Critically Endangered
            'EN': 3.0,  # Endangered  
            'VU': 2.0,  # Vulnerable
            'NT': 1.5,  # Near Threatened
            'LC': 1.0   # Least Concern
        }
        
        # Madagascar endemic species bonus
        self.endemic_bonus = 1.5
        
        # Species information database
        self.species_info = self.load_species_conservation_status()
    
    def load_species_conservation_status(self) -> Dict:
        """Load conservation status for Madagascar species."""
        return {
            'Indri_indri': {'status': 'CR', 'endemic': True, 'priority': 'highest'},
            'Propithecus_diadema': {'status': 'CR', 'endemic': True, 'priority': 'highest'},
            'Lemur_catta': {'status': 'EN', 'endemic': True, 'priority': 'high'},
            'Eulemur_macaco': {'status': 'VU', 'endemic': True, 'priority': 'high'},
            'Daubentonia_madagascariensis': {'status': 'EN', 'endemic': True, 'priority': 'highest'},
            'Cryptoprocta_ferox': {'status': 'VU', 'endemic': True, 'priority': 'high'},
            # Add more species as needed
        }
    
    def conservation_weighted_accuracy(self, y_true: np.ndarray, y_pred: np.ndarray, 
                                     species_names: List[str]) -> float:
        """Calculate accuracy weighted by conservation priority."""
        total_weight = 0
        weighted_correct = 0
        
        for i, species in enumerate(species_names):
            mask = y_true == i
            if not mask.any():
                continue
            
            species_accuracy = (y_pred[mask] == y_true[mask]).mean()
            
            # Get conservation weight
            if species in self.species_info:
                status = self.species_info[species]['status']
                weight = self.conservation_weights.get(status, 1.0)
                
                # Apply endemic bonus
                if self.species_info[species].get('endemic', False):
                    weight *= self.endemic_bonus
            else:
                weight = 1.0
            
            weighted_correct += species_accuracy * weight * mask.sum()
            total_weight += weight * mask.sum()
        
        return weighted_correct / total_weight if total_weight > 0 else 0.0
    
    def anti_poaching_precision(self, y_true: np.ndarray, y_pred: np.ndarray,
                               target_species: List[str]) -> float:
        """Calculate precision for high-priority anti-poaching species."""
        target_indices = [i for i, species in enumerate(target_species) 
                         if species in ['Indri_indri', 'Propithecus_diadema', 
                                       'Lemur_catta', 'Cryptoprocta_ferox']]
        
        if not target_indices:
            return 0.0
        
        # Calculate precision for target species
        target_mask = np.isin(y_true, target_indices)
        if not target_mask.any():
            return 0.0
        
        target_true = y_true[target_mask]
        target_pred = y_pred[target_mask]
        
        precision_scores = []
        for idx in target_indices:
            tp = ((target_true == idx) & (target_pred == idx)).sum()
            fp = ((target_true != idx) & (target_pred == idx)).sum()
            
            if tp + fp > 0:
                precision_scores.append(tp / (tp + fp))
        
        return np.mean(precision_scores) if precision_scores else 0.0
    
    def ecosystem_connectivity_score(self, predicted_masks: np.ndarray,
                                   true_masks: np.ndarray) -> float:
        """Calculate habitat connectivity preservation score."""
        # Simplified connectivity metric based on preserved habitat patches
        connectivity_scores = []
        
        for i in range(len(predicted_masks)):
            pred_mask = predicted_masks[i]
            true_mask = true_masks[i]
            
            # Calculate preserved habitat area
            preserved_ratio = np.logical_and(pred_mask > 0, true_mask > 0).sum() / max(true_mask.sum(), 1)
            
            # Calculate fragmentation (simplified)
            # In practice, this would use more sophisticated connectivity algorithms
            fragmentation_penalty = self.calculate_fragmentation_penalty(pred_mask)
            
            connectivity_score = preserved_ratio * (1 - fragmentation_penalty)
            connectivity_scores.append(connectivity_score)
        
        return np.mean(connectivity_scores)
    
    def calculate_fragmentation_penalty(self, mask: np.ndarray) -> float:
        """Calculate habitat fragmentation penalty."""
        # Simplified fragmentation calculation
        # Count number of separate habitat patches
        from scipy import ndimage
        
        labeled_array, num_features = ndimage.label(mask > 0)
        
        if num_features == 0:
            return 1.0  # Complete fragmentation
        
        # Penalty based on number of fragments vs ideal (fewer is better)
        ideal_fragments = 1
        fragmentation_penalty = min(1.0, (num_features - ideal_fragments) / 10.0)
        
        return max(0.0, fragmentation_penalty)
    
    def field_deployment_score(self, model_size_mb: float, inference_fps: float,
                              accuracy: float) -> float:
        """Calculate readiness score for field deployment."""
        # Normalize components (0-1 scale)
        size_score = max(0, 1 - model_size_mb / 100)  # Penalty for models > 100MB
        speed_score = min(1.0, inference_fps / 30)     # Target 30 FPS
        accuracy_score = accuracy
        
        # Weighted combination
        deployment_score = (
            0.3 * size_score +
            0.3 * speed_score + 
            0.4 * accuracy_score
        )
        
        return deployment_score
    
    def generate_conservation_report(self, results: Dict) -> Dict:
        """Generate comprehensive conservation impact report."""
        report = {
            'conservation_summary': {
                'overall_conservation_score': 0.0,
                'species_performance': {},
                'habitat_preservation': {},
                'anti_poaching_readiness': {},
                'field_deployment_status': {}
            },
            'recommendations': [],
            'priority_actions': []
        }
        
        # Add detailed analysis based on results
        # This would be expanded based on specific model outputs
        
        return report

def calculate_model_conservation_impact(model_results: Dict, 
                                      conservation_priorities: Dict) -> Dict:
    """Calculate overall conservation impact of the model."""
    metrics = ConservationMetrics()
    
    impact_score = {
        'species_protection': 0.0,
        'habitat_preservation': 0.0, 
        'anti_poaching_effectiveness': 0.0,
        'research_advancement': 0.0,
        'overall_impact': 0.0
    }
    
    # Calculate impact components
    # Implementation would depend on specific model outputs
    
    return impact_score
