# From the /IMGEAN path, python3 -m backend.tests.test_file_utils

from backend.config_reader import read_config
import backend.file_utils as fu
import os
from PIL import Image

# Config settings
FILES = 'FILES'
BASE_DIR = 'BASE_DIR'
GENERATED_DIR = 'GENERATED_DIR'
DISCARDED_DIR = 'DISCARDED_DIR'
CHECKING_DIR = 'CHECKING_DIR'
LABELING_DIR = 'LABELING_DIR'
DISCARDED_TRACKER = 'DISCARDED_TRACKER'

def test_verify_or_create_dirs(config):
    # Assert that once its called all the directories on config['FILES'] are created
    # Unless it is a .txt, that has also to be created if it doesnt exist
    # Assert that if the .txt exists, it does not create a new one erasing the info on the previous one

    # Create all directories specified in the config
    fu.verify_or_create_dirs(config)

    # Check if all directories are created
    for dir_path in config['FILES'].values():
        if not dir_path.endswith('.txt'):
            assert os.path.exists(dir_path), f"Directory {dir_path} was not created."

    # Check if .txt file exists and if it's not being overwritten
    txt_file_path = next((path for path in config['FILES'] if path.endswith('.txt')), None)
    
    if txt_file_path:
        # If the .txt file exists, assert that it is not recreated
        if os.path.exists(txt_file_path):
            initial_size = os.path.getsize(txt_file_path)
            fu.verify_or_create_dirs(config['FILES'])  # Call again to test non-overwriting
            assert os.path.getsize(txt_file_path) == initial_size, "The .txt file was overwritten."
        else:
            # If it does not exist, assert that it was created
            assert os.path.exists(txt_file_path), f"Expected .txt file {txt_file_path} was not created."

def test_save_generated_image(config):
    # Create an image
    image = Image.new('RGB', (100, 100), color = 'blue')
    
    # Save it with the function
    filename = 'test_image.png'
    fu.save_generated_image(config, image, filename)

    # Assert that it is on config[GENERATED_DIR] now
    assert os.path.exists(os.path.join(config[FILES][GENERATED_DIR], filename)), f"Image {filename} was not saved in {config[FILES][GENERATED_DIR]}."

    # remove the image
    os.remove(os.path.join(config[FILES][GENERATED_DIR], filename))

def test_move_generated_discard(config):
    # Create three images on config[FILES][GENERATED_DIR] with save_generated_image(config, image, filename)
    for i in range(3):
        image = Image.new('RGB', (100, 100), color='blue')
        filename = f'test_image_{i}.png'
        fu.save_generated_image(config, image, filename)

    # Check that config[FILES][GENERATED_DIR] has three images
    generated_files = os.listdir(config[FILES][GENERATED_DIR])
    assert len(generated_files) == 3, "Expected 3 images in the generated directory."

    # Call the function with a single name
    single_file = generated_files[0]
    fu.move_generated_discard(config, [single_file])

    # Check that it is now on config[FILES][DISCARDED_DIR]
    assert os.path.exists(os.path.join(config[FILES][DISCARDED_DIR], single_file)), f"Image {single_file} was not moved to {config[FILES][DISCARDED_DIR]}."

    # Delete them it from config[FILES][DISCARDED_DIR]
    os.remove(os.path.join(config[FILES][DISCARDED_DIR], single_file))

    # Check that config[FILES][GENERATED_DIR] has two images
    generated_files = os.listdir(config[FILES][GENERATED_DIR])
    assert len(generated_files) == 2, "Expected 2 images in the generated directory after moving one."

    # Call the function with the two remaining names inside of a list
    fu.move_generated_discard(config, generated_files)

    # Check that both files are now on config[FILES][DISCARDED_DIR]
    for filename in generated_files:
        assert os.path.exists(os.path.join(config[FILES][DISCARDED_DIR], filename)), f"Image {filename} was not moved to {config[FILES][DISCARDED_DIR]}."

    # Delete them
    for filename in generated_files:
        os.remove(os.path.join(config[FILES][DISCARDED_DIR], filename))

    # Check that config[FILES][GENERATED_DIR] is now empty
    assert len(os.listdir(config[FILES][GENERATED_DIR])) == 0, "Expected the generated directory to be empty."

    # Also during the process check that config[FILES][DISCARDED_TRACKER] (A path to a .txt) is being updated,
    # so one new line per discarded image with filename\treason
    with open(config[FILES][DISCARDED_TRACKER], 'r') as tracker_file:
        discarded_lines = tracker_file.readlines()
    
    # Check that the number of discarded lines matches the number of discarded files
    assert len(discarded_lines) == 3, "Expected 3 lines in the discarded tracker file."

    # Check if each discarded line has the correct format
    for filename in generated_files + [single_file]:
        assert any(filename in line for line in discarded_lines), f"{filename} was not found in the discarded tracker."

    # Remove contents on the discard tracker
    with open(config[FILES][DISCARDED_TRACKER], 'w') as tracker_file:
        tracker_file.truncate(0)

