import os
import shutil
import glob
import time

# Config settings
FILES = 'FILES'
BASE_DIR = 'BASE_DIR'
GENERATED_DIR = 'GENERATED_DIR'
DISCARDED_DIR = 'DISCARDED_DIR'
CHECKING_DIR = 'CHECKING_DIR'
LABELING_DIR = 'LABELING_DIR'
DISCARDED_TRACKER = 'DISCARDED_TRACKER'

def verify_or_create_dirs(config):
    """
    Verifies the existence of directories and text files specified in the config, creating them otherwise.

    Args:
        config (dict): Configuration settings loaded from config.yaml.

    Returns:
        None
    """
    for directory in config[FILES].values():
        if directory.endswith('.txt'):
            if not os.path.exists(directory):
                with open(directory, 'w') as f:
                    pass
        else:
            if not os.path.exists(directory):
                os.makedirs(directory)

def save_generated_image(config, image, filename):
    """
    Saves a generated image to a specified directory defined in the configuration file.

    Args:
        config (dict): Configuration settings loaded from config.yaml.
        image (PIL.Image): The image object to be saved.
        filename (str): The name of the file to save the image as.

    Returns:
        None
    """
    generated_path = os.path.join(config[FILES][GENERATED_DIR], filename)
    image.save(generated_path)

def _discard_image(config, file_path, reason='Unknown'):
    """
    Private function, moves the file to the discard directory
    """
    with open(config[FILES]['DISCARDED_TRACKER'], 'a') as tracker:
        tracker.write(f"{os.path.basename(file_path)}\t{reason}\n")
    
    discarded_path = os.path.join(config[FILES]['DISCARDED_DIR'], os.path.basename(file_path))
    shutil.move(file_path, discarded_path)

def _move_checking(config, file_path):
    """
    Private function, moves the file to the checking directory
    """
    checking_path = os.path.join(config[FILES][CHECKING_DIR], os.path.basename(file_path))
    shutil.move(file_path, checking_path)

def _move_labeling(config, file_path):
    """
    Private function, moves the file to the labeling directory
    """
    labeling_path = os.path.join(config[FILES][LABELING_DIR], os.path.basename(file_path))
    shutil.move(file_path, labeling_path)

def move_generated_discard(config, filenames, reason='Automatic checking'):
    """
    Moves one or more generated images from generated_directory to discard_directory.

    Args:
        config (dict): Configuration settings loaded from config.yaml.
        filenames (str or list): The name or list of names of the files to be discarded.
        reason (str, optional): The reason for discarding the files. Default is 'Automatic checking'.

    Returns:
        None
    """
    filenames = [filenames] if type(filenames) == str else filenames
    for filename in filenames:
        file_path = os.path.join(config[FILES][GENERATED_DIR], filename)
        _discard_image(config, file_path, reason)

def move_checking_discard(config, filenames, reason='Manual decision'):
    """
    Moves one or more generated images from checking_directory to discard_directory.

    Args:
        config (dict): Configuration settings loaded from config.yaml.
        filenames (str or list): The name or list of names of the files to be discarded.
        reason (str, optional): The reason for discarding the files. Default is 'Manual decision'.

    Returns:
        None
    """
    filenames = [filenames] if type(filenames) == str else filenames
    for filename in filenames:
        file_path = os.path.join(config[FILES][CHECKING_DIR], filename)
        _discard_image(config, file_path, reason)

def move_labeling_discard(config, filenames, reason='Manual decision'):
    """
    Moves one or more generated images from labeling_directory to discard_directory.

    Args:
        config (dict): Configuration settings loaded from config.yaml.
        filenames (str or list): The name or list of names of the files to be discarded.
        reason (str, optional): The reason for discarding the files. Default is 'Manual decision'.

    Returns:
        None
    """
    filenames = [filenames] if type(filenames) == str else filenames
    for filename in filenames:
        file_path = os.path.join(config[FILES][LABELING_DIR], filename)
        _discard_image(config, file_path, reason)

def move_generated_checking(config, filenames):
    """
    Moves one or more generated images from generated_directory to checking_directory.

    Args:
        config (dict): Configuration settings loaded from config.yaml.
        filenames (str or list): The name or list of names of the files to be discarded.

    Returns:
        None
    """
    filenames = [filenames] if type(filenames) == str else filenames
    for filename in filenames:
        file_path = os.path.join(config[FILES][GENERATED_DIR], filename)
        _move_checking(config, file_path)

def move_all_generated_images_checking(config):
    files = [f for f in os.listdir(config[FILES][GENERATED_DIR]) if os.path.isfile(os.path.join(config[FILES][GENERATED_DIR], f))]
    move_generated_checking(config, files)

def ensure_unique_id_generation(config):
    generated_dir = config[FILES][GENERATED_DIR]
    unique_id = str(int(time.time()))
    
    for filename in os.listdir(generated_dir):
        old_path = os.path.join(generated_dir, filename)
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}_{unique_id}{ext}"
        new_path = os.path.join(generated_dir, new_filename)
        os.rename(old_path, new_path)

