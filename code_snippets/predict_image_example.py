import os
from backend.config_reader import read_config
from backend.annotation_manager.automatic_labeling import open_model, get_predictions_with_confidence

#
# FOR USING IT, MOVE IT TO THE SAME FOLDER AS MAIN.PY
#

# Config settings
ANNOTATION = 'ANNOTATION'
BASE_DIR = 'BASE_DIR'

# Opening config
config = read_config('./config.yaml')

# We know beforehand which file we want to open
image_name = 'sample1.png'
image_path = os.path.join(config[ANNOTATION][BASE_DIR], image_name)

# Based on the dataset_utils, we also know which labels we have
# (This ones are not right, i had to add action-other to have the same number, i don't know which one is missing)
class_labels = [
    'hs-LongHair', 'hs-BlackHair', 'hs-Hat', 'hs-Glasses', 'hs-Muffler',
    'ub-Shirt', 'ub-Sweater', 'ub-Vest', 'ub-TShirt', 'ub-Cotton',
    'ub-Jacket', 'ub-SuitUp', 'ub-Tight', 'ub-ShortSleeve', 'lb-LongTrousers',
    'lb-Skirt', 'lb-ShortSkirt', 'lb-Dress', 'lb-Jeans', 'lb-TightTrousers',
    'shoes-Leather', 'shoes-Sport', 'shoes-Boots', 'shoes-Cloth', 'shoes-Casual',
    'attach-Backpack', 'attach-SingleShoulderBag', 'attach-HandBag', 'attach-Box', 
    'attach-PlasticBag', 'attach-PaperBag', 'attach-HandTrunk', 'attach-Other', 
    'AgeLess16', 'Age17-30', 'Age31-45', 'Female', 'BodyFat', 'BodyNormal', 
    'BodyThin', 'Customer', 'Clerk', 'action-Calling', 'action-Talking', 
    'action-Gathering', 'action-Holding', 'action-Pushing', 'action-Pulling', 
    'action-CarrybyArm', 'action-CarrybyHand', 'action-Other'
]

# For opening the model we just need the config file and how many labels are there
model = open_model(config, number_attributes=len(class_labels))

# For getting the predictions
predictions_with_confidence = get_predictions_with_confidence(config, model, image_path, class_labels)

# The output is in a dictionary
print(f"Predictions for {image_name}:")
for label, confidence in predictions_with_confidence:
    print(f'Class: {label}, Confidence: {confidence:.4f}')
