from PyQt5 import QtWidgets, QtCore
import os

class ModelSettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, title='Model Settings' ,model_name='', model_path=''):
        super(ModelSettingsDialog, self).__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(400, 200)
        
        self.model_name = model_name
        self.model_path = model_path

        # Layout
        layout = QtWidgets.QFormLayout(self)

        # Model Name Field
        self.nameLineEdit = QtWidgets.QLineEdit(self)
        self.nameLineEdit.setText(model_name)
        layout.addRow("Model Name:", self.nameLineEdit)

        # Model Path Field with Browse Button
        self.pathLineEdit = QtWidgets.QLineEdit(self)
        self.pathLineEdit.setText(model_path)
        self.browseButton = QtWidgets.QPushButton("Browse")
        self.browseButton.clicked.connect(self.browse_file)
        path_layout = QtWidgets.QHBoxLayout()
        path_layout.addWidget(self.pathLineEdit)
        path_layout.addWidget(self.browseButton)
        layout.addRow("Model Path:", path_layout)

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
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Python File", "", "Python Files (*.safetensors)")
        if file_name:
            # Get the project root directory
            project_dir = os.path.abspath(".")  # Use your project root directory here
            # Convert the absolute path to a relative path
            relative_path = os.path.relpath(file_name, start=project_dir)
            # Update the file path text box with the relative path
            self.pathLineEdit.setText(relative_path)

    def get_model_data(self):
        """Retrieve the name and path entered by the user."""
        return self.nameLineEdit.text(), self.pathLineEdit.text()
    
    def validate_input(self):
        """Ensure the model name and path are not empty, and the path exists."""
        model_name = self.nameLineEdit.text().strip()
        model_path = self.pathLineEdit.text().strip()
        if not model_name or not model_path or not os.path.exists(model_path):
            QtWidgets.QMessageBox.warning(self, "Error", "Please provide a valid model name and path.")
            return False
        return True