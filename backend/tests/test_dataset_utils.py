import os
import tempfile
import pytest
from unittest.mock import patch
import pickle

import numpy as np
from easydict import EasyDict

#from backend.annotation_manager.dataset_utils import DatasetManager
from backend.annotation_manager.dataset_utils import DatasetManager

# ---------------------------------------------------
# Fixtures - Setup and Teardown for Tests
# ---------------------------------------------------

@pytest.fixture
def temp_dir():
    """
    Fixture to create and return a temporary directory for testing.
    This directory is automatically cleaned up after the test completes.
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

@pytest.fixture
def dataset_manager(temp_dir):
    """
    Fixture to initialize the DatasetManager with a test pickle file
    located in the temporary directory. This ensures that each test
    starts with a fresh DatasetManager.
    """
    test_pickle_file = os.path.join(temp_dir, 'test_dataset_annotation.pkl')
    return DatasetManager(test_pickle_file)

# ---------------------------------------------------
# Test Group: Annotation Loading
# ---------------------------------------------------

def test_load_annotation_new_dataset(dataset_manager):
    """
    Test loading an annotation when the pickle file does not exist.
    This ensures that a new annotation is initialized with default values.
    """
    annotation = dataset_manager.load_annotation()
    assert annotation['description'] == 'New Dataset', "Default description should be 'New Dataset'"
    assert annotation['root'] == '', "Default root should be an empty string"
    assert annotation['reorder'] == '', "Default reorder should be an empty string"

def test_load_annotation_with_custom_values(dataset_manager):
    """
    Test loading an annotation with custom description, root, and reorder
    when the pickle file does not exist.
    """
    annotation = dataset_manager.load_annotation(description="Custom Dataset", reorder="alphabetical", root="/new/root/path")
    assert annotation['description'] == 'Custom Dataset', "Description should be updated to 'Custom Dataset'"
    assert annotation['root'] == '/new/root/path', "Root should be updated to '/new/root/path'"
    assert annotation['reorder'] == 'alphabetical', "Reorder should be updated to 'alphabetical'"

def test_load_annotation_update_existing_file(dataset_manager):
    """
    Test loading an existing annotation from a pickle file and updating only certain fields (e.g., reorder).
    """
    dataset_manager.save_annotation(EasyDict({
        'description': 'Existing Dataset',
        'reorder': '',
        'root': '/old/root/path',
        'image_name': [],
        'label': np.array([]),
        'attr_name': [],
        'label_idx': EasyDict({
            'eval': [],
            'color': [],
            'extra': []
        }),
        'partition': EasyDict({
            'train': [],
            'val': [],
            'test': [],
            'trainval': []
        }),
        'weight_train': [],
        'weight_trainval': []
    }))

    annotation = dataset_manager.load_annotation(reorder="alphabetical")
    assert annotation['description'] == 'Existing Dataset', "Description should remain unchanged"
    assert annotation['root'] == '/old/root/path', "Root should remain unchanged"
    assert annotation['reorder'] == 'alphabetical', "Reorder should be updated to 'alphabetical'"

def test_load_annotation_with_partial_update(dataset_manager):
    """
    Test loading an existing annotation and updating multiple fields (e.g., root, reorder),
    leaving others (e.g., description) unchanged.
    """
    dataset_manager.save_annotation(EasyDict({
        'description': 'Existing Dataset',
        'reorder': '',
        'root': '/old/root/path',
        'image_name': [],
        'label': np.array([]),
        'attr_name': [],
        'label_idx': EasyDict({
            'eval': [],
            'color': [],
            'extra': []
        }),
        'partition': EasyDict({
            'train': [],
            'val': [],
            'test': [],
            'trainval': []
        }),
        'weight_train': [],
        'weight_trainval': []
    }))

    annotation = dataset_manager.load_annotation(root="/new/root/path", reorder="alphabetical")
    assert annotation['description'] == 'Existing Dataset', "Description should remain unchanged"
    assert annotation['root'] == '/new/root/path', "Root should be updated to '/new/root/path'"
    assert annotation['reorder'] == 'alphabetical', "Reorder should be updated to 'alphabetical'"

# ---------------------------------------------------
# Test Group: Label Handling (Add, Remove, Edit)
# ---------------------------------------------------

@pytest.mark.parametrize("label", ["gender", "age", "size"])
def test_add_remove_label(dataset_manager, label):
    """
    Test adding and removing labels in DatasetManager.
    This checks that labels can be added and removed correctly.
    Parameterized to test multiple label names.
    """
    index = dataset_manager.add_label(label)
    assert label in dataset_manager.annotation.attr_name, f"Label {label} should be added"

    dataset_manager.remove_label(index)
    assert label not in dataset_manager.annotation.attr_name, f"Label {label} should be removed"

def test_edit_label(dataset_manager):
    """
    Test editing a label in DatasetManager.
    This verifies that labels can be modified correctly.
    """
    index = dataset_manager.add_label('gender')
    dataset_manager.edit_label(index, 'new_gender')
    assert 'new_gender' in dataset_manager.annotation.attr_name, "Label should be renamed to new_gender"
    assert 'gender' not in dataset_manager.annotation.attr_name, "Original label 'gender' should not exist"

def test_remove_label_out_of_bounds(dataset_manager):
    """
    Test that removing a label with an invalid index raises an appropriate error.
    This tests boundary conditions for label removal.
    """
    with pytest.raises(IndexError):
        dataset_manager.remove_label(999)  # Index out of bounds

def test_add_duplicate_label_rejected(dataset_manager):
    """
    Test that DatasetManager prevents adding duplicate labels.
    This ensures that the same label cannot be added more than once.
    """
    dataset_manager.add_label('unique_label')
    with pytest.raises(ValueError):
        dataset_manager.add_label('unique_label')
    assert dataset_manager.annotation.attr_name.count('unique_label') == 1, "Duplicate labels should not be allowed, and should appear only once."

# ---------------------------------------------------
# Test Group: File Handling (Images and Annotations)
# ---------------------------------------------------

@patch('os.path.exists')
def test_fetch_image_with_root(mock_exists, dataset_manager):
    """
    Test fetching an image in DatasetManager with the complete root path.
    """
    mock_exists.return_value = True
    dataset_manager.annotation.root = '/test/root'
    dataset_manager.annotation.image_name.append('existing_image.jpg')
    image_path = dataset_manager.fetch_image(0, include_root_path=True)
    expected_image_path = os.path.join(dataset_manager.annotation.root, 'existing_image.jpg')
    assert image_path == expected_image_path, f"Expected {expected_image_path}, but got {image_path}"

@patch('os.path.exists')
def test_fetch_image_without_root(mock_exists, dataset_manager):
    """
    Test fetching an image in DatasetManager without the root path.
    """
    mock_exists.return_value = True
    dataset_manager.annotation.image_name.append('existing_image.jpg')
    image_name = dataset_manager.fetch_image(0, include_root_path=False)
    expected_image_name = 'existing_image.jpg'
    assert image_name == expected_image_name, f"Expected {expected_image_name}, but got {image_name}"

@patch('os.path.exists')
def test_fetch_image(mock_exists, dataset_manager):
    """
    Test fetching an image in DatasetManager. Simulates different file existence scenarios.
    """
    mock_exists.return_value = True
    initial_image_count = len(dataset_manager.annotation.image_name)
    dataset_manager.annotation.image_name.append('existing_image.jpg')
    image_index = initial_image_count
    image_path = dataset_manager.fetch_image(image_index)
    expected_image_path = os.path.join(dataset_manager.annotation.root, 'existing_image.jpg')
    assert image_path == expected_image_path, f"Expected {expected_image_path}, but got {image_path}"

@patch('os.path.exists')
def test_fetch_all_images(mock_exists, dataset_manager):
    """
    Test fetching all images in DatasetManager.
    """
    mock_exists.return_value = True
    dataset_manager.annotation.root = '/test/root'
    dataset_manager.annotation.image_name.extend(['image1.jpg', 'image2.jpg', 'image3.jpg'])
    all_images_with_root = dataset_manager.fetch_all_images(include_root_path=True)
    expected_images_with_root = [
        os.path.join(dataset_manager.annotation.root, 'image1.jpg'),
        os.path.join(dataset_manager.annotation.root, 'image2.jpg'),
        os.path.join(dataset_manager.annotation.root, 'image3.jpg'),
    ]
    assert all_images_with_root == expected_images_with_root, "Fetched images with root paths do not match expected."

    all_images_without_root = dataset_manager.fetch_all_images(include_root_path=False)
    expected_images_without_root = ['image1.jpg', 'image2.jpg', 'image3.jpg']
    assert all_images_without_root == expected_images_without_root, "Fetched images without root paths do not match expected."

def test_load_annotation_from_file(temp_dir):
    """
    Test that DatasetManager correctly handles corrupted pickle files.
    """
    corrupted_file = os.path.join(temp_dir, 'corrupted_dataset.pkl')
    with open(corrupted_file, 'wb') as f:
        f.write(b'corrupted data')  # Write some invalid pickle data
    with pytest.raises(RuntimeError, match="Failed to load annotation from corrupted pickle file"):
        dataset_manager = DatasetManager(corrupted_file)  # Error happens here

# ---------------------------------------------------
# Test Group: Error Handling
# ---------------------------------------------------

def test_handle_nonexistent_pickle_file(temp_dir):
    """
    Test that DatasetManager handles a missing pickle file correctly.
    This ensures the library doesn't crash when the annotation file is missing.
    """
    nonexistent_pickle_file = os.path.join(temp_dir, 'nonexistent.pkl')
    dataset_manager = DatasetManager(nonexistent_pickle_file)
    annotation = dataset_manager.load_annotation()
    assert annotation is not None, "New annotation should be initialized when file does not exist"

def test_invalid_image_index(dataset_manager):
    """
    Test that attempting to retrieve an image with an invalid index raises an error.
    This ensures proper bounds checking for image retrieval.
    """
    with pytest.raises(IndexError):
        dataset_manager.fetch_image(-1)  # Invalid negative index

# ---------------------------------------------------
# Test Group: Performance and Large Files
# ---------------------------------------------------

def test_large_file_handling(dataset_manager, temp_dir):
    """
    Test that DatasetManager can handle large files.
    """
    large_file = os.path.join(temp_dir, 'large_file.bin')
    with open(large_file, 'wb') as f:
        f.write(os.urandom(10**7))  # 10MB file
    dataset_manager.load_annotation()

# ---------------------------------------------------
# Test Group: Security and Path Handling
# ---------------------------------------------------

def test_special_character_in_file_names(temp_dir):
    """
    Test that DatasetManager can handle files with special characters in their names.
    This checks compatibility with non-standard file names.
    """
    special_file = os.path.join(temp_dir, 'tést_file_ü.pkl')
    with open(special_file, 'wb') as f:
        pickle.dump({'key': 'value'}, f)
    dataset_manager = DatasetManager(special_file)
    annotation = dataset_manager.load_annotation()
    assert annotation['key'] == 'value', "The content of the special character file should be loaded correctly."




# ---------------------------------------------------
# Test Group: Label Handling for Images
# ---------------------------------------------------

def test_add_image_with_default_labels(dataset_manager):
    """Test adding an image without providing labels."""
    # Initially, there should be no images
    assert len(dataset_manager.annotation.image_name) == 0, "Initially, there should be 0 images."

    # Add an image without labels
    dataset_manager.add_image('image_without_labels.jpg')

    # Check that the image has been added
    assert len(dataset_manager.annotation.image_name) == 1, "There should now be 1 image."
    assert dataset_manager.annotation.image_name[-1] == 'image_without_labels.jpg', "The last image should be the new image added."

    # Check that the labels have been added correctly (should be [0, 0] if there are 2 attributes)
    expected_labels = [0] * len(dataset_manager.annotation.attr_name)  # Assuming 2 attributes
    assert np.array_equal(dataset_manager.annotation.label[-1], expected_labels), "The last label should match the default labels added."


def test_get_labels_for_image(dataset_manager):
    """Test retrieving labels for a specific image."""
    # Add an image and verify its labels
    dataset_manager.add_image('image_for_labels.jpg')  # This will create default labels

    # Get the total number of images after adding
    total_images = len(dataset_manager.annotation.image_name)

    # Get the expected labels (should match the number of attributes)
    expected_labels = [0] * len(dataset_manager.annotation.attr_name)  # Create a list of zeros matching attr_name length

    # Get labels for the last added image
    labels = dataset_manager.get_labels_for_image(total_images - 1)  # Use total_images - 1 for the last index
    assert labels == expected_labels, f"Expected labels for the last image should be {expected_labels}"

    # Test for out-of-range index
    with pytest.raises(IndexError):
        dataset_manager.get_labels_for_image(total_images)  # Out of range, should raise IndexError


def test_remove_label_from_image(dataset_manager):
    """Test removing the label from a specific image."""
    # Add an image to ensure it has a label
    dataset_manager.add_image('image_to_remove_label.jpg')  # This will create default labels based on attr_name
    
    # Initial label check
    initial_labels = [0] * len(dataset_manager.annotation.attr_name)  # Generate initial label based on attr_name
    assert np.array_equal(dataset_manager.annotation.label[0], initial_labels), \
        f"Initial label for the image should be {initial_labels}"

    # Remove label from the first image
    dataset_manager.remove_label_from_image(0)
    assert np.array_equal(dataset_manager.annotation.label[0], initial_labels), \
        "Label should be reset to default after removal."

    with pytest.raises(IndexError):
        dataset_manager.remove_label_from_image(1)  # Out of range


def test_edit_label_for_image(dataset_manager):
    """Test editing an existing label for a specific image."""
    # Add an image to ensure it has a label
    dataset_manager.add_image('image_to_edit_label.jpg')  # This will create default labels based on attr_name

    new_label = [1] * len(dataset_manager.annotation.attr_name)  # Create a new label with ones
    dataset_manager.edit_label_for_image(0, new_label)
    assert np.array_equal(dataset_manager.annotation.label[0], new_label), \
        f"Label for the image should be updated to {new_label}"

    with pytest.raises(IndexError):
        dataset_manager.edit_label_for_image(1, new_label)  # Out of range

    with pytest.raises(ValueError):
        dataset_manager.edit_label_for_image(0, [1])  # Size does not match attributes


def test_add_image_with_custom_labels(dataset_manager):
    """Test adding an image with custom labels."""
    # Initially, there should be no images
    assert len(dataset_manager.annotation.image_name) == 0, "Initially, there should be 0 images."
    
    # Create custom labels that match the number of attributes
    custom_labels = [1] * len(dataset_manager.annotation.attr_name)  # Match the size with the number of attributes
    dataset_manager.add_image('image_with_labels.jpg', custom_labels)

    # Check that the image has been added
    assert len(dataset_manager.annotation.image_name) == 1, "There should now be 1 image."
    assert dataset_manager.annotation.image_name[-1] == 'image_with_labels.jpg', \
        "The last image should be the new image added."

    # Check that the labels have been added correctly
    assert np.array_equal(dataset_manager.annotation.label[-1], custom_labels), \
        "The last label should match the custom labels added."


def test_add_image_with_invalid_labels(dataset_manager):
    """Test adding an image with invalid labels."""
    assert len(dataset_manager.annotation.image_name) == 0, "Initially, there should be 0 images."

    # Attempt to add an image with invalid label length
    with pytest.raises(ValueError):
        dataset_manager.add_image('image_with_invalid_labels.jpg', [1] * (len(dataset_manager.annotation.attr_name) + 1))  # One less than needed


def test_remove_image_and_check_labels(dataset_manager):
    """Test removing an image and ensuring the labels are correctly updated."""
    # Add two attributes first
    dataset_manager.add_label('Label1')
    dataset_manager.add_label('Label2')

    # Add two images with labels
    dataset_manager.add_image('image1.jpg', [1, 0])
    dataset_manager.add_image('image2.jpg', [0, 1])

    # Remove the first image
    dataset_manager.remove_image(0)

    # Ensure the image and label are removed, and the second image/label is still present
    assert dataset_manager.annotation.image_name == ['image2.jpg'], "First image should be removed."
    assert np.array_equal(dataset_manager.annotation.label, [[0, 1]]), "First image's label should be removed."

def test_remove_all_images(dataset_manager):
    """Test removing all images from the dataset."""
    # Add attributes first
    dataset_manager.add_label('Label1')
    dataset_manager.add_label('Label2')

    # Add multiple images
    dataset_manager.add_image('image1.jpg', [1, 0])
    dataset_manager.add_image('image2.jpg', [0, 1])
    
    # Remove both images
    dataset_manager.remove_image(1)  # Remove the second image first
    dataset_manager.remove_image(0)  # Now remove the first image

    # Check that all images and labels are gone
    assert len(dataset_manager.annotation.image_name) == 0, "All images should be removed."
    assert dataset_manager.annotation.label.size == 0, "All labels should be removed."

def test_fetch_image_invalid_root(dataset_manager):
    """Test fetching an image with an invalid root path."""
    # Add an image
    dataset_manager.annotation.root = '/invalid/root'
    dataset_manager.add_image('image1.jpg')

    # Attempt to fetch the image with an invalid root path
    with pytest.raises(FileNotFoundError):
        dataset_manager.fetch_image(0, include_root_path=True)


def test_remove_label_empty_dataset(dataset_manager):
    """Test removing a label from an empty dataset."""
    with pytest.raises(IndexError):
        dataset_manager.remove_label(0)  # No labels exist, so this should raise an error

def test_fetch_all_images_empty_dataset(dataset_manager):
    """Test fetching all images when no images exist."""
    all_images = dataset_manager.fetch_all_images()
    assert all_images == [], "Should return an empty list when no images are in the dataset."



# ---------------------------------------------------
# Test Group: Integration Testing (End-to-End)
# ---------------------------------------------------

@pytest.fixture
def temp_pickle_file():
    """Creates a temporary pickle file for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        pickle_file = os.path.join(temp_dir, 'test_dataset.pkl')
        yield pickle_file

