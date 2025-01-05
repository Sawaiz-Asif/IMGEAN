import functools
import yaml
import json
import os
from pathlib import Path
from datetime import datetime

def create_default_config(config_path):
    """Creates a new config file with default values if none exists."""
    base_dir = str(Path(config_path).parent)
    # Default configuration structure
    default_config = {
        'PROJECT_NAME': 'MyProject',  # Placeholder name for the project
        'FILES': {
            'BASE_DIR': base_dir,
            'CHECKING_DIR': os.path.join(base_dir, 'checking'),
            'DISCARDED_DIR': os.path.join(base_dir, 'discarded'),
            'DISCARDED_TRACKER': os.path.join(base_dir, 'discarded', 'reasons_tracker.txt'),
            'GENERATED_DIR': os.path.join(base_dir, 'generated'),
            'LABELING_DIR': os.path.join(base_dir, 'labeling')
        },
        'DATASET': {
            'NAME': None,
            'PATH': os.path.join(base_dir, 'dataset_custom.pkl'),
        },
        'ANNOTATION': {
            'BASE_DIR': os.path.join(base_dir, 'labeling'),
            'CURRENT_SELECTED': 0,
            'MODELS': [

            ]
        },
        'AUTO_LABEL': {
            'CHECKBOX_THRESHOLD': 0.5,
            'CONFIDENCE_THRESHOLDS': [

            ],
            'DEFAULT_COLOR': 'blue',
            'MAX_AUTO_LABEL': 11
        },
        'GENERATION': {
            'BASE_OUTPUT_PATH': './ComfyUI/output',
            'IP_COMFY': 'http://127.0.0.1:8188',
            'MODELS': [
            ],
            'PROMPTS': {
                'negative': "",
                'positive': ''
            },
            'filename': 'generated_image',
            'manual_quality_check': True,
            'model': None,
            'num_images': 3,
            'resolution_height': 1024,
            'resolution_width': 1024,
            'seed': None,
            'steps': 1
        },
        'QUALITY_CHECKS': {
            'BASE_DIR': './backend/quality_checker',
            'FUNCTIONS': [
            ],
            'selected_checks': []
        }
    }

    # Save the config to the specified path
    save_config(default_config, config_path)
    print(f"New config file created at {config_path}")
def create_projects_file():
    """Create the projects.json file with the initial structure if it doesn't exist."""
    projects_file = './projects/projects.json'
    
    # Check if the 'projects.json' file exists
    if not os.path.exists(projects_file):
        # Create the 'projects' directory if it doesn't exist
        os.makedirs('./projects', exist_ok=True)

        # Initial structure to create if the file doesn't exist
        initial_data = {
            "projects": [
                {
                    "name": "Project1",
                    "path": "projects/Project1",
                    "is_active": True,
                    "last_modified": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                }
            ]
        }
        
        try:
            # Write the initial data to the 'projects.json' file
            with open(projects_file, 'w') as f:
                json.dump(initial_data, f, indent=4)
            print(f"Created the file {projects_file} with initial data.")
            
            # Now, create the project directory and the default config file
            new_project_path = initial_data["projects"][0]["path"]
            os.makedirs(new_project_path, exist_ok=True)  # Create the project folder
            create_default_config(f"{new_project_path}/config.yaml")  # Create the default config file

        except Exception as e:
            print(f"Error creating the file: {e}")

def read_active_project(projects_file):
    """Read the projects.json file and return the active project."""
    try:
        with open(projects_file, 'r') as f:
            data = json.load(f)

        # Find the active project (marked by 'is_active': True)
        active_project = None
        for project in data.get("projects", []):
            if project.get("is_active", False):
                active_project = project
                break

        if active_project:
            print(f"Active project found: {active_project['name']} at {active_project['path']}")
        else:
            print("No active project found.")
        
        return active_project  # Returns the active project or None

    except Exception as e:
        print(f"Error reading projects file: {e}")
        return None

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
        # Ensure the directory exists
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Write the configuration to the file
        with open(config_path, 'w') as file:
            yaml.dump(config, file, Dumper=yaml.SafeDumper, default_flow_style=False)
        print("Path :" , config_path)
        print("Configuration saved successfully.")
    except Exception as e:
        print(f"Failed to save configuration: {e}")

def update_base_dir(config_path, new_base_dir):
    """
    Updates the BASE_DIR in the configuration file and updates all dependent paths manually.
    """
    try:
        # Load the existing configuration
        config = read_config(config_path)

        # Update the BASE_DIR
        config['FILES']['BASE_DIR'] = new_base_dir

        # Manually update dependent paths
        config['FILES']['CHECKING_DIR'] = os.path.join(new_base_dir, 'checking')
        config['FILES']['DISCARDED_DIR'] = os.path.join(new_base_dir, 'discarded')
        config['FILES']['DISCARDED_TRACKER'] = os.path.join(new_base_dir, 'discarded', 'reasons_tracker.txt')
        config['FILES']['GENERATED_DIR'] = os.path.join(new_base_dir, 'generated')
        config['FILES']['LABELING_DIR'] = os.path.join(new_base_dir, 'labeling')
        config['DATASET']['PATH'] = os.path.join(new_base_dir, 'dataset_custom.pkl')
        config['ANNOTATION']['BASE_DIR'] = os.path.join(new_base_dir, 'labeling')

        # Save the updated configuration
        save_config(config, config_path)
        print(f"BASE_DIR and dependent paths updated successfully in {config_path}")

    except Exception as e:
        print(f"Failed to update paths: {e}")