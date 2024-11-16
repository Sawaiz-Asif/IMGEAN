from PyQt5 import QtWidgets
from frontend.settings_ui import Ui_SettingsWindow  # Import the UI class
import os
import logging

# Import the save_config function from config_reader.py
from backend.config_reader import save_config
# Import the DatasetManager class
from backend.annotation_manager.dataset_utils import DatasetManager



class SettingsWindow(QtWidgets.QMainWindow, Ui_SettingsWindow):
    def __init__(self, stacked_widget, config):
        super(SettingsWindow, self).__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget
        self.config = config

        # Initialize DatasetManager
        self.dataset_manager = DatasetManager(
            pickle_file=self.config['DATASET']['PATH'],
            config=self.config,
            use_default_path=True
        )

        if not self.dataset_manager.initialized:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to initialize Dataset Manager.")
            return

        self.initialize_ui()  # Initialize UI elements with config data

        # Connect button clicks to methods
        self.returnButton.clicked.connect(self.on_return)

        # Dataset section connections
        self.pickleFilePathBrowseButton.clicked.connect(self.browse_pickle_file)
        self.addLabelButton.clicked.connect(self.add_label)
        self.editLabelButton.clicked.connect(self.edit_label)
        self.removeLabelButton.clicked.connect(self.remove_label)
        self.saveDatasetButton.clicked.connect(self.save_dataset_settings)

        # Annotator section connections
        self.addNewAnnotatorModelButton.clicked.connect(self.add_new_annotator_model)
        self.removeAnnotatorModelButton.clicked.connect(self.remove_annotator_model)
        self.saveAnnotatorButton.clicked.connect(self.save_annotator_settings)

        # Image Generator section connections
        self.addNewImageModelButton.clicked.connect(self.add_new_image_model)
        self.removeImageModelButton.clicked.connect(self.remove_image_model)
        self.outputFolderBrowseButton.clicked.connect(self.browse_output_folder)
        self.saveImageGenButton.clicked.connect(self.save_image_generator_settings)

        # Quality Checker section connections
        self.addNewQualityFunctionButton.clicked.connect(self.add_new_quality_function)
        self.removeQualityFunctionButton.clicked.connect(self.remove_quality_function)
        self.saveQualityCheckerButton.clicked.connect(self.save_quality_checker_settings)

    def initialize_ui(self):
        # Initialize Dataset section
        dataset_config = self.config.get('DATASET', {})

        # Description (currently the name)
        self.descriptionLineEdit.setText(dataset_config.get('NAME', ''))

        # Pickle file path
        pickle_file_path = dataset_config.get('PATH', '')
        self.pickleFilePathLineEdit.setText(pickle_file_path)

        # Labels (use DatasetManager to get labels)
        success, labels = self.dataset_manager.get_dataset_labels()
        if success:
            self.labels = labels
            self.labelsListWidget.addItems(self.labels)
        else:
            self.labels = []
            QtWidgets.QMessageBox.warning(self, "Warning", "Failed to load labels from dataset.")

        # Initialize Annotator section
        annotator_config = self.config.get('ANNOTATOR', {})
        models = annotator_config.get('MODELS', [])
        self.annotatorModelsList.clear()
        for model in models:
            self.annotatorModelsList.addItem(model.get('Name', 'Unknown Model'))

        self.colorAssistCheckbox.setChecked(annotator_config.get('ColorAssist', False))
        self.confidenceThresholdsLineEdit.setText(str(annotator_config.get('ConfidenceThresholds', '')))

        # Initialize Image Generator section
        generation_config = self.config.get('GENERATION', {})
        models = generation_config.get('MODELS', [])
        self.imageModelsList.clear()
        for model in models:
            self.imageModelsList.addItem(model.get('name', 'Unknown Model'))

        self.outputFolderLineEdit.setText(generation_config.get('BASE_OUTPUT_PATH', '../ComfyUI/output'))
        self.comfyUiIpLineEdit.setText(generation_config.get('IP_COMFY', 'http://127.0.0.1:8188'))

        # Initialize Quality Checker section
        quality_config = self.config.get('QUALITY_CHECKS', {})
        functions = quality_config.get('FUNCTIONS', [])
        self.qualityFunctionsList.clear()
        for function in functions:
            self.qualityFunctionsList.addItem(function.get('name', 'Unknown Function'))

    # Dataset Section Methods
    def browse_pickle_file(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Pickle File", "", "Pickle Files (*.pkl);;All Files (*)", options=options)
        if file_name:
            self.pickleFilePathLineEdit.setText(file_name)
            self.dataset_manager.pickle_file = file_name
            self.dataset_manager.load_annotation()
            self.load_labels()

    def load_labels(self):
        success, labels = self.dataset_manager.get_dataset_labels()
        if success:
            self.labels = labels
            self.labelsListWidget.clear()
            self.labelsListWidget.addItems(self.labels)
        else:
            self.labels = []
            QtWidgets.QMessageBox.warning(self, "Warning", "Failed to load labels from dataset.")

    def add_label(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Add Label', 'Enter new label:')
        if ok and text:
            success = self.dataset_manager.add_label(new_label=text)
            if success:
                self.labels.append(text)
                self.labelsListWidget.addItem(text)
            else:
                QtWidgets.QMessageBox.warning(self, "Warning", "Failed to add label.")

    def edit_label(self):
        selected_items = self.labelsListWidget.selectedItems()
        if selected_items:
            item = selected_items[0]
            index = self.labelsListWidget.row(item)
            text, ok = QtWidgets.QInputDialog.getText(self, 'Edit Label', 'Modify label:', text=item.text())
            if ok and text:
                success = self.dataset_manager.edit_label(label_index=index, new_label=text)
                if success:
                    self.labels[index] = text
                    item.setText(text)
                else:
                    QtWidgets.QMessageBox.warning(self, "Warning", "Failed to edit label.")

    def remove_label(self):
        selected_items = self.labelsListWidget.selectedItems()
        if selected_items:
            item = selected_items[0]
            index = self.labelsListWidget.row(item)
            confirm = QtWidgets.QMessageBox.question(self, 'Confirm', f"Are you sure you want to remove label '{item.text()}'?")
            if confirm == QtWidgets.QMessageBox.Yes:
                success = self.dataset_manager.remove_label(label_index=index)
                if success:
                    self.labelsListWidget.takeItem(index)
                    del self.labels[index]
                else:
                    QtWidgets.QMessageBox.warning(self, "Warning", "Failed to remove label.")

    def save_dataset_settings(self):
        # Update config
        self.config['DATASET']['NAME'] = self.descriptionLineEdit.text()
        self.config['DATASET']['PATH'] = self.pickleFilePathLineEdit.text()

        # Save config file
        self.save_config()

        # Update dataset manager
        self.dataset_manager.pickle_file = self.config['DATASET']['PATH']
        self.dataset_manager.save_annotation()

        QtWidgets.QMessageBox.information(self, "Success", "Dataset settings saved successfully.")

    # Annotator Section Methods
    def add_new_annotator_model(self):
        name, ok = QtWidgets.QInputDialog.getText(self, 'Add New Model', 'Enter model name:')
        if ok and name:
            # Collect other required fields
            backbone_type, ok = QtWidgets.QInputDialog.getText(self, 'Backbone Type', 'Enter backbone type (e.g., resnet50):')
            if not ok:
                return
            classifier_bn, ok = QtWidgets.QInputDialog.getItem(self, 'Classifier BN', 'Batch Norm (true/false):', ['true', 'false'], 0, False)
            if not ok:
                return
            classifier_name, ok = QtWidgets.QInputDialog.getText(self, 'Classifier Name', 'Enter classifier name:')
            if not ok:
                return
            classifier_pooling, ok = QtWidgets.QInputDialog.getText(self, 'Classifier Pooling', 'Enter pooling method (e.g., avg):')
            if not ok:
                return
            classifier_scale, ok = QtWidgets.QInputDialog.getInt(self, 'Classifier Scale', 'Enter scale value:', value=1)
            if not ok:
                return
            dataset_height, ok = QtWidgets.QInputDialog.getInt(self, 'Dataset Height', 'Enter height:', value=256)
            if not ok:
                return
            dataset_width, ok = QtWidgets.QInputDialog.getInt(self, 'Dataset Width', 'Enter width:', value=192)
            if not ok:
                return
            path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Model File', '', 'Model Files (*.pth *.pt)')
            if not path or not os.path.exists(path):
                QtWidgets.QMessageBox.warning(self, 'Error', 'Model file does not exist.')
                return

            # Build model entry
            model_entry = {
                'Name': name,
                'BACKBONE_TYPE': backbone_type,
                'CLASSIFIER': {
                    'BN': classifier_bn.lower() == 'true',
                    'NAME': classifier_name,
                    'POOLING': classifier_pooling,
                    'SCALE': classifier_scale
                },
                'DATASET': {
                    'HEIGHT': dataset_height,
                    'WIDTH': dataset_width
                },
                'PATH': path
            }

            # Verify model mapping exists
            if not self.verify_model_mapping(name):
                QtWidgets.QMessageBox.warning(self, 'Error', f"No model mapping found for '{name}'.")
                return

            # Add to config and UI
            self.config.setdefault('ANNOTATOR', {}).setdefault('MODELS', []).append(model_entry)
            self.annotatorModelsList.addItem(name)

        # Save the updated config
        self.save_config()

    def remove_annotator_model(self):
        selected_items = self.annotatorModelsList.selectedItems()
        if selected_items:
            item = selected_items[0]
            index = self.annotatorModelsList.row(item)
            confirm = QtWidgets.QMessageBox.question(self, 'Confirm', f"Are you sure you want to remove model '{item.text()}'?")
            if confirm == QtWidgets.QMessageBox.Yes:
                self.annotatorModelsList.takeItem(index)
                del self.config['ANNOTATOR']['MODELS'][index]
                # Save the updated config
                self.save_config()

    def save_annotator_settings(self):
        self.config.setdefault('ANNOTATOR', {})
        self.config['ANNOTATOR']['ColorAssist'] = self.colorAssistCheckbox.isChecked()
        self.config['ANNOTATOR']['ConfidenceThresholds'] = self.confidenceThresholdsLineEdit.text()
        self.save_config()
        QtWidgets.QMessageBox.information(self, "Success", "Annotator settings saved successfully.")

    def verify_model_mapping(self, model_name):
        # Implement logic to verify that the model mapping exists
        # For example, check if model_name exists in model_mapping
        # Here, we'll simulate the model_mapping as an example
        model_mapping = {
            "Model1": ("func1", "func2", "func3"),
            "Model2": ("funcA", "funcB", "funcC")
            # Add actual model mappings here
        }
        return model_name in model_mapping

    # Image Generator Section Methods
    def browse_output_folder(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Output Folder", "")
        if directory:
            self.outputFolderLineEdit.setText(directory)

    def add_new_image_model(self):
        name, ok = QtWidgets.QInputDialog.getText(self, 'Add New Model', 'Enter model name:')
        if ok and name:
            path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Model File', '', 'Model Files (*.safetensors *.ckpt)')
            if path and os.path.exists(path):
                model_entry = {'name': name, 'path': path}
                self.config['GENERATION']['MODELS'].append(model_entry)
                self.imageModelsList.addItem(name)
                # Save the updated config
                self.save_config()
            else:
                QtWidgets.QMessageBox.warning(self, 'Error', 'Selected file does not exist.')

    def remove_image_model(self):
        selected_items = self.imageModelsList.selectedItems()
        if selected_items:
            item = selected_items[0]
            index = self.imageModelsList.row(item)
            confirm = QtWidgets.QMessageBox.question(self, 'Confirm', f"Are you sure you want to remove model '{item.text()}'?")
            if confirm == QtWidgets.QMessageBox.Yes:
                self.imageModelsList.takeItem(index)
                del self.config['GENERATION']['MODELS'][index]
                # Save the updated config
                self.save_config()

    def save_image_generator_settings(self):
        self.config['GENERATION']['BASE_OUTPUT_PATH'] = self.outputFolderLineEdit.text()
        self.config['GENERATION']['IP_COMFY'] = self.comfyUiIpLineEdit.text()
        self.save_config()
        QtWidgets.QMessageBox.information(self, "Success", "Image generator settings saved successfully.")

    # Quality Checker Section Methods
    def add_new_quality_function(self):
        name, ok = QtWidgets.QInputDialog.getText(self, 'Add New Function', 'Enter function name:')
        if ok and name:
            file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Function File', '', 'Python Files (*.py)')
            if file_path and os.path.exists(file_path):
                args_text, ok = QtWidgets.QInputDialog.getText(self, 'Function Arguments', 'Enter arguments (comma-separated):')
                args = tuple(args_text.split(',')) if ok and args_text else None
                function_entry = {'name': name, 'path': file_path, 'args': args}
                self.config['QUALITY_CHECKS']['FUNCTIONS'].append(function_entry)
                self.qualityFunctionsList.addItem(name)
                # Save the updated config
                self.save_config()
            else:
                QtWidgets.QMessageBox.warning(self, 'Error', 'Selected file does not exist.')

    def remove_quality_function(self):
        selected_items = self.qualityFunctionsList.selectedItems()
        if selected_items:
            item = selected_items[0]
            index = self.qualityFunctionsList.row(item)
            confirm = QtWidgets.QMessageBox.question(self, 'Confirm', f"Are you sure you want to remove function '{item.text()}'?")
            if confirm == QtWidgets.QMessageBox.Yes:
                self.qualityFunctionsList.takeItem(index)
                del self.config['QUALITY_CHECKS']['FUNCTIONS'][index]
                # Save the updated config
                self.save_config()

    def save_quality_checker_settings(self):
        self.save_config()
        QtWidgets.QMessageBox.information(self, "Success", "Quality checker settings saved successfully.")

    # Config Saving Method
    def save_config(self):
        # Use the save_config function from config_reader.py
        save_config(self.config, './config.yaml')

    # General Methods
    def on_return(self):
        self.stacked_widget.setCurrentIndex(0)
        print("Returning to the main menu")