def test_move_generated_checking(config):
    # Create three images on config[FILES][GENERATED_DIR] with save_generated_image(config, image, filename)
    for i in range(3):
        image = Image.new('RGB', (100, 100), color='blue')
        filename = f'test_image_{i}.png'
        fu.save_generated_image(config, image, filename)

    # Check that config[FILES][GENERATED_DIR] has three images
    generated_files = os.listdir(config[FILES][GENERATED_DIR])
    assert len(generated_files) == 3, "Expected 3 images in the generated directory."

    # Call the function with a single name
    single_file = generated_files[0]
    fu.move_generated_checking(config, [single_file])

    # Check that it is now on config[FILES][CHECKING_DIR]
    assert os.path.exists(os.path.join(config[FILES][CHECKING_DIR], single_file)), f"Image {single_file} was not moved to {config[FILES][CHECKING_DIR]}."

    # Delete them it from config[FILES][CHECKING_DIR]
    os.remove(os.path.join(config[FILES][CHECKING_DIR], single_file))

    # Check that config[FILES][GENERATED_DIR] has two images
    generated_files = os.listdir(config[FILES][GENERATED_DIR])
    assert len(generated_files) == 2, "Expected 2 images in the generated directory after moving one."

    # Call the function with the two remaining names inside of a list
    fu.move_generated_checking(config, generated_files)

    # Check that both files are now on config[FILES][CHECKING_DIR]
    for filename in generated_files:
        assert os.path.exists(os.path.join(config[FILES][CHECKING_DIR], filename)), f"Image {filename} was not moved to {config[FILES][CHECKING_DIR]}."

    # Delete them
    for filename in generated_files:
        os.remove(os.path.join(config[FILES][CHECKING_DIR], filename))

    # Check that config[FILES][GENERATED_DIR] is now empty
    assert len(os.listdir(config[FILES][GENERATED_DIR])) == 0, "Expected the generated directory to be empty."

def test_move_checking_discard(config):
    # Create three images on config[FILES][GENERATED_DIR] with save_generated_image(config, image, filename)
    for i in range(3):
        image = Image.new('RGB', (100, 100), color='blue')
        filename = f'test_image_{i}.png'
        fu.save_generated_image(config, image, filename)

    # Move them to the checking dir with move_generated_checking(config, filenames)
    generated_files = os.listdir(config[FILES][GENERATED_DIR])
    fu.move_generated_checking(config, generated_files)

    # Check that config[FILES][CHECKING_DIR] has three images
    checking_files = os.listdir(config[FILES][CHECKING_DIR])
    assert len(checking_files) == 3, "Expected 3 images in the checking directory."

    # Call the function with a single name
    single_file = checking_files[0]
    fu.move_checking_discard(config, [single_file])

    # Check that it is now on config[FILES][DISCARDED_DIR]
    assert os.path.exists(os.path.join(config[FILES][DISCARDED_DIR], single_file)), f"Image {single_file} was not moved to {config[FILES][DISCARDED_DIR]}."

    # Delete them it from config[FILES][DISCARDED_DIR]
    os.remove(os.path.join(config[FILES][DISCARDED_DIR], single_file))

    # Check that config[FILES][CHECKING_DIR] has two images
    checking_files = os.listdir(config[FILES][CHECKING_DIR])
    assert len(checking_files) == 2, "Expected 2 images in the checking directory after moving one."

    # Call the function with the two remaining names inside of a list
    fu.move_checking_discard(config, checking_files)

    # Check that both files are now on config[FILES][DISCARDED_DIR]
    for filename in checking_files:
        assert os.path.exists(os.path.join(config[FILES][DISCARDED_DIR], filename)), f"Image {filename} was not moved to {config[FILES][DISCARDED_DIR]}."

    # Delete them
    for filename in checking_files:
        os.remove(os.path.join(config[FILES][DISCARDED_DIR], filename))

    # Check that config[FILES][CHECKING_DIR] is now empty
    assert len(os.listdir(config[FILES][CHECKING_DIR])) == 0, "Expected the checking directory to be empty."

    # Also during the process check that config[FILES][DISCARDED_TRACKER] (A path to a .txt) is being updated,
    # so one new line per discarded image with filename\treason
    with open(config[FILES][DISCARDED_TRACKER], 'r') as tracker_file:
        discarded_lines = tracker_file.readlines()
    
    # Check that the number of discarded lines matches the number of discarded files
    assert len(discarded_lines) == 3, "Expected 3 lines in the discarded tracker file."

    # Check if each discarded line has the correct format
    for filename in checking_files + [single_file]:
        assert any(filename in line for line in discarded_lines), f"{filename} was not found in the discarded tracker."

    # Remove contents on the discard tracker
    with open(config[FILES][DISCARDED_TRACKER], 'w') as tracker_file:
        tracker_file.truncate(0)

