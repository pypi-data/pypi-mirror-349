# token_itemize/config.py
import os
import yaml

def load_config(config_file='config.yaml'):
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            try:
                config = yaml.safe_load(f)
                return config if config else {}
            except yaml.YAMLError as e:
                print(f"Error parsing config file: {str(e)}")
                return {}
    else:
        return {}