def test_dataset_manager_integration(temp_pickle_file):
    """Comprehensive integration test for the DatasetManager class."""

    # Step 1: Initialize the DatasetManager
    manager = DatasetManager(temp_pickle_file)
    print("\n--- Step 1: Initialized DatasetManager ---")
    print(f"Description: {manager.annotation.description}")
    print(f"Attributes (before adding any): {manager.annotation.attr_name}")
    print(f"Images (before adding any): {manager.annotation.image_name}")
    
    assert manager.annotation.description == 'New Dataset'
    assert len(manager.annotation.attr_name) == 0
    assert len(manager.annotation.image_name) == 0

    # Step 2: Add Images without Labels
    print("\n--- Step 2: Adding Images Without Labels ---")
    
    # Add three images without labels
    manager.add_image('image1.jpg')
    manager.add_image('image2.jpg')
    manager.add_image('image3.jpg')

    print("After adding three images",manager.annotation.partition.train)
    
    print(f"Images after adding three images without labels: {manager.annotation.image_name}")
    assert manager.annotation.image_name == ['image1.jpg', 'image2.jpg', 'image3.jpg']
    
       # Check that labels are empty arrays with correct shape
    expected_labels = np.empty((3, 0), dtype=object)  # No attributes, labels are empty for each image
    np.testing.assert_array_equal(manager.annotation.label, expected_labels)
    print(f"Labels after adding three images without labels (should be empty):\n{manager.annotation.label}")


    # Step 3: Add First Label and Verify
    print("\n--- Step 3: Adding First Label ---")
    manager.add_label('Label1')
    
    # Check if label is added to all images
    expected_labels = np.zeros((3, 1))  # 3 images, 1 label initialized to 0
    np.testing.assert_array_equal(manager.annotation.label, expected_labels)
    print(f"Labels after adding 'Label1':\n{manager.annotation.label}")

    # Step 4: Add Second Label and Verify
    print("\n--- Step 4: Adding Second Label ---")
    manager.add_label('Label2')

    # Check if second label is added to all images
    expected_labels = np.zeros((3, 2))  # 3 images, 2 labels initialized to 0
    np.testing.assert_array_equal(manager.annotation.label, expected_labels)
    print(f"Labels after adding 'Label2':\n{manager.annotation.label}")

    # Step 5: Remove Middle Image and Verify
    print("\n--- Step 5: Removing Middle Image ---")
    print(f"Images before removing 'image2.jpg': {manager.annotation.image_name}")
    manager.remove_image(1)
    print("train After removing one image",manager.annotation.partition.train)

    # Check that the middle image ('image2.jpg') and its labels are removed
    expected_labels = np.zeros((2, 2))  # 2 images left, both with 2 labels
    np.testing.assert_array_equal(manager.annotation.label, expected_labels)
    assert manager.annotation.image_name == ['image1.jpg', 'image3.jpg']
    print(f"Images after removing 'image2.jpg': {manager.annotation.image_name}")
    print(f"Labels after removing 'image2.jpg':\n{manager.annotation.label}")

    # Step 6: Remove All Labels and Verify
    print("\n--- Step 6: Removing All Labels ---")
    print(f"Attributes before removing all labels: {manager.annotation.attr_name}")

    # Remove 'Label2' first, then 'Label1'
    manager.remove_label(1)
    manager.remove_label(0)
    
    # Check that all labels are removed
    assert len(manager.annotation.attr_name) == 0
    assert manager.annotation.label.size == 0
    print(f"Attributes after removing all labels: {manager.annotation.attr_name}")
    print(f"Labels after removing all labels (should be empty):\n{manager.annotation.label}")

    # Step 7: Add New Label and Check Configuration
    print("\n--- Step 7: Adding New Label After Removing All ---")
    manager.add_label('NewLabel')

    # Check that the new label is added to both images
    expected_labels = np.zeros((2, 1))  # 2 images, 1 new label
    np.testing.assert_array_equal(manager.annotation.label, expected_labels)
    print(f"Labels after adding 'NewLabel':\n{manager.annotation.label}")

    # Step 8: Edit Labels for Both Images
    print("\n--- Step 8: Editing Labels ---")
    manager.edit_label_for_image(0, [1])  # Set the first image label to [1]
    manager.edit_label_for_image(1, [0])  # Set the second image label to [0]

    expected_labels = np.array([[1], [0]])
    np.testing.assert_array_equal(manager.annotation.label, expected_labels)
    print(f"Labels after editing:\n{manager.annotation.label}")

    # Step 9: Error Handling (Before label removal)
    print("\n--- Step 9: Error Handling ---")
    with pytest.raises(ValueError):
        print("Testing error for adding 'image4.jpg' with invalid label length")
        manager.add_image('image4.jpg', labels=[1, 1])  # Invalid label length

    with pytest.raises(IndexError):
        print("Testing error for editing labels for a non-existent image")
        manager.edit_label_for_image(5, [0])  # Invalid image index

    with pytest.raises(IndexError):
        print("Testing error for removing a non-existent label")
        manager.remove_label(10)  # Invalid label index

    # Step 10: Fetch Images
    print("\n--- Step 10: Fetching Images ---")
    image_name = manager.fetch_image(0)
    print(f"Fetched image at index 0: {image_name}")
    assert image_name == 'image1.jpg'

    all_images = manager.fetch_all_images()
    print(f"All images fetched: {all_images}")
    assert all_images == ['image1.jpg', 'image3.jpg']

    # Step 11: Persistence
    print("\n--- Step 11: Testing Persistence ---")
    print("Reloading the manager and verifying state")
    new_manager = DatasetManager(temp_pickle_file)
    print(f"Reloaded manager state: attr_name={new_manager.annotation.attr_name}, image_name={new_manager.annotation.image_name}")
    assert new_manager.annotation.attr_name == ['NewLabel']
    assert new_manager.annotation.image_name == ['image1.jpg', 'image3.jpg']
    expected_labels = np.array([[1], [0]])
    print(type(new_manager.annotation.label))
    np.testing.assert_array_equal(new_manager.annotation.label, expected_labels)
    print(f"Labels after reloading manager:\n{new_manager.annotation.label}")
# ---------------------------------------------------
# END OF TEST CASES
# ---------------------------------------------------