def test_move_generated_labeling(config):
    # Create three images on config[FILES][GENERATED_DIR] with save_generated_image(config, image, filename)
    for i in range(3):
        image = Image.new('RGB', (100, 100), color='blue')
        filename = f'test_image_{i}.png'
        fu.save_generated_image(config, image, filename)

    # Check that config[FILES][GENERATED_DIR] has three images
    generated_files = os.listdir(config[FILES][GENERATED_DIR])
    assert len(generated_files) == 3, "Expected 3 images in the generated directory."

    # Call the function with a single name
    single_file = generated_files[0]
    fu.move_generated_labeling(config, [single_file])

    # Check that it is now on config[FILES][LABELING_DIR]
    assert os.path.exists(os.path.join(config[FILES][LABELING_DIR], single_file)), f"Image {single_file} was not moved to {config[FILES][LABELING_DIR]}."

    # Delete it from config[FILES][LABELING_DIR]
    os.remove(os.path.join(config[FILES][LABELING_DIR], single_file))

    # Check that config[FILES][GENERATED_DIR] has two images
    generated_files = os.listdir(config[FILES][GENERATED_DIR])
    assert len(generated_files) == 2, "Expected 2 images in the generated directory after moving one."

    # Call the function with the two remaining names inside of a list
    fu.move_generated_labeling(config, generated_files)

    # Check that both files are now on config[FILES][LABELING_DIR]
    for filename in generated_files:
        assert os.path.exists(os.path.join(config[FILES][LABELING_DIR], filename)), f"Image {filename} was not moved to {config[FILES][LABELING_DIR]}."

    # Delete them
    for filename in generated_files:
        os.remove(os.path.join(config[FILES][LABELING_DIR], filename))

    # Check that config[FILES][GENERATED_DIR] is now empty
    assert len(os.listdir(config[FILES][GENERATED_DIR])) == 0, "Expected the generated directory to be empty."

