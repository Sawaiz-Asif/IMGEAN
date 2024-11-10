import functools
import yaml

# Defines the join tag for storing paths on the config file
class StringConcatinator(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = '!join'
    
    @classmethod
    def from_yaml(cls, loader, node):
        return functools.reduce(lambda a, b: a + b, [loader.construct_scalar(i) for i in node.value])

# Read the configuration with the custom tags and returns it
def read_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    return config

# Save the configuration with custom tags to the YAML file
def save_config(config, config_path):
    """Saves the updated configuration to the YAML file."""
    try:
        with open(config_path, 'w') as file:
            yaml.dump(config, file, Dumper=yaml.SafeDumper, default_flow_style=False)
        print("Configuration saved successfully.")
    except Exception as e:
        print(f"Failed to save configuration: {e}")