from PyQt5 import QtWidgets, QtCore
import os
import importlib.util
from PIL import Image
import numpy as np

class QualityCheckerDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, function_name='', file_path='', args='', is_editing=False):
        super(QualityCheckerDialog, self).__init__(parent)
        
        # Set dynamic title based on whether it's editing or adding
        operation = "Edit" if is_editing else "Add New"
        self.setWindowTitle(f"{operation} Quality Function")
        self.setFixedSize(500, 300)

        self.function_name = function_name
        self.file_path = file_path
        self.args = args

        # Layout
        layout = QtWidgets.QFormLayout(self)

        # Function Name
        self.nameLineEdit = QtWidgets.QLineEdit(self)
        self.nameLineEdit.setText(function_name)
        layout.addRow("Function Name:", self.nameLineEdit)

        # Function File Path with Browse Button
        self.pathLineEdit = QtWidgets.QLineEdit(self)
        self.pathLineEdit.setText(file_path)
        self.browseButton = QtWidgets.QPushButton("Browse")
        self.browseButton.clicked.connect(self.browse_file)
        path_layout = QtWidgets.QHBoxLayout()
        path_layout.addWidget(self.pathLineEdit)
        path_layout.addWidget(self.browseButton)
        layout.addRow("Function File Path:", path_layout)

        # Arguments Input
        self.argsLineEdit = QtWidgets.QLineEdit(self)
        self.argsLineEdit.setText(args)
        layout.addRow("Arguments (comma-separated):", self.argsLineEdit)

        # Save and Cancel Buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.saveButton = QtWidgets.QPushButton("Save")
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        button_layout.addWidget(self.saveButton)
        button_layout.addWidget(self.cancelButton)
        layout.addRow("", button_layout)

        # Connect buttons
        self.saveButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def browse_file(self):
        """Open a file dialog to select a Python file and save the relative path."""
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Python File", "", "Python Files (*.py)")
        if file_name:
            # Get the project root directory
            project_dir = os.path.abspath(".")  # Use your project root directory here
            # Convert the absolute path to a relative path
            relative_path = os.path.relpath(file_name, start=project_dir)
            # Update the file path text box with the relative path
            self.pathLineEdit.setText(relative_path)

    def get_function_data(self):
        """Retrieve the function name, path, and arguments entered by the user."""
        function_name = self.nameLineEdit.text().strip()
        file_path = self.pathLineEdit.text().strip()
        args = self.argsLineEdit.text().strip()
        return function_name, file_path, args

    def validate_input(self):
        """Validate the file path and test the function with the derived name."""
        file_path = self.pathLineEdit.text().strip()
        user_defined_name = self.nameLineEdit.text().strip()

        if not file_path:
            QtWidgets.QMessageBox.warning(self, "Error", "File path cannot be empty.")
            return False

        if not os.path.exists(file_path):
            QtWidgets.QMessageBox.warning(self, "Error", "File path does not exist.")
            return False

        # Test the function with a sample image using the derived function name
        if not self.test_function(file_path):
            QtWidgets.QMessageBox.warning(self, "Error", "The function test failed. Please check your function.")
            return False

        return True

    def test_function(self, file_path):
        """Test the function using a sample image (as a NumPy array) and derived function name."""
        try:
            # Load the sample image and convert it to a NumPy array
            sample_image_path = os.path.join("resources", "sample.jpg")
            if not os.path.exists(sample_image_path):
                raise FileNotFoundError("Sample image not found.")

            # Open the image using PIL and convert to NumPy array
            pil_image = Image.open(sample_image_path)
            numpy_image = np.array(pil_image)

            # Derive the function name from the file path
            derived_function_name = os.path.splitext(os.path.basename(file_path))[0]

            # Dynamically load the Python file as a module
            spec = importlib.util.spec_from_file_location("module.name", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Check if the derived function exists in the module
            if not hasattr(module, derived_function_name):
                raise AttributeError(f"Function '{derived_function_name}' not found in the file.")

            quality_function = getattr(module, derived_function_name)
            # Handle `None` or empty arguments
            args = self.argsLineEdit.text().strip()
            if args:  # If arguments exist, split and convert to a tuple
                args_tuple = tuple(args.split(','))
            else:  # If no arguments provided, set to None
                args_tuple = None

            # Get the arguments as a tuple
            args = self.argsLineEdit.text().strip()
            args_tuple = tuple(args.split(',')) if args else None
            result=0
            # Call the function with the NumPy image and arguments
            if args_tuple:
                result = quality_function(numpy_image, args_tuple)
            else:
                result = quality_function(numpy_image)

            # Ensure the function returns a boolean
            if result not in [True, False]:
                raise ValueError("Function did not return a boolean value.")

            return True
        except Exception as e:
            print(f"Function test failed: {e}")
            return False