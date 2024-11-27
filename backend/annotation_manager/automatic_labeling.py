import torch
import os
from PIL import Image
import torch.nn.functional as F
from backend.annotation_manager.custom_models import *

# Config settings
ANNOTATION = 'ANNOTATION'
MODELS = 'MODELS'
CURRENT_SELECTED ='CURRENT_SELECTED'

model_mapping = {
    "PAR_MODEL": (get_PAR_model, load_PAR_model, process_PAR_model)
    # Add more mappings as needed
}

def open_model(config, model_name=None, number_attributes=51):
    """
    Load a pre-trained model from a checkpoint based on the provided configuration.

    Args:
        config (dict): Configuration dictionary that holds the model path under `ANNOTATION`.
        model_name (str): Key in `config[ANNOTATION][MODELS][INDEX][NAME]` to access the model path.
        number_attributes (int): Number of attributes used to configure the model.

    Returns:
        torch.nn.Module: The loaded PyTorch model.
    """

    cfg = get_model_config(config, model_name)
    model_type = cfg.get('TYPE', 'PAR_MODEL')
    # This part of here dynamically handles geting the model and loading it based on the model_mapping dict
    get_model, load_model, _ = model_mapping.get(model_type)
    if get_model:
        model = get_model(cfg, number_attributes)
        load_model(cfg, model)
    else:
        raise ValueError(f"Model type '{model_type}' is not defined.")

    model.eval()
    
    return model


def get_predictions_with_confidence(config, model, image_path, class_labels, model_name=None):
    """
    Get the predicted labels and their confidence scores for an image using the loaded model.

    Args:
        config (dict): Configuration dictionary for model processing.
        model (torch.nn.Module): The pre-trained model used for inference.
        image_path (str): Path to the image file to be processed.
        class_labels (list): List of class names corresponding to the model output.
        model_key (str): Key in `config[ANNOTATION]` to access the model path.

    Returns:
        list: A list of tuples containing class labels and their corresponding confidence scores.
    """

    # This part of here dynamically handles geting the model and loading it based on the model_mapping dict
    cfg = get_model_config(config, model_name)
    model_type = cfg.get('TYPE', 'PAR_MODEL')

    _, _, get_transform = model_mapping.get(model_type)
    if get_transform:
        _, valid_transform = get_transform(cfg)
    else:
        raise ValueError(f"Model type '{model_type}' is not defined.")
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    image = Image.open(image_path).convert('RGB')
    image_tensor = valid_transform(image).unsqueeze(0)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    image_tensor = image_tensor.to(device)
    
    # Perform inference
    with torch.no_grad():
        logits, feat = model(image_tensor)
    
    # Apply softmax to get probabilities
    probabilities = F.softmax(logits[0], dim=1)
    
    probabilities = probabilities.cpu().numpy().flatten()
    predictions_with_confidence = list(zip(class_labels, probabilities))
    
    return predictions_with_confidence

def get_model_config(config, model_name):
    """
    Retrieve the configuration for a specific model by name.

    Args:
        config (dict): The configuration dictionary.
        model_name (str): The name of the model to retrieve.

    Returns:
        dict: The configuration for the specified model.
    """
    index = config[ANNOTATION][CURRENT_SELECTED]
    if model_name is None:
        return config[ANNOTATION][MODELS][index]

    models = config.get(ANNOTATION, {}).get(MODELS, [])
    for model_cfg in models:
        if model_cfg.get('Name') == model_name:
            return model_cfg
    raise ValueError(f"Model with name '{model_name}' not found in configuration.")