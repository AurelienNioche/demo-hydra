import os.path

import hydra
from omegaconf import DictConfig, OmegaConf
import argparse
import sys # Import sys to access command line arguments directly

def main(cfg: DictConfig) -> None:
    """
    Example CLI commands:

    1. Run with model_a config:
       python main.py model_a

    2. Run with model_b config:
       python main.py model_b

    3. Run with model_a and override activation:
       python main.py model_a activation=foutre

    4. Run with model_b and override learning rate:
       python main.py model_b learning_rate=0.05
    """
    print("--- Full Configuration ---")
    print(OmegaConf.to_yaml(cfg))
    print("-------------------------")

    print("\n--- Effective Parameters ---")
    # Access all parameters directly from cfg
    print(f"Shared parameter: {cfg.shared_param}")
    print(f"Learning rate: {cfg.learning_rate}")
    print(f"Model Name: {cfg.name}") # 'name' is now top-level
    print(f"Layers: {cfg.layers}") # 'layers' is now top-level
    print(f"Activation: {cfg.activation}") # 'activation' is now top-level

    # Use getattr for optional parameters like dropout, providing a default (None)
    dropout = getattr(cfg, 'dropout', None)
    print(f"Dropout: {dropout}")
    print("--------------------------")

if __name__ == "__main__":
    # Use argparse to get the model name and overrides
    parser = argparse.ArgumentParser(description="Run model with Hydra configuration.")
    parser.add_argument("model_name", help="Name of the model config file (e.g., model_a)")
    # Capture all remaining arguments as potential overrides
    args, overrides = parser.parse_known_args()

    base_config_folder = "model"
    common_config_filename = "defaults.yaml"  # Common config file name
    default_config_filename = "default.yaml"

    # Get the model config path
    model_config_path = os.path.join(base_config_folder, args.model_name)
    # If the model name is a directory, use the default.yaml inside it
    if os.path.isdir(model_config_path):
        model_config_path = os.path.join(model_config_path, default_config_filename)

    # Initialize Hydra context (adjust config_path as needed)
    # Using version_base=None for compatibility with Hydra 1.0 behavior if needed
    with hydra.initialize(config_path=os.path.dirname(model_config_path), version_base=None):

        # 1. Load common defaults
        common_cfg = OmegaConf.load(os.path.join(base_config_folder, common_config_filename))

        # 2. Compose the model configuration
        model_cfg = hydra.compose(config_name=os.path.basename(model_config_path), overrides=overrides)

        # 3. Merge them (model-specific overrides common)
        cfg = OmegaConf.merge(common_cfg, model_cfg)

        # Run the main function with the composed config
        main(cfg) 