import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock
import numpy as np
from easydict import EasyDict
from backend.annotation_manager.dataset_utils import DatasetManager
import logging
import pickle

#################
#
#  You can run this by this
#  export PYTHONPATH=$(pwd)     
#  pytest -v backend/tests/test_dataset_utils.py
#
#
################

# Configure logging for the tests
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# ---------------------------------------------------
# Fixtures - Setup and Teardown for Tests
# ---------------------------------------------------


# ---------------------------------------------------
# Custom Mock Class for Annotation (Pickle-safe)
# ---------------------------------------------------

class MockAnnotation:
    def __init__(self):
        self.attr_name = []
        self.image_name = []
        self.label = np.array([], dtype=int)
        self.description = 'New Dataset'


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

    # Try to import the actual Annotation class
    try:
        from backend.annotation_manager.dataset_utils import Annotation
    except ImportError:
        # If Annotation class is not directly importable, use MockAnnotation class
        Annotation = MockAnnotation

    # Ensure the pickle file exists with the MockAnnotation or real Annotation object
    if not os.path.exists(test_pickle_file):
        empty_annotation = Annotation()  # Using the real or mocked Annotation object
        with open(test_pickle_file, 'wb') as f:
            pickle.dump(empty_annotation, f)

    config = {
    'PROJECT_NAME': 'PAR for zs',
    'FILES': {
        'BASE_DIR': temp_dir,
    },
    'DATASET': {
        'TYPE': 'pedes',
        'NAME': 'RAP2',
        'TRAIN_SPLIT': 'trainval',
        'VAL_SPLIT': 'test',
        'ZERO_SHOT': True,
        'HEIGHT': 256,
        'WIDTH': 192,
        'PATH': test_pickle_file  # Essential for DatasetManager
    },
    'ANNOTATION': {
        'BASE_DIR': os.path.join(temp_dir, 'labeling')
    }
    }

    manager = DatasetManager(test_pickle_file, config)

    # Assert that 'annotation' is correctly initialized
    assert hasattr(manager, 'annotation'), "DatasetManager should have an 'annotation' attribute after initialization."

    return manager

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
    success = dataset_manager.add_label(label)
    assert success is True, f"Label {label} should be added successfully"
    assert label in dataset_manager.annotation.attr_name, f"Label {label} should be in annotation"

    label_index = dataset_manager.annotation.attr_name.index(label)
    success = dataset_manager.remove_label(label_index)
    assert success is True, f"Label {label} should be removed successfully"
    assert label not in dataset_manager.annotation.attr_name, f"Label {label} should no longer be in annotation"

def test_edit_label(dataset_manager):
    """
    Test editing a label in DatasetManager.
    This verifies that labels can be modified correctly.
    """
    success = dataset_manager.add_label('gender')
    assert success is True, "Label 'gender' should be added successfully"
    index = dataset_manager.annotation.attr_name.index('gender')
    success = dataset_manager.edit_label(index, 'new_gender')
    assert success is True, "Label should be edited successfully"
    assert 'new_gender' in dataset_manager.annotation.attr_name, "Label should be renamed to new_gender"
    assert 'gender' not in dataset_manager.annotation.attr_name, "Original label 'gender' should not exist"

def test_add_duplicate_label_rejected(dataset_manager):
    """
    Test that DatasetManager prevents adding duplicate labels.
    This ensures that the same label cannot be added more than once.
    """
    success = dataset_manager.add_label('unique_label')
    assert success is True, "Label 'unique_label' should be added successfully"

    success = dataset_manager.add_label('unique_label')
    assert success is False, "Duplicate label should be rejected"
    assert dataset_manager.annotation.attr_name.count('unique_label') == 1, "Duplicate labels should not be allowed"

# ---------------------------------------------------
# Test Group: Image Handling (Add, Remove)
# ---------------------------------------------------

