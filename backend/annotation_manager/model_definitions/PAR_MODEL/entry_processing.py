import torchvision.transforms as T

# ANNOTATION = 'ANNOTATION'
# PAR_MODEL = 'PAR_MODEL'
DATASET = 'DATASET'
HEIGHT = 'HEIGHT'
WIDTH = 'WIDTH'

def get_transform(config):
    # cfg = config[ANNOTATION][PAR_MODEL][DATASET]
    cfg = config[DATASET]
    height = cfg[HEIGHT]
    width = cfg[WIDTH]
    normalize = T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

    train_transform = T.Compose([
        T.Resize((height, width)),
        T.Pad(10),
        T.RandomCrop((height, width)),
        T.RandomHorizontalFlip(),
        T.ToTensor(),
        normalize,
    ])

    valid_transform = T.Compose([
        T.Resize((height, width)),
        T.ToTensor(),
        normalize
    ])

    return train_transform, valid_transform