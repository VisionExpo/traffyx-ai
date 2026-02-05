import sys
import os

# Add src to python path to allow imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

import argparse
import yaml
import os

# Import the canonical PipelineRunner
from pipeline.runner import PipelineRunner

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Traffyx-AI Pipeline Runner")
    parser.add_argument("--video", type=str, required=True, help="Path to input video")
    parser.add_argument("--config", type=str, default="params.yaml", help="Path to configuration file")
    
    args = parser.parse_args()

    # Load configuration
    config = {}
    if os.path.exists(args.config):
        with open(args.config, "r") as f:
            config = yaml.safe_load(f)
    else:
        print(f"Warning: Config file {args.config} not found. Using defaults.")

    runner = PipelineRunner(args.video, config)
    runner.run()
