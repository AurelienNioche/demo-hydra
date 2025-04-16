import os.path

import hydra
from omegaconf import DictConfig, OmegaConf
import argparse


BASE_CONFIG_FOLDER = "model"
DEFAULT_MODEL_CONFIG = "default.yaml"

def main(cfg: DictConfig) -> None:
    print("--- Full Configuration ---")
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    # Use argparse to get the model name and overrides
    parser = argparse.ArgumentParser(description="Run model with Hydra configuration.")
    parser.add_argument("model_name", help="Name of the model config file (e.g., model_a)")
    # Capture all remaining arguments as potential overrides
    args, overrides = parser.parse_known_args()

    # Get the model config path
    model_config_path = os.path.join(BASE_CONFIG_FOLDER, args.model_name)
    # If the model name is a directory, use the default.yaml inside it
    if os.path.isdir(model_config_path):
        model_config_path = os.path.join(model_config_path, DEFAULT_MODEL_CONFIG)

    # Initialize Hydra context (adjust config_path as needed)
    # Using version_base=None for compatibility with Hydra 1.0 behavior if needed
    with hydra.initialize(config_path=os.path.dirname(model_config_path), version_base=None):
        # Compose the model configuration
        cfg = hydra.compose(config_name=os.path.basename(model_config_path), overrides=overrides)
        # Run the main function with the composed config
        main(cfg) 