def test_move_discarded_labeling(config):
    # Create three images on config[FILES][GENERATED_DIR] with save_generated_image(config, image, filename)
    for i in range(3):
        image = Image.new('RGB', (100, 100), color='blue')
        filename = f'test_image_{i}.png'
        fu.save_generated_image(config, image, filename)

    # Move them to the discarded dir with move_generated_discard(config, filenames, reason='Automatic checking')
    generated_files = [f for f in os.listdir(config['FILES'][GENERATED_DIR]) if not f.endswith('.txt')]
    fu.move_generated_discard(config, generated_files)

    # Check that config[FILES][DISCARDED_DIR] has three images
    discarded_files = [f for f in os.listdir(config['FILES'][DISCARDED_DIR]) if not f.endswith('.txt')]
    assert len(discarded_files) == 3, "Expected 3 images in the discarded directory."

    # Call the function with a single name
    single_file = discarded_files[0]
    fu.move_discarded_labeling(config, [single_file])

    # Check that it is now on config[FILES][LABELING_DIR]
    assert os.path.exists(os.path.join(config[FILES][LABELING_DIR], single_file)), f"Image {single_file} was not moved to {config[FILES][LABELING_DIR]}."

    # Delete it from config[FILES][LABELING_DIR]
    os.remove(os.path.join(config[FILES][LABELING_DIR], single_file))

    # Check that config[FILES][DISCARDED_DIR] has two images
    discarded_files = [f for f in os.listdir(config['FILES'][DISCARDED_DIR]) if not f.endswith('.txt')]
    assert len(discarded_files) == 2, "Expected 2 images in the discarded directory after moving one."

    # Call the function with the two remaining names inside of a list
    fu.move_discarded_labeling(config, discarded_files)

    # Check that both files are now on config[FILES][LABELING_DIR]
    for filename in discarded_files:
        assert os.path.exists(os.path.join(config[FILES][LABELING_DIR], filename)), f"Image {filename} was not moved to {config[FILES][LABELING_DIR]}."

    # Delete them
    for filename in discarded_files:
        os.remove(os.path.join(config[FILES][LABELING_DIR], filename))

    # Check that config[FILES][DISCARDED_DIR] is now empty
    assert len(os.listdir(config[FILES][DISCARDED_DIR])) == 0+1, "Expected the discarded directory to be empty."

    # Also during the process check that config[FILES][DISCARDED_TRACKER] (A path to a .txt) is being updated,
    # so one less line per moved image with shape filename\treason
    with open(config[FILES][DISCARDED_TRACKER], 'r') as tracker_file:
        discarded_lines = tracker_file.readlines()
    
    # Check that the number of discarded lines matches the number of discarded files
    assert len(discarded_lines) == 0, "Expected 1 line in the discarded tracker file after moving 2 images."

def test_move_checking_labeling(config):
    # Create three images on config[FILES][GENERATED_DIR] with save_generated_image(config, image, filename)
    for i in range(3):
        image = Image.new('RGB', (100, 100), color='blue')
        filename = f'test_image_{i}.png'
        fu.save_generated_image(config, image, filename)

    # Move them to the checking dir with move_generated_checking(config, filenames)
    generated_files = os.listdir(config[FILES][GENERATED_DIR])
    fu.move_generated_checking(config, generated_files)

    # Check that config[FILES][CHECKING_DIR] has three images
    checking_files = os.listdir(config[FILES][CHECKING_DIR])
    assert len(checking_files) == 3, "Expected 3 images in the checking directory."

    # Call the function with a single name
    single_file = checking_files[0]
    fu.move_checking_labeling(config, [single_file])

    # Check that it is now on config[FILES][LABELING_DIR]
    assert os.path.exists(os.path.join(config[FILES][LABELING_DIR], single_file)), f"Image {single_file} was not moved to {config[FILES][LABELING_DIR]}."

    # Delete it from config[FILES][LABELING_DIR]
    os.remove(os.path.join(config[FILES][LABELING_DIR], single_file))

    # Check that config[FILES][CHECKING_DIR] has two images
    checking_files = os.listdir(config[FILES][CHECKING_DIR])
    assert len(checking_files) == 2, "Expected 2 images in the checking directory after moving one."

    # Call the function with the two remaining names inside of a list
    fu.move_checking_labeling(config, checking_files)

    # Check that both files are now on config[FILES][LABELING_DIR]
    for filename in checking_files:
        assert os.path.exists(os.path.join(config[FILES][LABELING_DIR], filename)), f"Image {filename} was not moved to {config[FILES][LABELING_DIR]}."

    # Delete them
    for filename in checking_files:
        os.remove(os.path.join(config[FILES][LABELING_DIR], filename))

    # Check that config[FILES][CHECKING_DIR] is now empty
    assert len(os.listdir(config[FILES][CHECKING_DIR])) == 0, "Expected the checking directory to be empty."

