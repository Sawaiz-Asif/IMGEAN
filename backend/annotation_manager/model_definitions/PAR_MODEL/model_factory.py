from backend.annotation_manager.model_definitions.PAR_MODEL.registry import BACKBONE
from backend.annotation_manager.model_definitions.PAR_MODEL.registry import CLASSIFIER

def build_backbone(key, multi_scale=False):

    model_dict = {
        'resnet50': 2048
    }

    model = BACKBONE[key]()
    output_d = model_dict[key]

    return model, output_d

def build_classifier(key):

    return CLASSIFIER[key]