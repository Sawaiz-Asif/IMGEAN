import numpy as np
import os
import pickle
import logging
from easydict import EasyDict
from PIL import Image

# Configure logging
logging.basicConfig(filename='dataset_manager.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class DatasetManager:
    def __init__(self, pickle_file, config, description=None, reorder=None):
        """
        Initializes the DatasetManager by loading an annotation from a pickle file if it exists.
        If the pickle file does not exist, it initializes a new dataset and saves it as a pickle.

        Args:
            pickle_file (str): The path to the pickle file where the dataset is stored.
            config (dict): The configuration dictionary loaded from the config file.
            description (str, optional): A custom description for the dataset. Defaults to None.
            reorder (str, optional): A reorder value to set or replace. Defaults to None.

        Initializes:
            self.initialized (bool): Whether the initialization was successful.
        """
        try:
            self.config = config

            # Set the root and ensure directories exist
            self.root = self.config['FILES']['BASE_DIR']
            if not os.path.exists(self.root):
                try:
                    os.makedirs(self.root)
                except OSError as e:
                    logging.error(f"Error creating directory {self.root}: {e}")
                    self.initialized = False
                    return

            # Allowed formats (could be added to the config)
            self.allowed_formats = ['.png', '.jpg']

            # Constraints for image dimensions
            self.image_height = self.config['DATASET']['HEIGHT']
            self.image_width = self.config['DATASET']['WIDTH']

            # Other config values
            self.train_split = self.config['DATASET']['TRAIN_SPLIT']
            self.val_split = self.config['DATASET']['VAL_SPLIT']
            self.zero_shot = self.config['DATASET']['ZERO_SHOT']

            self.pickle_file = pickle_file
            success, annotation = self.load_annotation(description, reorder)
            if not success:
                logging.error("Failed to load annotation.")
                self.initialized = False
                return

            self.annotation = annotation
            self.initialized = True

        except Exception as e:
            logging.error(f"Error in __init__: {e}")
            self.initialized = False

    def load_annotation(self, description=None, reorder=None, root=None):
        """
        Loads the annotation from a pickle file if it exists. If the pickle file does not exist,
        it initializes a new dataset with default values and saves it.

        Returns:
            tuple: (bool, EasyDict): True and annotation if successful, False otherwise.
        """
        try:
            if os.path.exists(self.pickle_file):
                with open(self.pickle_file, 'rb') as f:
                    annotation = pickle.load(f)

                modified = False
                if description:
                    annotation['description'] = description
                    modified = True
                if reorder:
                    annotation['reorder'] = reorder
                    modified = True
                if root:
                    annotation['root'] = root
                    modified = True

                if modified:
                    self.save_annotation(annotation)
            else:
                annotation = EasyDict({
                    'description': description if description else 'New Dataset',
                    'reorder': reorder if reorder else '',
                    'root': root if root else '',
                    'image_name': [],
                    'label': np.zeros((0, 0), dtype=int),
                    'attr_name': [],
                    'label_idx': EasyDict({'eval': [], 'color': [], 'extra': []}),
                    'partition': EasyDict({'train': [], 'val': [], 'test': [], 'trainval': []}),
                    'weight_train': [],
                    'weight_trainval': []
                })
                self.save_annotation(annotation)

            return True, annotation
        except (IOError, pickle.PickleError) as e:
            logging.error(f"Error in load_annotation: {e}")
            return False, None

    def save_annotation(self, annotation=None):
        """
        Saves the current annotation to the pickle file.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            with open(self.pickle_file, 'wb') as f:
                pickle.dump(annotation or self.annotation, f)
            return True
        except IOError as e:
            logging.error(f"Error in save_annotation: {e}")
            return False

    def get_all_labels(self):
        """
        Fetches all labels from the dataset.

        Returns:
            tuple: (bool, np.ndarray): True and labels if successful, False otherwise.
        """
        try:
            return True, self.annotation.label
        except AttributeError as e:
            logging.error(f"Error in get_all_labels: {e}")
            return False, None

    def add_label(self, new_label, default_value=0):
        """
        Adds a new label to the dataset and assigns it a default value for all images.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if new_label in self.annotation.attr_name:
                return False

            self.annotation.attr_name.append(new_label)
            if len(self.annotation.image_name) == 0:
                self.annotation.label = np.zeros((0, len(self.annotation.attr_name)), dtype=int)
            else:
                new_default_column = np.full((self.annotation.label.shape[0], 1), default_value, dtype=int)
                self.annotation.label = np.column_stack((self.annotation.label, new_default_column))

            self.save_annotation()
            return True
        except ValueError as e:
            logging.error(f"Error in add_label: {e}")
            return False

    def edit_label(self, label_index, new_label):
        """
        Modifies an existing label by index.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if 0 <= label_index < len(self.annotation.attr_name):
                self.annotation.attr_name[label_index] = new_label
                self.save_annotation()
                return True
            else:
                return False
        except IndexError as e:
            logging.error(f"Error in edit_label: {e}")
            return False

    def remove_label(self, label_index):
        """
        Removes a label from all images by index.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if not (0 <= label_index < len(self.annotation.attr_name)):
                return False

            self.annotation.attr_name.pop(label_index)
            if self.annotation.label.size > 0:
                if self.annotation.label.shape[1] <= label_index:
                    return False

                self.annotation.label = np.delete(self.annotation.label, label_index, axis=1)

            self.save_annotation()
            return True
        except IndexError as e:
            logging.error(f"Error in remove_label: {e}")
            return False

    def fetch_labels_by_image_name(self, image_name):
        """
        Fetches the labels associated with a specific image by its name or path.

        Returns:
            tuple: (bool, list): True and labels if successful, False otherwise.
        """
        try:
            image_path = os.path.normpath(os.path.abspath(image_name))

            if image_path not in self.annotation.image_name:
                return False, None

            image_index = self.annotation.image_name.index(image_path)
            labels = self.annotation.label[image_index].tolist()
            return True, labels
        except Exception as e:
            logging.error(f"Error in fetch_labels_by_image_name: {e}")
            return False, None

    def fetch_image_by_name(self, image_name):
        """
        Opens and returns the image by its name or path.

        Returns:
            tuple: (bool, PIL.Image.Image): True and image if successful, False otherwise.
        """
        try:
            image_path = os.path.normpath(os.path.abspath(image_name))

            if image_path not in self.annotation.image_name:
                return False, None

            try:
                image = Image.open(image_path)
                return True, image
            except Exception as e:
                logging.error(f"Error loading image: {e}")
                return False, None
        except Exception as e:
            logging.error(f"Error in fetch_image_by_name: {e}")
            return False, None

    def fetch_image_path(self, image_index):
        """
        Fetches the full image path by index.

        Returns:
            tuple: (bool, str): True and image path if successful, False otherwise.
        """
        try:
            if image_index < 0 or image_index >= len(self.annotation.image_name):
                return False, None

            image_name = self.annotation.image_name[image_index]
            image_path = os.path.join(self.annotation.root, image_name)

            if not os.path.exists(image_path):
                return False, None

            return True, image_path
        except Exception as e:
            logging.error(f"Error in fetch_image_path: {e}")
            return False, None

    def fetch_image(self, image_index):
        """
        Opens and returns the image by index.

        Returns:
            tuple: (bool, PIL.Image.Image): True and image if successful, False otherwise.
        """
        try:
            success, image_path = self.fetch_image_path(image_index)
            if not success:
                return False, None

            try:
                image = Image.open(image_path)
                return True, image
            except Exception as e:
                logging.error(f"Error loading image: {e}")
                return False, None
        except Exception as e:
            logging.error(f"Error in fetch_image: {e}")
            return False, None

    def add_image(self, image_name, labels=None):
        """
        Adds a new image and its corresponding labels to the dataset.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            print(f"Attempting to add image: {image_name}")

            # Check if the image exists
            if not os.path.exists(image_name):
                print("Image file does not exist.")
                return False

            image_path = os.path.normpath(os.path.abspath(image_name))

            # Check if the image already exists in the dataset
            if image_path in self.annotation.image_name:
                print(f"Image already exists in dataset: {image_path}")
                return False

            # Check the file extension for allowed formats
            _, file_extension = os.path.splitext(image_path)
            if file_extension.lower() not in self.allowed_formats:
                print(f"Invalid file format: {file_extension.lower()}")
                return False

            # Open the image and check its dimensions
            try:
                image = Image.open(image_path)
                print(f"Image size: {image.size}, Required size: ({self.image_width}, {self.image_height})")
                if image.size != (self.image_width, self.image_height):
                    image.close()
                    print(f"Image dimensions {image.size} do not match required size ({self.image_width}, {self.image_height}).")
                    return False
                image.close()
            except Exception as e:
                logging.error(f"Error loading image: {e}")
                return False

            # Assign default labels if none provided
            if labels is None:
                labels = [0] * len(self.annotation.attr_name)
                print(f"Default labels assigned: {labels}")
            if len(labels) != len(self.annotation.attr_name):
                print("Label count does not match attribute count.")
                return False

            # Add the image path and its labels to the dataset
            self.annotation.image_name.append(image_path)

            if len(self.annotation.image_name) == 1:
                self.annotation.label = np.array([labels], dtype=int)
            else:
                self.annotation.label = np.row_stack((self.annotation.label, np.array(labels, dtype=int)))

            # Add image to the training partition
            self.annotation.partition.train.append(len(self.annotation.image_name) - 1)
            self.annotation.partition.trainval.append(len(self.annotation.image_name) - 1)

            # Save the annotation after adding the image
            self.save_annotation()
            print(f"Image {image_name} added successfully with labels: {labels}")
            return True
        except Exception as e:
            logging.error(f"Error in add_image: {e}")
            return False

    def remove_image(self, index):
        """
        Removes an image and its labels by index.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if 0 <= index < len(self.annotation.image_name):
                self.annotation.image_name.pop(index)

                if self.annotation.label.shape[0] == 1:
                    self.annotation.label = np.array([], dtype=int)
                elif self.annotation.label.shape[0] > index:
                    self.annotation.label = np.delete(self.annotation.label, index, axis=0)

                if index in self.annotation.partition.train:
                    self.annotation.partition.train.remove(index)
                if index in self.annotation.partition.trainval:
                    self.annotation.partition.trainval.remove(index)

                self.annotation.partition.train = [i if i < index else i - 1 for i in self.annotation.partition.train]
                self.annotation.partition.trainval = [i if i < index else i - 1 for i in self.annotation.partition.trainval]

                self.save_annotation()
                return True
            else:
                return False
        except Exception as e:
            logging.error(f"Error in remove_image: {e}")
            return False

    def get_labels_for_image(self, image_index):
        """
        Retrieves the labels associated with a specific image by its index.

        Returns:
            tuple: (bool, list): True and labels if successful, False otherwise.
        """
        try:
            if image_index < 0 or image_index >= len(self.annotation.image_name):
                return False, None
            return True, self.annotation.label[image_index].tolist()
        except Exception as e:
            logging.error(f"Error in get_labels_for_image: {e}")
            return False, None

    def edit_label_for_image(self, image_index, new_label_value):
        """
        Edits an existing label for a specific image.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if image_index < 0 or image_index >= len(self.annotation.image_name):
                return False

            if len(new_label_value) != len(self.annotation.attr_name):
                return False

            self.annotation.label[image_index] = np.array(new_label_value, dtype=int)
            self.save_annotation()
            return True
        except Exception as e:
            logging.error(f"Error in edit_label_for_image: {e}")
            return False

    def remove_label_from_image(self, image_index):
        """
        Removes the label from a specific image.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if image_index < 0 or image_index >= len(self.annotation.image_name):
                return False

            self.annotation.label[image_index] = np.zeros(len(self.annotation.attr_name), dtype=int)
            self.save_annotation()
            return True
        except Exception as e:
            logging.error(f"Error in remove_label_from_image: {e}")
            return False