def test_move_labeling_discard(config):
    # Create three images on config[FILES][GENERATED_DIR] with save_generated_image(config, image, filename)
    for i in range(3):
        image = Image.new('RGB', (100, 100), color='blue')
        filename = f'test_image_{i}.png'
        fu.save_generated_image(config, image, filename)

    # Move them to the checking dir with move_generated_checking(config, filenames),
    # and then move_checking_labeling(config, filenames)
    generated_files = os.listdir(config[FILES][GENERATED_DIR])
    fu.move_generated_checking(config, generated_files)
    checking_files = os.listdir(config[FILES][CHECKING_DIR])
    fu.move_checking_labeling(config, checking_files)

    # Check that config[FILES][LABELING_DIR] has three images
    labeling_files = os.listdir(config[FILES][LABELING_DIR])
    assert len(labeling_files) == 3, "Expected 3 images in the labeling directory."

    # Call the function with a single name
    single_file = labeling_files[0]
    fu.move_labeling_discard(config, [single_file])

    # Check that it is now on config[FILES][DISCARDED_DIR]
    assert os.path.exists(os.path.join(config[FILES][DISCARDED_DIR], single_file)), f"Image {single_file} was not moved to {config[FILES][DISCARDED_DIR]}."

    # Delete it from config[FILES][DISCARDED_DIR]
    os.remove(os.path.join(config[FILES][DISCARDED_DIR], single_file))

    # Check that config[FILES][LABELING_DIR] has two images
    labeling_files = os.listdir(config[FILES][LABELING_DIR])
    assert len(labeling_files) == 2, "Expected 2 images in the labeling directory after moving one."

    # Call the function with the two remaining names inside of a list
    fu.move_labeling_discard(config, labeling_files)

    # Check that both files are now on config[FILES][DISCARDED_DIR]
    for filename in labeling_files:
        assert os.path.exists(os.path.join(config[FILES][DISCARDED_DIR], filename)), f"Image {filename} was not moved to {config[FILES][DISCARDED_DIR]}."

    # Delete them
    for filename in labeling_files:
        os.remove(os.path.join(config[FILES][DISCARDED_DIR], filename))

    # Check that config[FILES][LABELING_DIR] is now empty
    assert len(os.listdir(config[FILES][LABELING_DIR])) == 0, "Expected the labeling directory to be empty."

    # Also during the process check that config[FILES][DISCARDED_TRACKER] (A path to a .txt) is being updated,
    # so one new line per discarded image with filename\treason
    with open(config[FILES][DISCARDED_TRACKER], 'r') as tracker_file:
        discarded_lines = tracker_file.readlines()
    
    # Check that the number of discarded lines matches the number of discarded files
    assert len(discarded_lines) == 3, "Expected 3 lines in the discarded tracker file after moving 3 images."

    # Check if each discarded line has the correct format
    for filename in labeling_files + [single_file]:
        assert any(filename in line for line in discarded_lines), f"{filename} was not found in the discarded tracker."

    # Remove contents on the discard tracker
    with open(config[FILES][DISCARDED_TRACKER], 'w') as tracker_file:
        tracker_file.truncate(0)

def test_delete_all_discarded(config):
    # Create three images on config[FILES][GENERATED_DIR] with save_generated_image(config, image, filename)
    for i in range(3):
        image = Image.new('RGB', (100, 100), color='blue')
        filename = f'test_image_{i}.png'
        fu.save_generated_image(config, image, filename)

    # Move them to the discarded dir with move_generated_discard(config, filenames, reason='Automatic checking')
    generated_files = os.listdir(config[FILES][GENERATED_DIR])
    fu.move_generated_discard(config, generated_files, reason='Automatic checking')

    # Check that config[FILES][DISCARDED_DIR] has three images
    discarded_files = [f for f in os.listdir(config['FILES'][DISCARDED_DIR]) if not f.endswith('.txt')]
    assert len(discarded_files) == 3, "Expected 3 images in the discarded directory."

    # Call the function
    fu.delete_all_discarded(config)

    # Check that config[FILES][DISCARDED_DIR] is now empty
    assert len(os.listdir(config[FILES][DISCARDED_DIR])) == 0, "Expected the discarded directory to be empty."

    # Remove contents on the discard tracker
    with open(config[FILES][DISCARDED_TRACKER], 'w') as tracker_file:
        tracker_file.truncate(0)