@patch('os.path.exists', return_value=True)  # Mock file existence check
@patch('PIL.Image.open')  # Mock image opening
def test_add_image_with_default_labels(mock_open, mock_exists, dataset_manager):
    """Test adding an image without providing labels."""
    # Initially, there should be no images
    assert len(dataset_manager.annotation.image_name) == 0, "Initially, there should be 0 images."

    # Create a mock image object with size attribute and close method
    mock_image = MagicMock()
    mock_image.size = (dataset_manager.image_width, dataset_manager.image_height)
    mock_image.close = MagicMock()

    # Set Image.open to return the mock image
    mock_open.return_value = mock_image

    # The image path being tested
    image_path = 'image_without_labels.jpg'
    abs_image_path = os.path.abspath(image_path)

    # Add an image without labels
    success = dataset_manager.add_image(image_path)
    if not success:
        print(f"Image addition failed. Image path: {abs_image_path}, Size: {mock_image.size}")
        if abs_image_path in dataset_manager.annotation.image_name:
            print(f"Image already exists: {abs_image_path}")
        if os.path.splitext(image_path)[-1].lower() not in dataset_manager.allowed_formats:
            print(f"Invalid file format: {os.path.splitext(image_path)[-1].lower()}")

    # Assert that the image was added successfully
    assert success is True, "Image should be added successfully"
    assert len(dataset_manager.annotation.image_name) == 1, "There should now be 1 image."
    assert dataset_manager.annotation.image_name[-1] == abs_image_path, \
        "The last image should be the new image added."

    # Check that the labels have been added correctly (should be default)
    expected_labels = np.zeros((1, 0), dtype=int)
    np.testing.assert_array_equal(dataset_manager.annotation.label, expected_labels)

@patch('os.path.exists', return_value=True)
@patch('PIL.Image.open')
def test_add_image_with_custom_labels(mock_open, mock_exists, dataset_manager):
    """Test adding an image with custom labels."""
    # Add a label first
    dataset_manager.add_label('test_label')

    # Create a mock image object
    mock_image = MagicMock()
    mock_image.size = (dataset_manager.image_width, dataset_manager.image_height)
    mock_image.close = MagicMock()
    mock_open.return_value = mock_image

    # Add an image with labels
    image_path = 'image_with_labels.jpg'
    abs_image_path = os.path.abspath(image_path)
    success = dataset_manager.add_image(image_path, labels=[1])

    assert success is True, "Image should be added with custom labels"
    assert len(dataset_manager.annotation.image_name) == 1, "There should now be 1 image."
    assert dataset_manager.annotation.image_name[-1] == abs_image_path, \
        "The last image should be the new image added."
    expected_labels = np.array([[1]], dtype=int)
    np.testing.assert_array_equal(dataset_manager.annotation.label, expected_labels)

@patch('os.path.exists', return_value=True)
@patch('PIL.Image.open')
def test_add_image_with_invalid_labels(mock_open, mock_exists, dataset_manager):
    """Test adding an image with invalid labels."""
    # Add a label first
    dataset_manager.add_label('test_label')

    # Create a mock image object
    mock_image = MagicMock()
    mock_image.size = (dataset_manager.image_width, dataset_manager.image_height)
    mock_image.close = MagicMock()
    mock_open.return_value = mock_image

    # Add an image with incorrect number of labels
    image_path = 'image_with_invalid_labels.jpg'
    success = dataset_manager.add_image(image_path, labels=[1, 0])  # Incorrect label length

    assert success is False, "Adding an image with invalid labels should fail."

# ---------------------------------------------------
# Additional Tests for DatasetManager Methods
# ---------------------------------------------------

def test_fetch_labels_by_image_name(dataset_manager):
    """Test fetching labels by image name."""
    # Add a label and an image
    dataset_manager.add_label('test_label')
    with patch('os.path.exists', return_value=True), \
         patch('PIL.Image.open', return_value=MagicMock(size=(192, 256))):
        dataset_manager.add_image('test_image.jpg', [1])

    # Fetch labels by image name
    success, labels = dataset_manager.fetch_labels_by_image_name('test_image.jpg')
    assert success is True, "Should successfully fetch labels by image name."
    assert labels == [1], "Labels should match the ones assigned during image addition."

@patch('os.path.exists', return_value=True)
@patch('PIL.Image.open')
def test_fetch_image_by_name(mock_image_open, mock_path_exists, dataset_manager):
    """Test fetching an image by its name."""
    # Create a mock image object
    mock_image = MagicMock()
    mock_image.size = (192, 256)
    mock_image.close = MagicMock()
    mock_image_open.return_value = mock_image

    # Add an image
    dataset_manager.add_image('test_image.jpg')

    # Fetch image by name
    success, image = dataset_manager.fetch_image_by_name('test_image.jpg')
    assert success is True, "Should successfully fetch image by name."
    assert image == mock_image, "Fetched image should match the mock image."

