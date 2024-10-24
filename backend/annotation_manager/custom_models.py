import torch

from backend.annotation_manager.model_definitions.PAR_MODEL import base_block as PAR_MODEL_base_block
from backend.annotation_manager.model_definitions.PAR_MODEL import model_factory as PAR_MODEL_model_factory
from backend.annotation_manager.model_definitions.PAR_MODEL import entry_processing as PAR_MODEL_entry_processing

# THIS TWO IMPORTS ARE RELEVANT, THEY LOAD THE MODELS INSIDE THE PROGRAM
from backend.annotation_manager.model_definitions.PAR_MODEL.backbones import resnet50
from backend.annotation_manager.model_definitions.PAR_MODEL import base_block

BACKBONE_TYPE = 'BACKBONE_TYPE'
CLASSIFIER = 'CLASSIFIER'
NAME = 'NAME'
POOLING = 'POOLING'
SCALE = 'SCALE'
BN = 'BN'
PATH = 'PATH'

def get_PAR_model(cfg, number_attributes):
    """
    Build and return a custom PAR model consisting of a backbone and a classifier.

    Args:
        cfg (dict): Configuration dictionary containing settings for the backbone and classifier.
        number_attributes (int): Number of attributes used by the classifier.

    Returns:
        torch.nn.Module: The constructed PAR model as a FeatClassifier instance.
    """
    backbone, c_output = PAR_MODEL_model_factory.build_backbone(cfg[BACKBONE_TYPE])

    classifier = PAR_MODEL_model_factory.build_classifier(cfg[CLASSIFIER][NAME])(
        nattr=number_attributes,
        c_in=c_output,
        bn=cfg[CLASSIFIER][BN],
        pool=cfg[CLASSIFIER][POOLING],
        scale=cfg[CLASSIFIER][SCALE]
    )

    return PAR_MODEL_base_block.FeatClassifier(backbone, classifier)

def load_PAR_model(cfg, model):
    """
    Load the weights of a custom PAR model from a checkpoint into the provided model.

    Args:
        cfg (dict): Configuration dictionary containing the path to the model weights.
        model (torch.nn.Module): The model instance into which the weights will be loaded.

    Returns:
        None: This function modifies the model in place.
    """
    #checkpoint = torch.load(cfg[PATH], weights_only=False)


    # Sawaiz have updated this code
    # Check if CUDA is available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # Load the checkpoint and map to the appropriate device
    checkpoint = torch.load(cfg[PATH], map_location=device)

    # update ends here 

    # As we read the checkpoint, each attribute has an extra "module." on the name and therefore cannot be loaded directly
    state_dict = checkpoint['state_dicts']
    new_state_dict = {}
    for k, v in state_dict.items():
        if k.startswith('module.'):
            new_state_dict[k[7:]] = v
        else:
            new_state_dict[k] = v

    model.load_state_dict(new_state_dict)

def process_PAR_model(config):
    """
    Returns the transformations that are needed to apply to the image in order to use the model.

    Args:
        config (dict): Configuration dictionary containing transformation settings.

    Returns:
        tuple: A tuple containing the transformation for training and for validation.
    """
    return PAR_MODEL_entry_processing.get_transform(config)