def test_discard_all_checking(config):
    # Create three images on config[FILES][GENERATED_DIR] with save_generated_image(config, image, filename)
    for i in range(3):
        image = Image.new('RGB', (100, 100), color='blue')
        filename = f'test_image_{i}.png'
        fu.save_generated_image(config, image, filename)

    # Move them to the checking dir with move_generated_checking(config, filenames)
    generated_files = os.listdir(config[FILES][GENERATED_DIR])
    fu.move_generated_checking(config, generated_files)

    # Check that config[FILES][CHECKING_DIR] has three images
    checking_files = os.listdir(config[FILES][CHECKING_DIR])
    assert len(checking_files) == 3, "Expected 3 images in the checking directory."

    # Call the function
    fu.discard_all_checking(config)

    # Check that config[FILES][DISCARDED_DIR] has three images now
    discarded_files = [f for f in os.listdir(config['FILES'][DISCARDED_DIR]) if not f.endswith('.txt')]
    assert len(discarded_files) == 3, "Expected 3 images in the discarded directory after discarding from checking."

    # Check that config[FILES][CHECKING_DIR] has 0 images now
    checking_files = os.listdir(config[FILES][CHECKING_DIR])
    assert len(checking_files) == 0, "Expected the checking directory to be empty after discarding."

    # Remove files from the discarded directory
    for filename in generated_files:
        os.remove(os.path.join(config[FILES][DISCARDED_DIR], filename))

    # Check that config[FILES][DISCARDED_TRACKER] has three new entries, one per image
    with open(config[FILES][DISCARDED_TRACKER], 'r') as tracker_file:
        discarded_lines = tracker_file.readlines()

    # Check that the number of discarded lines matches the number of discarded files
    assert len(discarded_lines) == 3, "Expected 3 lines in the discarded tracker file after discarding images."

    # Verify that each discarded line contains the correct image filename and reason
    for filename in checking_files:
        assert any(filename in line for line in discarded_lines), f"{filename} was not found in the discarded tracker."

    # Remove contents on the discard tracker
    with open(config[FILES][DISCARDED_TRACKER], 'w') as tracker_file:
        tracker_file.truncate(0)

def test_accept_all_checking(config):
    # Create three images on config[FILES][GENERATED_DIR] with save_generated_image(config, image, filename)
    for i in range(3):
        image = Image.new('RGB', (100, 100), color='blue')
        filename = f'test_image_{i}.png'
        fu.save_generated_image(config, image, filename)

    # Move them to the checking dir with move_generated_checking(config, filenames)
    generated_files = os.listdir(config[FILES][GENERATED_DIR])
    fu.move_generated_checking(config, generated_files)

    # Check that config[FILES][CHECKING_DIR] has three images
    checking_files = os.listdir(config[FILES][CHECKING_DIR])
    assert len(checking_files) == 3, "Expected 3 images in the checking directory."

    # Call the function
    fu.accept_all_checking(config)

    # Check that config[FILES][LABELING_DIR] has three images now
    labeling_files = os.listdir(config[FILES][LABELING_DIR])
    assert len(labeling_files) == 3, "Expected 3 images in the labeling directory after accepting from checking."

    # Check that config[FILES][CHECKING_DIR] has 0 images now
    checking_files = os.listdir(config[FILES][CHECKING_DIR])
    assert len(checking_files) == 0, "Expected the checking directory to be empty after accepting."

    # Remove files from the labeling directory
    for filename in generated_files:
        os.remove(os.path.join(config[FILES][LABELING_DIR], filename))

if __name__ == "__main__":
    config = read_config("./config.yaml")

    with open(config[FILES][DISCARDED_TRACKER], 'w') as tracker_file:
        tracker_file.truncate(0)

    test_verify_or_create_dirs(config)
    test_save_generated_image(config)
    test_move_generated_discard(config)
    test_move_generated_checking(config)
    test_move_checking_discard(config)
    test_move_generated_labeling(config)
    test_move_discarded_labeling(config)
    test_move_checking_labeling(config)
    test_move_labeling_discard(config)
    test_delete_all_discarded(config)
    test_discard_all_checking(config)
    test_accept_all_checking(config) 

    os.remove(config[FILES][DISCARDED_TRACKER])

    print("All tests correctly executed!")