@patch('os.path.exists', return_value=True)
def test_fetch_image_path(mock_exists, dataset_manager):
    """Test fetching the full image path by index."""
    # Mock Image.open
    with patch('PIL.Image.open', return_value=MagicMock(size=(192, 256))):
        # Add an image
        dataset_manager.add_image('test_image.jpg')

    # Fetch image path
    success, image_path = dataset_manager.fetch_image_path(0)
    expected_path = dataset_manager.annotation.image_name[0]

    assert success is True, "Should successfully fetch image path by index."
    assert image_path == expected_path, "Image path should match."

def test_fetch_image(dataset_manager):
    """Test opening and returning an image by index."""
    # Add an image
    mock_image = MagicMock()
    mock_image.size = (192, 256)
    mock_image.close = MagicMock()
    with patch('os.path.exists', return_value=True), \
         patch('PIL.Image.open', return_value=mock_image):
        dataset_manager.add_image('test_image.jpg')

        # Fetch image
        success, image = dataset_manager.fetch_image(0)
        assert success is True, "Should successfully fetch image by index."
        assert image == mock_image, "Fetched image should match the mock image."

def test_remove_image(dataset_manager):
    """Test removing an image by index."""
    # Add an image
    with patch('os.path.exists', return_value=True), \
         patch('PIL.Image.open', return_value=MagicMock(size=(192, 256))):
        dataset_manager.add_image('test_image.jpg')

    # Remove the image
    success = dataset_manager.remove_image(0)
    assert success is True, "Should successfully remove the image."
    assert len(dataset_manager.annotation.image_name) == 0, "Image list should be empty after removal."

def test_get_labels_for_image(dataset_manager):
    """Test retrieving labels for a specific image by its index."""
    # Add a label and an image
    dataset_manager.add_label('test_label')
    with patch('os.path.exists', return_value=True), \
         patch('PIL.Image.open', return_value=MagicMock(size=(192, 256))):
        dataset_manager.add_image('test_image.jpg', [1])

    # Get labels for the image
    success, labels = dataset_manager.get_labels_for_image(0)
    assert success is True, "Should successfully get labels for the image."
    assert labels == [1], "Labels should match the ones assigned during image addition."

def test_edit_label_for_image(dataset_manager):
    """Test editing a label for a specific image."""
    # Add a label and an image
    dataset_manager.add_label('test_label')
    with patch('os.path.exists', return_value=True), \
         patch('PIL.Image.open', return_value=MagicMock(size=(192, 256))):
        dataset_manager.add_image('test_image.jpg', [0])

    # Edit label for the image
    success = dataset_manager.edit_label_for_image(0, [1])
    assert success is True, "Should successfully edit label for the image."

    # Verify that the label has been updated
    success, labels = dataset_manager.get_labels_for_image(0)
    assert labels == [1], "Labels should be updated to the new values."

def test_remove_label_from_image(dataset_manager):
    """Test removing labels from a specific image."""
    # Add a label and an image
    dataset_manager.add_label('test_label')
    with patch('os.path.exists', return_value=True), \
         patch('PIL.Image.open', return_value=MagicMock(size=(192, 256))):
        dataset_manager.add_image('test_image.jpg', [1])

    # Remove label from the image
    success = dataset_manager.remove_label_from_image(0)
    assert success is True, "Should successfully remove labels from the image."

    # Verify that the labels are reset
    success, labels = dataset_manager.get_labels_for_image(0)
    assert labels == [0], "Labels should be reset to default values."

def test_get_all_labels(dataset_manager):
    """Test fetching all labels from the dataset."""
    # Add labels and images
    dataset_manager.add_label('label1')
    dataset_manager.add_label('label2')
    with patch('os.path.exists', return_value=True), \
         patch('PIL.Image.open', return_value=MagicMock(size=(192, 256))):
        dataset_manager.add_image('image1.jpg', [1, 0])
        dataset_manager.add_image('image2.jpg', [0, 1])

    # Get all labels
    success, labels = dataset_manager.get_all_labels()
    assert success is True, "Should successfully fetch all labels."
    expected_labels = np.array([[1, 0], [0, 1]], dtype=int)
    np.testing.assert_array_equal(labels, expected_labels)

