import numpy as np
import os
import pickle
from easydict import EasyDict

class DatasetManager:
    def __init__(self, pickle_file, description=None, reorder=None, root=None):
        """
        Initializes the DatasetManager by attempting to load an annotation from a pickle file.
        If the file does not exist, it initializes a new dataset and saves it as a pickle.

        Args:
            pickle_file (str): The path to the pickle file where the dataset is stored.
            description (str, optional): A custom description for the dataset. Defaults to None.
            reorder (str, optional): A custom reorder value. Defaults to None.
            root (str, optional): A custom root path. Defaults to None.
        """
        self.pickle_file = pickle_file
        self.annotation = self.load_annotation(description, reorder, root)

    def load_annotation(self, description=None, reorder=None, root=None):
        """
        Loads the annotation from a pickle file if it exists, otherwise initializes a new dataset.

        Args:
            description (str, optional): The dataset description to set or replace. Defaults to None.
            reorder (str, optional): The reorder value to set or replace. Defaults to None.
            root (str, optional): The root path to set or replace. Defaults to None.

        Returns:
            EasyDict: The loaded or newly created annotation data.

        Raises:
            RuntimeError: If loading the annotation fails due to corruption or other errors.
        """
        try:
            if os.path.exists(self.pickle_file):
                with open(self.pickle_file, 'rb') as f:
                    print("Loading annotation from pickle file.")
                    annotation = pickle.load(f)

                # Update fields if they are provided
                modified = False
                if description is not None:
                    annotation['description'] = description
                    modified = True
                if reorder is not None:
                    annotation['reorder'] = reorder
                    modified = True
                if root is not None:
                    annotation['root'] = root
                    modified = True

                # Save updated annotation if changes were made
                if modified:
                    self.save_annotation(annotation)
            else:
                print("Pickle file not found. Initializing a new dataset.")
                annotation = EasyDict({
                    'description': description if description else 'New Dataset',
                    'reorder': reorder if reorder else '',
                    'root': root if root else '',
                    'image_name': [],
                    'label': np.zeros((0, 0), dtype=int),  # Ensuring labels are initialized as integers
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
                })
                self.annotation = annotation
                self.save_annotation(annotation)

            return annotation
        except (EOFError, pickle.UnpicklingError) as e:
            raise RuntimeError(f"Failed to load annotation from corrupted pickle file '{self.pickle_file}': {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error while loading annotation from '{self.pickle_file}': {e}")

    def save_annotation(self, annotation=None):
        """
        Saves the current annotation to the pickle file.

        Args:
            annotation (EasyDict): The annotation data to save. If None, saves the current annotation.

        Raises:
            RuntimeError: If saving the annotation fails.
        """
        try:
            with open(self.pickle_file, 'wb') as f:
                pickle.dump(annotation or self.annotation, f)
            print("Annotation successfully saved to pickle file.")
        except Exception as e:
            raise RuntimeError(f"Failed to save annotation: {e}")

    def get_all_labels(self):
        """
        Fetches all labels from the dataset.

        Returns:
            numpy.ndarray: An array of all labels for the images in the dataset.

        Raises:
            ValueError: If labels are not found in the dataset.
        """
        try:
            return self.annotation.label
        except AttributeError:
            raise ValueError("Labels not found in the dataset.")

    def add_label(self, new_label, default_value=0):
        """
        Adds a new label to the dataset and assigns it a default value for all images.

        Args:
            new_label (str): The new label to add.
            default_value (int): The default label value for all images (default is 0).

        Returns:
            int: The index of the newly added label.

        Raises:
            ValueError: If the label already exists in the dataset.
            RuntimeError: If the label could not be added due to other issues (e.g., saving errors).
        """
        try:
            if new_label in self.annotation.attr_name:
                raise ValueError(f"Label '{new_label}' already exists in the dataset.")

            # Add new attribute name and initialize labels
            self.annotation.attr_name.append(new_label)
            if len(self.annotation.image_name) == 0:
                self.annotation.label = np.zeros((0, len(self.annotation.attr_name)), dtype=int)
            else:
                new_default_column = np.full((self.annotation.label.shape[0], 1), default_value, dtype=int)
                self.annotation.label = np.column_stack((self.annotation.label, new_default_column))

            self.save_annotation()
            return len(self.annotation.attr_name) - 1
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise RuntimeError(f"Failed to add new label: {e}")

    def edit_label(self, label_index, new_label):
        """
        Modifies an existing label by index.

        Args:
            label_index (int): The index of the label to edit.
            new_label (str): The new label name.

        Raises:
            IndexError: If the label index is out of range.
            RuntimeError: If editing fails.
        """
        try:
            if 0 <= label_index < len(self.annotation.attr_name):
                self.annotation.attr_name[label_index] = new_label
                self.save_annotation()
            else:
                raise IndexError("Label index out of range.")
        except Exception as e:
            raise RuntimeError(f"Failed to edit label: {e}")

    def remove_label(self, label_index):
        """
        Removes a label from all images by index.

        Args:
            label_index (int): The index of the label to remove.

        Raises:
            IndexError: If the label index is out of range.
            ValueError: If there are issues removing the label (e.g., when label array is not valid).
        """
        # Check if the label index is within bounds
        if not (0 <= label_index < len(self.annotation.attr_name)):
            raise IndexError("Label index out of range.")

        # Attempt to remove the label
        self.annotation.attr_name.pop(label_index)

        if self.annotation.label.size > 0:
            # Ensure that the label array is valid for deletion
            if self.annotation.label.shape[1] <= label_index:
                raise ValueError("Label index is out of bounds for label array.")
            
            # Remove the corresponding column from the label array
            self.annotation.label = np.delete(self.annotation.label, label_index, axis=1)

        # Save the updated annotation
        self.save_annotation()

    def fetch_image(self, image_index, include_root_path=False):
        """
        Fetches a specific image path by index.

        Args:
            image_index (int): The index of the image to fetch.
            include_root_path (bool): If True, return the complete path. If False, return only the image name.

        Returns:
            str: The path or name of the image file.

        Raises:
            TypeError: If the index is not an integer.
            IndexError: If the index is out of range.
            FileNotFoundError: If the image file does not exist at the specified path.
        """
        if not isinstance(image_index, int):
            raise TypeError("Index must be an integer")
        
        if image_index < 0 or image_index >= len(self.annotation.image_name):
            raise IndexError("Image index out of range.")

        image_name = self.annotation.image_name[image_index]

        if include_root_path:
            full_image_path = os.path.join(self.annotation.root, image_name)
            if not os.path.exists(full_image_path):
                raise FileNotFoundError(f"Image not found at path: {full_image_path}")

            return full_image_path
        
        return image_name

    def fetch_all_images(self, include_root_path=False):
        """
        Fetches the paths or names of all images in the dataset.

        Args:
            include_root_path (bool): If True, return complete paths. If False, return only the image names.

        Returns:
            list: A list of all image file paths or names.
        """
        try:
            if include_root_path:
                return [os.path.join(self.annotation.root, img) for img in self.annotation.image_name]
            else:
                return self.annotation.image_name
        except Exception as e:
            raise RuntimeError(f"Failed to fetch all images: {e}")

    def add_image(self, image_name, labels=None):
        """
        Adds a new image and its corresponding labels to the dataset.

        Args:
            image_name (str): The name of the image file to add.
            labels (list, optional): The list of labels corresponding to the new image. If None, a list of zeros will be created.

        Raises:
            ValueError: If the length of the labels list does not match the number of attributes,
                        or if the attribute names are not set.
            Exception: If saving errors occur.
        """

        # Initialize labels with zeros if no labels are provided
        if labels is None:
            labels = [0] * len(self.annotation.attr_name)  # Create a list of zeros

        # Check if the number of labels matches the number of attributes
        if len(labels) != len(self.annotation.attr_name):
            raise ValueError("Label list length does not match the number of attributes.")

        # Add the image name
        self.annotation.image_name.append(image_name)

        # Append the labels to the label array directly, assuming the label array is aligned with images
        if len(self.annotation.image_name) == 1:
            # If this is the first image, initialize the label array
            self.annotation.label = np.array([labels], dtype=int)
        else:
            # For additional images, append the labels
            self.annotation.label = np.row_stack((self.annotation.label, np.array(labels, dtype=int)))

        # Attempt to save the updated annotation
        try:
            self.save_annotation()
        except Exception as save_error:
            raise Exception(f"Failed to save the updated annotation: {save_error}")

    def remove_image(self, index):
        """
        Removes an image and its labels by index.

        Args:
            index (int): The index of the image to remove.

        Raises:
            IndexError: If the image index is out of range.
            RuntimeError: If the image could not be removed due to other issues (e.g., saving errors).
        """
        try:
            if 0 <= index < len(self.annotation.image_name):
                self.annotation.image_name.pop(index)

                if self.annotation.label.shape[0] == 1:
                    self.annotation.label = np.array([], dtype=int)
                    print("Resetting label array to empty since last image was removed.")
                elif self.annotation.label.shape[0] > index:
                    self.annotation.label = np.delete(self.annotation.label, index, axis=0)

                self.save_annotation()
            else:
                raise IndexError("Image index out of range.")
        except Exception as e:
            raise RuntimeError(f"Failed to remove image: {e}")

    def get_labels_for_image(self, image_index):
        """
        Retrieves the labels associated with a specific image by its index.

        Args:
            image_index (int): The index of the image for which to retrieve labels.

        Returns:
            list: A list of labels associated with the specified image.

        Raises:
            IndexError: If the image index is out of range.
        """
        if image_index < 0 or image_index >= len(self.annotation.image_name):
            raise IndexError("Image index out of range.")
        
        return self.annotation.label[image_index].tolist()

    def remove_label_from_image(self, image_index):
        """
        Removes the label from a specific image.

        Args:
            image_index (int): The index of the image from which the label will be removed.

        Raises:
            IndexError: If the image index is out of range.
        """
        if image_index < 0 or image_index >= len(self.annotation.image_name):
            raise IndexError("Image index out of range.")

        # Reset the label for the specified image
        self.annotation.label[image_index] = np.zeros(len(self.annotation.attr_name), dtype=int)  # Assuming default is zero
        self.save_annotation()

    def edit_label_for_image(self, image_index, new_label_value):
        """
        Edits an existing label for a specific image.

        Args:
            image_index (int): The index of the image for which to edit the label.
            new_label_value: The new label value. Must match the size of the existing labels.

        Raises:
            IndexError: If the image index is out of range.
            ValueError: If the size of the new label does not match the number of attributes.
        """
        if image_index < 0 or image_index >= len(self.annotation.image_name):
            raise IndexError("Image index out of range.")
        
        # Check if the new label's size matches the number of attributes
        if len(new_label_value) != len(self.annotation.attr_name):
            raise ValueError("New label size must match the number of attributes.")

        # Update the label
        self.annotation.label[image_index] = np.array(new_label_value, dtype=int)
        self.save_annotation()

# Example usage:
# dataset_manager = DatasetManager("dataset_annotation.pkl")