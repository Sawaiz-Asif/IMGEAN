from PyQt5 import QtWidgets
from frontend.settings_ui import Ui_SettingsWindow  # Import the UI class
# dialogs
from frontend.model_settings_dialog import ModelSettingsDialog
from frontend.quality_checker_dialog import QualityCheckerDialog
from frontend.annotator_model_dialog import AnnotatorModelDialog
from frontend.add_thresh_dialog import AddThresholdDialog

import ast

import os
import logging

# Import the save_config function from config_reader.py
from backend.config_reader import save_config
# Import the DatasetManager class
from backend.annotation_manager.dataset_utils import DatasetManager

from PyQt5.QtCore import pyqtSignal

from backend.annotation_manager.dataset_utils import DatasetManager


class SettingsWindow(QtWidgets.QMainWindow):
    dataset_updated = pyqtSignal()# Signal to notify updates

    def __init__(self, main_window, config, ui_styles):
        super(SettingsWindow, self).__init__()

        self.ui = Ui_SettingsWindow(config, ui_styles)  # Initialize the UI
        self.ui.setupUi(self)

        self.main_window = main_window
        self.config = config
        self.ui_styles = ui_styles

        # Initialize DatasetManager
        # self.dataset_manager = DatasetManager(
        #     pickle_file=self.config['DATASET']['PATH'],
        #     config=self.config,
        #     use_default_path=True
        # )
        self.dataset_manager = DatasetManager(config['DATASET']['PATH'], config)
        if not self.dataset_manager.initialized:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to initialize Dataset Manager.")
            return

        self.initialize_ui()  # Initialize UI elements with config data

        # Connect button clicks to methods
        self.ui.returnButton.clicked.connect(self.on_return)

        # Dataset section connections
        self.ui.pickleFilePathBrowseButton.clicked.connect(self.browse_pickle_file)
        self.ui.addLabelButton.clicked.connect(self.add_label)
        self.ui.editLabelButton.clicked.connect(self.edit_label)
        self.ui.removeLabelButton.clicked.connect(self.remove_label)
        self.ui.saveDatasetButton.clicked.connect(self.save_dataset_settings)

        # Image Generator section connections
        self.ui.addNewImageModelButton.clicked.connect(lambda: self.manage_image_model())
        self.ui.removeImageModelButton.clicked.connect(self.remove_image_model)
        self.ui.outputFolderBrowseButton.clicked.connect(self.browse_output_folder)
        self.ui.saveImageGenButton.clicked.connect(self.save_image_generator_settings)
        self.ui.imageModelSettingsButton.clicked.connect(self.edit_selected_image_model)

        # Quality Checker section connections
        self.ui.removeQualityFunctionButton.clicked.connect(self.remove_quality_function)
        self.ui.saveQualityCheckerButton.clicked.connect(self.save_quality_checker_settings)
        self.ui.addNewQualityFunctionButton.clicked.connect(lambda: self.manage_quality_function())
        self.ui.qualityFunctionSettingsButton.clicked.connect(self.edit_selected_quality_function)

        # Annotator section connections
        # self.addNewAnnotatorModelButton.clicked.connect(self.add_new_annotator_model)
        # self.removeAnnotatorModelButton.clicked.connect(self.remove_annotator_model)
        self.ui.saveAnnotatorButton.clicked.connect(self.save_annotator_settings)

        # Button connections
        self.ui.addConfidenceButton.clicked.connect(self.add_confidence_threshold)
        self.ui.editConfidenceButton.clicked.connect(self.edit_confidence_threshold)
        self.ui.removeConfidenceButton.clicked.connect(self.remove_confidence_threshold)
        # Connect buttons
        self.ui.addModelButton.clicked.connect(self.add_new_model)
        self.ui.editModelButton.clicked.connect(self.edit_selected_model)
        self.ui.removeModelButton.clicked.connect(self.remove_selected_model)

        

    def initialize_ui(self):
        # Initialize Dataset section
        dataset_config = self.config.get('DATASET', {})

        # Description (currently the name)
        self.ui.descriptionLineEdit.setText(dataset_config.get('NAME', ''))

        # Pickle file path
        pickle_file_path = dataset_config.get('PATH', '')
        self.ui.pickleFilePathLineEdit.setText(pickle_file_path)

        # Labels (use DatasetManager to get labels)
        success, labels = self.dataset_manager.get_dataset_labels()
        if success:
            self.labels = labels
            self.ui.labelsListWidget.addItems(self.labels)
        else:
            self.labels = []
            QtWidgets.QMessageBox.warning(self, "Warning", "Failed to load labels from dataset.")

        # Initialize Annotator section
        annotator_config = self.config.get('ANNOTATION', {})
        self.annotator_data = annotator_config.get('MODELS', []).copy()  # Work on a copy of the models
        self.ui.annotatorModelsList.clear()
        for model in self.annotator_data:
            self.ui.annotatorModelsList.addItem(model.get('Name', 'Unnamed Model'))

        self.ui.currentSelectionComboBox.clear()
        for model in self.annotator_data:
            self.ui.currentSelectionComboBox.addItem(model.get('Name', 'Unnamed Model'))

        # Set the current selection
        current_selected = self.config.get('ANNOTATION', {}).get('CURRENT_SELECTED', 0)
        if 0 <= current_selected < len(self.annotator_data):
            self.ui.currentSelectionComboBox.setCurrentIndex(current_selected)

        

        # Handle other Annotator fields
        self.ui.colorAssistCheckbox.setChecked(annotator_config.get('ColorAssist', False))
        auto_label_config = self.config.get('AUTO_LABEL', {})
        # Load MAX_AUTO_LABEL
        self.ui.maxAutoLabelSpinBox.setValue(auto_label_config.get('MAX_AUTO_LABEL', 12))

        # Load CHECKBOX_THRESHOLD
        self.ui.checkboxThresholdSpinBox.setValue(auto_label_config.get('CHECKBOX_THRESHOLD', 0.5))

        # Load DEFAULT_COLOR
        default_color = auto_label_config.get('DEFAULT_COLOR', 'blue')
        if default_color in [self.ui.defaultColorComboBox.itemText(i) for i in range(self.ui.defaultColorComboBox.count())]:
            self.ui.defaultColorComboBox.setCurrentText(default_color)
        else:
            self.ui.defaultColorComboBox.setCurrentIndex(0)  # Fallback to the first color

        # Load CONFIDENCE_THRESHOLDS
        self.temp_confidence_thresholds = auto_label_config.get('CONFIDENCE_THRESHOLDS', [])
        self.ui.confidenceThresholdList.clear()
        for threshold in self.temp_confidence_thresholds:
            self.ui.confidenceThresholdList.addItem(f"{threshold['color']}: {threshold['value']}")

        # Load Color-Assisted Mode (if applicable in the config)
        self.ui.colorAssistCheckbox.setChecked(auto_label_config.get('ENABLE_COLOR_ASSIST', False))


        # Initialize Image Generator section
        self.temp_image_config = self.config.get('GENERATION', {}).copy()
        models = self.temp_image_config.get('MODELS', [])
        self.ui.imageModelsList.clear()
        for model in models:
            self.ui.imageModelsList.addItem(model.get('name', 'Unknown Model'))

        self.ui.outputFolderLineEdit.setText(self.temp_image_config.get('BASE_OUTPUT_PATH', '../ComfyUI/output'))
        self.ui.comfyUiIpLineEdit.setText(self.temp_image_config.get('IP_COMFY', 'http://127.0.0.1:8188'))

        # Initialize Quality Checker section
        self.temp_quality_config = self.config.get('QUALITY_CHECKS', {}).copy()
        functions = self.temp_quality_config.get('FUNCTIONS', [])
        self.ui.qualityFunctionsList.clear()
        for function in functions:
            self.ui.qualityFunctionsList.addItem(function.get('name', 'Unknown Function'))
    

    def manage_image_model(self, model_index=None):
        """
        Opens the model settings dialog for creating or editing a model.
        If model_index is provided, it will be in edit mode.
        """
        # Determine if we are editing an existing model or creating a new one
        title=''
        if model_index is not None:
            model_data = self.temp_image_config['MODELS'][model_index]
            current_name = model_data.get('name', '')
            current_path = model_data.get('path', '')
            title = 'Edit Model'
        else:
            current_name = ''
            current_path = ''
            title = 'Add New Model'
        
        # Open the dialog
        dialog = ModelSettingsDialog(self,title=title, model_name=current_name, model_path=current_path)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_name, new_path = dialog.get_model_data()

            # Validate user input
            if not dialog.validate_input():
                return

            if model_index is None:  # Creating a new model
                model_entry = {'name': new_name, 'path': new_path}
                self.temp_image_config['MODELS'].append(model_entry)
                self.ui.imageModelsList.addItem(new_name)
            else:  # Editing an existing model
                self.temp_image_config['MODELS'][model_index]['name'] = new_name
                self.temp_image_config['MODELS'][model_index]['path'] = new_path
                self.ui.imageModelsList.item(model_index).setText(new_name)

            # Save the updated configuration
            QtWidgets.QMessageBox.information(self, "Success", "Model settings saved successfully.")
    def edit_selected_image_model(self):
        print("hi i am here")
        selected_items = self.ui.imageModelsList.selectedItems()
        if selected_items:
            index = self.ui.imageModelsList.row(selected_items[0])
            self.manage_image_model(model_index=index)

    # Dataset Section Methods
    def browse_pickle_file(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Pickle File", "", "Pickle Files (*.pkl);;All Files (*)", options=options)
        if file_name:
            project_dir = os.path.abspath(".")
            file_name = os.path.relpath(file_name, start=project_dir)
            self.ui.pickleFilePathLineEdit.setText(file_name)
            self.dataset_manager.pickle_file = file_name
            self.dataset_manager.load_annotation()
            self.load_labels()

    def load_labels(self):
        success, labels = self.dataset_manager.get_dataset_labels()
        if success:
            self.labels = labels
            self.ui.labelsListWidget.clear()
            self.ui.labelsListWidget.addItems(self.labels)
        else:
            self.labels = []
            QtWidgets.QMessageBox.warning(self, "Warning", "Failed to load labels from dataset.")

    def add_label(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Add Label', 'Enter new label:')
        if ok and text:
            success = self.dataset_manager.add_label(new_label=text)
            if success:
                self.labels.append(text)
                self.ui.labelsListWidget.addItem(text)
            else:
                QtWidgets.QMessageBox.warning(self, "Warning", "Failed to add label.")

    def edit_label(self):
        selected_items = self.ui.labelsListWidget.selectedItems()
        if selected_items:
            item = selected_items[0]
            index = self.ui.labelsListWidget.row(item)
            text, ok = QtWidgets.QInputDialog.getText(self, 'Edit Label', 'Modify label:', text=item.text())
            if ok and text:
                success = self.dataset_manager.edit_label(label_index=index, new_label=text)
                if success:
                    self.labels[index] = text
                    item.setText(text)
                else:
                    QtWidgets.QMessageBox.warning(self, "Warning", "Failed to edit label.")

    def remove_label(self):
        selected_items = self.ui.labelsListWidget.selectedItems()
        if selected_items:
            item = selected_items[0]
            index = self.ui.labelsListWidget.row(item)
            print(f"[INFO] Selected label to remove: '{item.text()}' at index {index}.")
            
            confirm = QtWidgets.QMessageBox.question(
                self, 'Confirm', f"Are you sure you want to remove label '{item.text()}'?"
            )
            
            if confirm == QtWidgets.QMessageBox.Yes:
                print(f"[INFO] User confirmed removal of label: '{item.text()}'.")
                success = self.dataset_manager.remove_label(label_index=index)
                
                if success:
                    print(f"[SUCCESS] Label '{item.text()}' removed successfully.")
                    self.ui.labelsListWidget.takeItem(index)
                    self.dataset_updated.emit()  # Emit the signal to notify updates
                    #del self.labels[index]
                else:
                    print(f"[ERROR] Failed to remove label: '{item.text()}'.")
                    QtWidgets.QMessageBox.warning(self, "Warning", "Failed to remove label.")
            else:
                print(f"[INFO] User canceled removal of label: '{item.text()}'.")
        else:
            print("[INFO] No label selected for removal.")

    def save_dataset_settings(self):
        # Update config
        self.config['DATASET']['NAME'] = self.ui.descriptionLineEdit.text()
        self.config['DATASET']['PATH'] = self.ui.pickleFilePathLineEdit.text()
        # Update dataset manager
        self.dataset_manager.pickle_file = self.config['DATASET']['PATH']
        self.dataset_manager.save_annotation()
        # Save config file
        self.save_config()

        QtWidgets.QMessageBox.information(self, "Success", "Dataset settings saved successfully.")

    # Quality Checker Section Methods
    def remove_quality_function(self):
        selected_items = self.ui.qualityFunctionsList.selectedItems()
        if selected_items:
            item = selected_items[0]
            index = self.ui.qualityFunctionsList.row(item)
            confirm = QtWidgets.QMessageBox.question(self, 'Confirm', f"Are you sure you want to remove function '{item.text()}'?")
            if confirm == QtWidgets.QMessageBox.Yes:
                self.ui.qualityFunctionsList.takeItem(index)
                del self.temp_quality_config['QUALITY_CHECKS']['FUNCTIONS'][index]

    def save_quality_checker_settings(self):
        self.config['QUALITY_CHECKS'] = self.temp_quality_config.copy()  # Save temp_config to main config
        self.save_config()  # Write to file
        QtWidgets.QMessageBox.information(self, "Success", "Quality checker settings saved successfully.")

    def parse_args(self,args_string):
        """
        Parse a comma-separated string into a list of values with inferred types.
        Example: "10,20" -> [10, 20]
        """
        if not args_string.strip():  # Handle empty input
            return []

        parsed_args = []
        for arg in args_string.split(','):
            arg = arg.strip()  # Remove whitespace
            try:
                # Convert to int or float if possible
                if '.' in arg:
                    parsed_args.append(float(arg))
                else:
                    parsed_args.append(int(arg))
            except ValueError:
                # Keep as string if conversion fails
                parsed_args.append(arg)
        return parsed_args

    def manage_quality_function(self, function_index=None):
        """
        Opens the quality function dialog for creating or editing a function.
        If function_index is provided, it will be in edit mode.
        """
        is_editing = function_index is not None

        if is_editing:
            # Pre-fill existing data for editing
            function_data = self.config['QUALITY_CHECKS']['FUNCTIONS'][function_index]
            current_name = function_data.get('name', '')
            current_path = function_data.get('path', '')
            current_path = os.path.relpath(current_path, start=os.path.abspath("."))  # Normalize to relative path
            args = function_data.get('args', [])
            if isinstance(args, (list, tuple)):
                current_args = ','.join(map(str, args))  # Display as a string
            else:
                current_args = ''  # Ensure current_args is always a string
        else:
            # Blank data for new function
            current_name = ''
            current_path = ''
            current_args = ''  # Ensure current_args is always a string

        # Open dialog for user input
        dialog = QualityCheckerDialog(
            self,
            function_name=current_name,
            file_path=current_path,
            args=current_args,
            is_editing=is_editing
        )

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            new_name, new_path, new_args = dialog.get_function_data()
            # Parse the new arguments
            new_args = self.parse_args(new_args) 

            # Validate inputs (file existence and function testing)
            if not dialog.validate_input():
                return
            try:
                result = ast.literal_eval(new_args)  # Converts to [10, 20]
                print(result)  # Output: [10, 20]
                print(type(result))  # Output: <class 'list'>
            except (ValueError, SyntaxError):
                print("Invalid input!")
            

            # Handle file movement for new or updated functions
            if not is_editing:
                try:
                    checking_dir = os.path.join(".", "data", "checking")
                    if not os.path.exists(checking_dir):
                        os.makedirs(checking_dir)

                    # Move the file to the directory
                    destination_path = os.path.join(checking_dir, os.path.basename(new_path))
                    if os.path.exists(destination_path):
                        QtWidgets.QMessageBox.warning(
                            self, "Error",
                            f"A file with the name '{os.path.basename(new_path)}' already exists in the checking directory."
                        )
                        return  # Stop further processing

                    os.replace(new_path, destination_path)
                    new_path = os.path.relpath(destination_path, start=os.path.abspath("."))
                except Exception as e:
                    QtWidgets.QMessageBox.critical(self, "Error", f"Failed to move the file: {e}")
                    return

            # Update or add the function entry in the config
            if is_editing:
                self.config['QUALITY_CHECKS']['FUNCTIONS'][function_index] = {
                    'name': new_name,
                    'path': new_path,
                    'args': new_args
                }
                self.ui.qualityFunctionsList.item(function_index).setText(new_name)
            else:
                function_entry = {'name': new_name, 'path': new_path, 'args': new_args}
                self.temp_quality_config['QUALITY_CHECKS']['FUNCTIONS'].append(function_entry)
                self.ui.qualityFunctionsList.addItem(new_name)

            QtWidgets.QMessageBox.information(self, "Success", "Quality function settings saved successfully.")

    def edit_selected_quality_function(self):
        selected_items = self.ui.qualityFunctionsList.selectedItems()
        if selected_items:
            index = self.ui.qualityFunctionsList.row(selected_items[0])
            self.manage_quality_function(function_index=index)


    # Image Generator Section Methods
    def browse_output_folder(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Output Folder", "")
        if directory:
            project_dir = os.path.abspath(".")
            relative_path = os.path.relpath(directory, start=project_dir)
            self.ui.outputFolderLineEdit.setText(relative_path)

    def add_new_image_model(self):
        name, ok = QtWidgets.QInputDialog.getText(self, 'Add New Model', 'Enter model name:')
        if ok and name:
            path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Model File', '', 'Model Files (*.safetensors *.ckpt)')
            if path and os.path.exists(path):
                model_entry = {'name': name, 'path': path}
                self.temp_image_config['GENERATION']['MODELS'].append(model_entry)
                self.ui.imageModelsList.addItem(name)
            else:
                QtWidgets.QMessageBox.warning(self, 'Error', 'Selected file does not exist.')

    def remove_image_model(self):
        selected_items = self.ui.imageModelsList.selectedItems()
        if selected_items:
            item = selected_items[0]
            index = self.ui.imageModelsList.row(item)
            confirm = QtWidgets.QMessageBox.question(self, 'Confirm', f"Are you sure you want to remove model '{item.text()}'?")
            if confirm == QtWidgets.QMessageBox.Yes:
                self.ui.imageModelsList.takeItem(index)
                del self.temp_image_config['GENERATION']['MODELS'][index]

    def save_image_generator_settings(self):
        self.temp_image_config['BASE_OUTPUT_PATH'] = self.ui.outputFolderLineEdit.text()
        self.temp_image_config['IP_COMFY'] = self.ui.comfyUiIpLineEdit.text()
        self.config['GENERATION'] = self.temp_image_config
        self.save_config()
        QtWidgets.QMessageBox.information(self, "Success", "Image generator settings saved successfully.")


    # Annotator Section Methods
    def add_confidence_threshold(self):
        """Add a new confidence threshold."""
        # Determine the current maximum threshold
        #existing_thresholds = [t['value'] for t in self.temp_confidence_thresholds]
        #min_value = max(existing_thresholds, default=0.0)
        min_value = 0.1
        max_value = 1.0

        # Open the AddThresholdDialog
        dialog = AddThresholdDialog(min_value=min_value, max_value=max_value, parent=self, color_mapping=self.ui.getPosibleColorsMapping())
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            color, value = dialog.get_data()
            self.temp_confidence_thresholds.append({'color': color, 'value': value})
            self.ui.confidenceThresholdList.addItem(f"{color}: {value}")

    def edit_confidence_threshold(self):
        """Edit the selected confidence threshold."""
        selected_items = self.ui.confidenceThresholdList.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select a threshold to edit.")
            return

        # Get selected threshold
        selected_item = selected_items[0]
        index = self.ui.confidenceThresholdList.row(selected_item)
        threshold = self.temp_confidence_thresholds[index]

        # Determine the valid range for editing
        #existing_thresholds = [t['value'] for i, t in enumerate(self.temp_confidence_thresholds) if i != index]
        min_value = 0.1
        max_value = 1.0

        # Open the dialog with the existing values
        dialog = AddThresholdDialog(
            min_value=min_value,
            max_value=max_value,
            color=threshold['color'],
            value=threshold['value'],
            parent=self,
            color_mapping=self.ui.getPosibleColorsMapping()
        )

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            color, value = dialog.get_data()
            self.temp_confidence_thresholds[index] = {'color': color, 'value': value}
            selected_item.setText(f"{color}: {value}")

    def remove_confidence_threshold(self):
        """Remove the selected confidence threshold."""
        selected_items = self.ui.confidenceThresholdList.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select a threshold to remove.")
            return

        for item in selected_items:
            index = self.ui.confidenceThresholdList.row(item)
            self.ui.confidenceThresholdList.takeItem(index)
            del self.temp_confidence_thresholds[index]
    
    def save_current_selection(self):
        current_index = self.ui.currentSelectionComboBox.currentIndex()
        self.config["ANNOTATION"]["CURRENT_SELECTED"] = current_index

    def add_new_model(self):
        """Open the dialog to add a new model."""
        new_model = {
            'Name': '',
            'BACKBONE_TYPE': 'resnet50',
            'CLASSIFIER': {'BN': False, 'NAME': 'linear', 'POOLING': 'avg', 'SCALE': 1},
            'DATASET': {'HEIGHT': 256, 'WIDTH': 192},
            'PATH': '',
            'ColorAssist': False,
            'ConfidenceThresholds': ''
        }
        dialog = AnnotatorModelDialog(self, model_data=new_model, is_editing=False)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.annotator_data.append(new_model)
            self.ui.annotatorModelsList.addItem(new_model["Name"])

    def remove_selected_model(self):
        """Remove the selected model."""
        selected_items = self.ui.annotatorModelsList.selectedItems()
        if selected_items:
            index = self.ui.annotatorModelsList.row(selected_items[0])
            confirm = QtWidgets.QMessageBox.question(self, "Confirm", f"Are you sure you want to remove model '{selected_items[0].text()}'?")
            if confirm == QtWidgets.QMessageBox.Yes:
                del self.annotator_data[index]
                self.ui.annotatorModelsList.takeItem(index)
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "No model selected for removal.")

    def save_annotator_settings(self):
        """Save the annotator data to the configuration file."""
        self.config['ANNOTATION']['MODELS'] = self.annotator_data
        self.config['ANNOTATION']['CURRENT_SELECTED'] = self.ui.annotatorModelsList.currentRow()
        self.save_current_selection()
        """Save all auto-label settings."""
        self.config['AUTO_LABEL'] = {
            'MAX_AUTO_LABEL': self.ui.maxAutoLabelSpinBox.value(),
            'CHECKBOX_THRESHOLD': self.ui.checkboxThresholdSpinBox.value(),
            'DEFAULT_COLOR': self.ui.defaultColorComboBox.currentText(),
            'CONFIDENCE_THRESHOLDS': self.temp_confidence_thresholds
        }
        self.save_config()
        QtWidgets.QMessageBox.information(self, "Success", "Annotator settings saved successfully.")

    def add_confidence_threshold(self):
        """Add a new confidence threshold with a custom dialog."""
        # Determine the current maximum threshold
        # existing_thresholds = [t['value'] for t in self.temp_confidence_thresholds]
        # min_value = max(existing_thresholds, default=0.0)  # Start from 0 if no thresholds exist
        min_value = 0.1
        max_value = 1.0  # Thresholds are limited to a maximum of 1

        # Open the AddThresholdDialog
        dialog = AddThresholdDialog(min_value=min_value, max_value=max_value, parent=self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            color, value = dialog.get_data()

            # Update the local thresholds list
            self.temp_confidence_thresholds.append({'color': color, 'value': value})

            # Update the UI list
            self.ui.confidenceThresholdList.addItem(f"{color}: {value}")

    def edit_selected_model(self):
        """Open the dialog to edit the selected model."""
        selected_items = self.ui.annotatorModelsList.selectedItems()
        if selected_items:
            index = self.ui.annotatorModelsList.row(selected_items[0])
            model_data = self.annotator_data[index]
            dialog = AnnotatorModelDialog(self, model_data=model_data, is_editing=True)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                # Update the UI with the new model name
                self.ui.annotatorModelsList.item(index).setText(model_data["Name"])
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "No model selected for editing.")

    # Config Saving Method
    def save_config(self):
        # Use the save_config function from config_reader.py
        save_config(self.config, './config.yaml')
    # General Methods
    def on_return(self):
        self.main_window.change_current_screen(0)
        print("Returning to the main menu")