def test_save_and_load_annotation(dataset_manager):
    """Test saving and loading the annotation."""
    # Add labels and images
    dataset_manager.add_label('label1')
    with patch('os.path.exists', return_value=True), \
         patch('PIL.Image.open', return_value=MagicMock(size=(192, 256))):
        dataset_manager.add_image('image1.jpg')

    # Save the annotation
    save_success = dataset_manager.save_annotation()
    assert save_success is True, "Should successfully save the annotation."

    # Load the annotation
    load_success, annotation = dataset_manager.load_annotation()
    assert load_success is True, "Should successfully load the annotation."
    assert annotation.attr_name == dataset_manager.annotation.attr_name, "Attributes should match after loading."
    assert annotation.image_name == dataset_manager.annotation.image_name, "Image names should match after loading."

def test_remove_label_out_of_bounds(dataset_manager):
    """Test removing a label with an invalid index."""
    # Try to remove a label when none exist
    success = dataset_manager.remove_label(0)
    assert success is False, "Removing label out of bounds should fail."

    # Add a label and then try to remove an invalid index
    dataset_manager.add_label('label1')
    success = dataset_manager.remove_label(1)  # Index out of bounds
    assert success is False, "Removing label with invalid index should fail."

def test_remove_image_out_of_bounds(dataset_manager):
    """Test removing an image with an invalid index."""
    # Try to remove an image when none exist
    success = dataset_manager.remove_image(0)
    assert success is False, "Removing image out of bounds should fail."

    # Add an image and then try to remove an invalid index
    with patch('os.path.exists', return_value=True), \
         patch('PIL.Image.open', return_value=MagicMock(size=(192, 256))):
        dataset_manager.add_image('image1.jpg')

    success = dataset_manager.remove_image(1)  # Index out of bounds
    assert success is False, "Removing image with invalid index should fail."

# ---------------------------------------------------
# Integration Test
# ---------------------------------------------------

