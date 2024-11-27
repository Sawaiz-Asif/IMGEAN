from PyQt5 import QtWidgets, QtCore
import os
import importlib.util
import yaml

class AnnotatorModelDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, model_data=None, is_editing=False):
        super(AnnotatorModelDialog, self).__init__(parent)
        
        self.setWindowTitle("Edit Model" if is_editing else "Add New Model")
        self.setFixedSize(600, 400)

        self.is_editing = is_editing

        # Initialize model data
        self.model_data = model_data or {}

        # Layout
        layout = QtWidgets.QFormLayout(self)

        # Model Name
        self.nameLineEdit = QtWidgets.QLineEdit(self)
        self.nameLineEdit.setText(self.model_data.get('Name', ''))
        layout.addRow("Model Name:", self.nameLineEdit)

        # Backbone Type
        self.backboneLineEdit = QtWidgets.QLineEdit(self)
        self.backboneLineEdit.setText(self.model_data.get('BACKBONE_TYPE', 'resnet50'))
        layout.addRow("Backbone Type:", self.backboneLineEdit)

        # Classifier Fields
        self.bnCheckbox = QtWidgets.QCheckBox(self)
        self.bnCheckbox.setChecked(self.model_data.get('CLASSIFIER', {}).get('BN', False))
        layout.addRow("Use Batch Norm (BN):", self.bnCheckbox)

        self.classifierNameLineEdit = QtWidgets.QLineEdit(self)
        self.classifierNameLineEdit.setText(self.model_data.get('CLASSIFIER', {}).get('NAME', 'linear'))
        layout.addRow("Classifier Name:", self.classifierNameLineEdit)

        self.poolingLineEdit = QtWidgets.QLineEdit(self)
        self.poolingLineEdit.setText(self.model_data.get('CLASSIFIER', {}).get('POOLING', 'avg'))
        layout.addRow("Pooling Method:", self.poolingLineEdit)

        self.scaleSpinBox = QtWidgets.QSpinBox(self)
        self.scaleSpinBox.setValue(self.model_data.get('CLASSIFIER', {}).get('SCALE', 1))
        layout.addRow("Scale:", self.scaleSpinBox)

        # Dataset Fields
        self.heightSpinBox = QtWidgets.QSpinBox(self)
        self.heightSpinBox.setValue(self.model_data.get('DATASET', {}).get('HEIGHT', 256))
        layout.addRow("Dataset Height:", self.heightSpinBox)

        self.widthSpinBox = QtWidgets.QSpinBox(self)
        self.widthSpinBox.setValue(self.model_data.get('DATASET', {}).get('WIDTH', 192))
        layout.addRow("Dataset Width:", self.widthSpinBox)

        # Model Path
        self.pathLineEdit = QtWidgets.QLineEdit(self)
        self.pathLineEdit.setText(self.model_data.get('PATH', ''))
        self.browseButton = QtWidgets.QPushButton("Browse")
        self.browseButton.clicked.connect(self.browse_file)
        path_layout = QtWidgets.QHBoxLayout()
        path_layout.addWidget(self.pathLineEdit)
        path_layout.addWidget(self.browseButton)
        layout.addRow("Model Path:", path_layout)

        # Color-assisted mode
        self.colorAssistCheckbox = QtWidgets.QCheckBox(self)
        self.colorAssistCheckbox.setChecked(self.model_data.get('ColorAssist', False))
        layout.addRow("Color-Assisted Mode:", self.colorAssistCheckbox)

        # Confidence thresholds
        self.confidenceLineEdit = QtWidgets.QLineEdit(self)
        self.confidenceLineEdit.setText(self.model_data.get('ConfidenceThresholds', ''))
        layout.addRow("Confidence Thresholds:", self.confidenceLineEdit)

        # Save and Cancel Buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.saveButton = QtWidgets.QPushButton("Save")
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        button_layout.addWidget(self.saveButton)
        button_layout.addWidget(self.cancelButton)
        layout.addRow("", button_layout)

        self.saveButton.clicked.connect(self.apply_changes)
        self.cancelButton.clicked.connect(self.reject)

    def browse_file(self):
        """Open a file dialog to select a Python file and save the relative path."""
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Model File", "", "Model Files (*.pth)")
        if file_name:
            # Get the project root directory
            project_dir = os.path.abspath(".")  # Use your project root directory here
            # Convert the absolute path to a relative path
            relative_path = os.path.relpath(file_name, start=project_dir)
            # Update the file path text box with the relative path
            self.pathLineEdit.setText(relative_path)

    def get_model_data(self):
        """Retrieve the entered data."""
        model_data = {
            'Name': self.nameLineEdit.text().strip(),
            'BACKBONE_TYPE': self.backboneLineEdit.text().strip(),
            'CLASSIFIER': {
                'BN': self.bnCheckbox.isChecked(),
                'NAME': self.classifierNameLineEdit.text().strip(),
                'POOLING': self.poolingLineEdit.text().strip(),
                'SCALE': self.scaleSpinBox.value(),
            },
            'DATASET': {
                'HEIGHT': self.heightSpinBox.value(),
                'WIDTH': self.widthSpinBox.value(),
            },
            'PATH': self.pathLineEdit.text().strip(),
            'ColorAssist': self.colorAssistCheckbox.isChecked(),
            'ConfidenceThresholds': self.confidenceLineEdit.text().strip()
        }
        return model_data

    def apply_changes(self):
        """Apply changes to the passed model data."""
        updated_data = self.get_model_data()
        self.model_data.update(updated_data)  # Update the passed model data
        self.accept()  # Close the dialog