def move_generated_labeling(config, filenames):
    """
    Moves one or more generated images from generated_directory to labeling_directory.

    Args:
        config (dict): Configuration settings loaded from config.yaml.
        filenames (str or list): The name or list of names of the files to be discarded.

    Returns:
        None
    """
    filenames = [filenames] if type(filenames) == str else filenames
    for filename in filenames:
        file_path = os.path.join(config[FILES][GENERATED_DIR], filename)
        _move_labeling(config, file_path)

def move_all_generated_images_labeling(config):
    files = [f for f in os.listdir(config[FILES][GENERATED_DIR]) if os.path.isfile(os.path.join(config[FILES][GENERATED_DIR], f))]
    move_generated_labeling(config, files)

def move_discarded_labeling(config, filenames):
    """
    Moves one or more generated images from discarded_directory to labeling_directory.

    Args:
        config (dict): Configuration settings loaded from config.yaml.
        filenames (str or list): The name or list of names of the files to be discarded.

    Returns:
        None
    """
    filenames = [filenames] if type(filenames) == str else filenames
    for filename in filenames:
        file_path = os.path.join(config[FILES][DISCARDED_DIR], filename)
        _move_labeling(config, file_path)

    discarded_tracker_path = config[FILES][DISCARDED_TRACKER]
    
    with open(discarded_tracker_path, 'r') as file:
        discarded_entries = file.readlines()

    discarded_entries = [entry.strip() for entry in discarded_entries]
    updated_entries = [entry for entry in discarded_entries if entry.split('\t')[0] not in filenames]

    with open(discarded_tracker_path, 'w') as file:
        for entry in updated_entries:
            file.write(f"{entry}\n")

def move_checking_labeling(config, filenames):
    """
    Moves one or more generated images from checking_directory to labeling_directory.

    Args:
        config (dict): Configuration settings loaded from config.yaml.
        filenames (str or list): The name or list of names of the files to be discarded.

    Returns:
        None
    """
    filenames = [filenames] if type(filenames) == str else filenames
    for filename in filenames:
        file_path = os.path.join(config[FILES][CHECKING_DIR], filename)
        _move_labeling(config, file_path)

def delete_all_discarded(config):
    """
    Delete all images on the discarded folder and clears the content of the tracker.

    Args:
        config (dict): Configuration settings loaded from config.yaml.
        filenames (str or list): The name or list of names of the files to be discarded.

    Returns:
        None
    """
    files = glob.glob(os.path.join(config[FILES][DISCARDED_DIR], '*'))
    for file in files:
        os.remove(file)

    with open(config[FILES][DISCARDED_TRACKER], 'w') as f:
                    pass


def discard_all_checking(config, reason='Manual decision'):
    """
    Discard all images on the checking folder.

    Args:
        config (dict): Configuration settings loaded from config.yaml.
        reason (str, optional): The reason for discarding the files. Default is 'Manual decision'.

    Returns:
        None
    """
    filenames = [os.path.basename(file) for file in glob.glob(os.path.join(config[FILES][CHECKING_DIR], '*'))]
    move_checking_discard(config, filenames, reason)

def accept_all_checking(config):
    """
    Moves all images on the checking_directory to the labeling_directory.

    Args:
        config (dict): Configuration settings loaded from config.yaml.

    Returns:
        None
    """
    filenames = [os.path.basename(file) for file in glob.glob(os.path.join(config[FILES][CHECKING_DIR], '*'))]
    move_checking_labeling(config, filenames)

def delete_single_discarded(config, filename):
    """
    Deletes a single discarded image from the discarded directory and removes its entry from the discarded tracker.

    Args:
        config (dict): Configuration settings loaded from config.yaml.
        filename (str): The name of the file to be deleted.

    Returns:
        None
    """
    file_path = os.path.join(config[FILES][DISCARDED_DIR], filename)
    
    # Check if the file exists in the discarded directory
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Remove the entry from the discarded tracker
    discarded_tracker_path = config[FILES][DISCARDED_TRACKER]
    
    with open(discarded_tracker_path, 'r') as file:
        discarded_entries = file.readlines()

    discarded_entries = [entry.strip() for entry in discarded_entries]
    updated_entries = [entry for entry in discarded_entries if entry.split('\t')[0] != filename]

    # Write the updated tracker back
    with open(discarded_tracker_path, 'w') as file:
        for entry in updated_entries:
            file.write(f"{entry}\n")

def move_labeling_dataset(config, filenames, dataset_path):
    """
    Moves one or more generated images from labeling_directory to the dataset.

    Args:
        config (dict): Configuration settings loaded from config.yaml.
        filenames (str or list): The name or list of names of the files to be moved to the dataset.
        dataset_path (str): The path to the dataset where the images will be moved.

    Returns:
        None
    """
    filenames = [filenames] if isinstance(filenames, str) else filenames
    
    for filename in filenames:
        file_path = os.path.join(config['FILES']['LABELING_DIR'], filename)
        
        destination_path = os.path.join(dataset_path, filename)
        
        os.rename(file_path, destination_path)