def test_dataset_manager_integration(temp_dir):
    """Comprehensive integration test for the DatasetManager class."""

    # Prepare temporary pickle file and config
    temp_pickle_file = os.path.join(temp_dir, 'test_dataset_annotation.pkl')
    config = {
        'FILES': {'BASE_DIR': temp_dir},
        'DATASET': {'HEIGHT': 256, 'WIDTH': 192, 'TRAIN_SPLIT': 'train', 'VAL_SPLIT': 'val', 'ZERO_SHOT': True}
    }

    # Step 1: Initialize the DatasetManager
    manager = DatasetManager(temp_pickle_file, config)
    print("\n--- Step 1: Initialized DatasetManager ---")
    print(f"Description: {manager.annotation.description}")
    print(f"Attributes (before adding any): {manager.annotation.attr_name}")
    print(f"Images (before adding any): {manager.annotation.image_name}")
    
    assert manager.annotation.description == 'New Dataset'
    assert len(manager.annotation.attr_name) == 0
    assert len(manager.annotation.image_name) == 0

    # Step 2: Add Images without Labels
    print("\n--- Step 2: Adding Images Without Labels ---")
    
    # Mock os.path.exists and PIL.Image.open
    with patch('os.path.exists', return_value=True), \
         patch('PIL.Image.open', return_value=MagicMock(size=(192, 256))):

        # Add three images without labels
        manager.add_image('image1.jpg')
        manager.add_image('image2.jpg')
        manager.add_image('image3.jpg')

    print(f"Images after adding three images without labels: {manager.annotation.image_name}")
    expected_image_names = [os.path.abspath('image1.jpg'), os.path.abspath('image2.jpg'), os.path.abspath('image3.jpg')]
    assert manager.annotation.image_name == expected_image_names
    
    # Check that labels are empty arrays with correct shape
    expected_labels = np.zeros((3, 0), dtype=int)  # No attributes, labels are empty for each image
    np.testing.assert_array_equal(manager.annotation.label, expected_labels)
    print(f"Labels after adding three images without labels (should be empty):\n{manager.annotation.label}")

    # Step 3: Add First Label and Verify
    print("\n--- Step 3: Adding First Label ---")
    manager.add_label('Label1')
    
    # Check if label is added to all images
    expected_labels = np.zeros((3, 1), dtype=int)  # 3 images, 1 label initialized to 0
    np.testing.assert_array_equal(manager.annotation.label, expected_labels)
    print(f"Labels after adding 'Label1':\n{manager.annotation.label}")

    # Step 4: Add Second Label and Verify
    print("\n--- Step 4: Adding Second Label ---")
    manager.add_label('Label2')

    # Check if second label is added to all images
    expected_labels = np.zeros((3, 2), dtype=int)  # 3 images, 2 labels initialized to 0
    np.testing.assert_array_equal(manager.annotation.label, expected_labels)
    print(f"Labels after adding 'Label2':\n{manager.annotation.label}")

    # Step 5: Remove Middle Image and Verify
    print("\n--- Step 5: Removing Middle Image ---")
    print(f"Images before removing 'image2.jpg': {manager.annotation.image_name}")
    manager.remove_image(1)

    # Check that the middle image ('image2.jpg') and its labels are removed
    expected_labels = np.zeros((2, 2), dtype=int)  # 2 images left, both with 2 labels
    np.testing.assert_array_equal(manager.annotation.label, expected_labels)
    expected_image_names = [os.path.abspath('image1.jpg'), os.path.abspath('image3.jpg')]
    assert manager.annotation.image_name == expected_image_names
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
    expected_labels = np.zeros((2, 1), dtype=int)  # 2 images, 1 new label
    np.testing.assert_array_equal(manager.annotation.label, expected_labels)
    print(f"Labels after adding 'NewLabel':\n{manager.annotation.label}")

    # Step 8: Edit Labels for Both Images
    print("\n--- Step 8: Editing Labels ---")
    manager.edit_label_for_image(0, [1])  # Set the first image label to [1]
    manager.edit_label_for_image(1, [0])  # Set the second image label to [0]

    expected_labels = np.array([[1], [0]], dtype=int)
    np.testing.assert_array_equal(manager.annotation.label, expected_labels)
    print(f"Labels after editing:\n{manager.annotation.label}")

    # Step 9: Error Handling
    print("\n--- Step 9: Error Handling ---")
    # Since methods return False instead of raising exceptions, we need to assert on the return value

    # Test adding image with invalid label length
    with patch('os.path.exists', return_value=True), \
         patch('PIL.Image.open', return_value=MagicMock(size=(192, 256))):
        success = manager.add_image('image4.jpg', labels=[1, 1])  # Invalid label length
        assert success is False, "Adding image with invalid label length should fail."

    # Test editing labels for a non-existent image
    success = manager.edit_label_for_image(5, [0])  # Invalid image index
    assert success is False, "Editing labels for non-existent image should fail."

    # Test removing a non-existent label
    success = manager.remove_label(10)  # Invalid label index
    assert success is False, "Removing a non-existent label should fail."

    # Step 10: Fetch Images
    print("\n--- Step 10: Fetching Images ---")
    # Fetch image at index 0
    mock_image = MagicMock()
    mock_image.size = (192, 256)
    mock_image.close = MagicMock()
    with patch('os.path.exists', return_value=True), \
         patch('PIL.Image.open', return_value=mock_image):
        success, image = manager.fetch_image(0)
        assert success is True, "Fetching image at index 0 should succeed."
        assert image == mock_image, "Fetched image should be the mock image."

    # Fetch all image names
    all_images = manager.annotation.image_name
    print(f"All images fetched: {all_images}")
    expected_image_names = [os.path.abspath('image1.jpg'), os.path.abspath('image3.jpg')]
    assert all_images == expected_image_names

    # Step 11: Persistence
    print("\n--- Step 11: Testing Persistence ---")
    print("Reloading the manager and verifying state")
    new_manager = DatasetManager(temp_pickle_file, config)
    print(f"Reloaded manager state: attr_name={new_manager.annotation.attr_name}, image_name={new_manager.annotation.image_name}")
    assert new_manager.annotation.attr_name == ['NewLabel']
    assert new_manager.annotation.image_name == expected_image_names
    expected_labels = np.array([[1], [0]], dtype=int)
    np.testing.assert_array_equal(new_manager.annotation.label, expected_labels)
    print(f"Labels after reloading manager:\n{new_manager.annotation.label}")

# ---------------------------------------------------
# END OF TEST FILE
# ---------------------------------------------------