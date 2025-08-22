#!/usr/bin/env python3
"""
Weights & Biases Setup for Madagascar Conservation AI
"""

import wandb
import os
from pathlib import Path

def setup_wandb_for_madagascar_conservation():
    """Initialize W&B for Madagascar conservation experiments."""
    
    # Initialize wandb (will prompt for login if needed)
    print("🔐 Setting up Weights & Biases...")
    print("Please ensure you have a W&B account and run 'wandb login' if needed")
    
    # Test configuration
    config = {
        "project": "madagascar_conservation_ai",
        "experiment_type": "setup_test",
        "hardware": "mps",
        "phase": "phase2_setup"
    }
    
    try:
        # Initialize a test run
        run = wandb.init(
            project="madagascar_conservation_ai",
            name="setup_test",
            config=config,
            tags=["setup", "test"]
        )
        
        # Log a test metric
        wandb.log({"setup_success": 1})
        
        # Finish the run
        wandb.finish()
        
        print("✅ W&B setup successful!")
        return True
        
    except Exception as e:
        print(f"❌ W&B setup failed: {e}")
        print("Please run 'wandb login' and try again")
        return False

if __name__ == "__main__":
    setup_wandb_for_madagascar_conservation()
