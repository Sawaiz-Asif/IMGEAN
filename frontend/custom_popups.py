from PyQt5.QtWidgets import QWidget, QSpinBox, QPushButton, QGridLayout, QHBoxLayout, QLabel, QDoubleSpinBox, QComboBox, QInputDialog, QInputDialog, QDialogButtonBox, QMessageBox
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QFontDatabase, QIcon

from ui_styles_constants import *

from PyQt5 import QtWidgets, QtGui
import os

from frontend.custom_ui_widgets import CustomCheckBox, CustomComboBox, CustomDoubleSpinBox, CustomSpinBox

class CustomQInputDialog(QInputDialog):
    def __init__(self, ui_styles=None):
        super().__init__()
        self.ui_styles = ui_styles
        regular_font_id = QFontDatabase.addApplicationFont(ui_styles[FONTS][REGULAR_FONT_FILE])
        self.regular_font_family = QFontDatabase.applicationFontFamilies(regular_font_id)[0]

    def showEvent(self, event):
        super().showEvent(event)
        
        button_box = self.findChild(QDialogButtonBox)
        
        if button_box:
            ok_button = button_box.button(QDialogButtonBox.Ok)
            cancel_button = button_box.button(QDialogButtonBox.Cancel)
            
            ok_button.setIcon(QIcon())
            cancel_button.setIcon(QIcon())

            ok_button.setObjectName("okButton")
            cancel_button.setObjectName("cancelButton")
            
            ok_button.setText("OK")
            cancel_button.setText("Cancel")

            ok_button.setFixedSize(self.ui_styles[SIZES][POPUP_BUTTONS][WIDTH], self.ui_styles[SIZES][POPUP_BUTTONS][HEIGHT])             
            cancel_button.setFixedSize(self.ui_styles[SIZES][POPUP_BUTTONS][WIDTH], self.ui_styles[SIZES][POPUP_BUTTONS][HEIGHT])

            self.setStyleSheet(f"""
                QInputDialog{{
                    background-color: {self.ui_styles[COLORS][BACKGROUND]};             
                }}
                QLabel {{
                    font-family: '{self.regular_font_family}';
                    font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
                }}
                QLineEdit{{
                    font-family: '{self.regular_font_family}';
                    font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px; 
                    background-color: {self.ui_styles[COLORS][BACKGROUND]};
                    border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                    border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                }}
                QPushButton#okButton {{
                    padding: px {self.ui_styles[PADDINGS][SETTINGS_BUTTONS_HORIZONTAL]}px px {self.ui_styles[PADDINGS][SETTINGS_BUTTONS_HORIZONTAL]}px;
                    border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                    font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
                    border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                    background-color: {self.ui_styles[COLORS][GREEN]}; 
                    color: {self.ui_styles[COLORS][BLACK]}
                }}
                    QPushButton#okButton:pressed {{
                    background-color: {self.ui_styles[COLORS][GREEN_PRESSED]};
                }}
                
                QPushButton#cancelButton {{
                    padding: px {self.ui_styles[PADDINGS][SETTINGS_BUTTONS_HORIZONTAL]}px px {self.ui_styles[PADDINGS][SETTINGS_BUTTONS_HORIZONTAL]}px;
                    border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                    font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
                    border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                    background-color: {self.ui_styles[COLORS][RED]}; 
                    color: {self.ui_styles[COLORS][BLACK]}
                }}
                    QPushButton#cancelButton:pressed {{
                    background-color: {self.ui_styles[COLORS][RED_PRESSED]};
                }}
            """)

    def getText(self, title, label, text=""):
        self.setWindowTitle(title)
        self.setLabelText(label)
        self.setTextValue(text)
        ok = self.exec_() == QInputDialog.Accepted
        return self.textValue(), ok
    
class CustomQMessageBox(QMessageBox):
    def __init__(self, ui_styles=None):
        super().__init__()
        self.ui_styles = ui_styles
        regular_font_id = QFontDatabase.addApplicationFont(ui_styles[FONTS][REGULAR_FONT_FILE])
        self.regular_font_family = QFontDatabase.applicationFontFamilies(regular_font_id)[0]

    def question(self, parent, title, text, buttons=QMessageBox.Yes | QMessageBox.No):
        # Create a QMessageBox instance
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.NoIcon)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(buttons)

        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {self.ui_styles[COLORS][BACKGROUND]};
            }}
            QLabel {{
                font-family: {self.regular_font_family};
                font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
            }}
            QMessageBox QDialogButtonBox {{
                alignment: center;
            }}
        """)

        # Customize button styles if needed
        yes_button = msg.button(QMessageBox.Yes)
        no_button = msg.button(QMessageBox.No)

        yes_button.setIcon(QIcon())
        no_button.setIcon(QIcon())

        yes_button.setText("Yes")
        no_button.setText("No")

        # Set the button sizes
        yes_button.setFixedSize(self.ui_styles[SIZES][POPUP_BUTTONS][WIDTH], self.ui_styles[SIZES][POPUP_BUTTONS][HEIGHT])             
        no_button.setFixedSize(self.ui_styles[SIZES][POPUP_BUTTONS][WIDTH], self.ui_styles[SIZES][POPUP_BUTTONS][HEIGHT])

        if yes_button:
            yes_button.setStyleSheet(f"""
                QPushButton {{
                    padding: px {self.ui_styles[PADDINGS][SETTINGS_BUTTONS_HORIZONTAL]}px px {self.ui_styles[PADDINGS][SETTINGS_BUTTONS_HORIZONTAL]}px;
                    border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                    font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
                    border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                    background-color: {self.ui_styles[COLORS][GREEN]};
                    color: {self.ui_styles[COLORS][BLACK]};
                }}
                QPushButton:pressed {{
                    background-color: {self.ui_styles[COLORS][GREEN_PRESSED]};
                }}
            """)
        if no_button:
            no_button.setStyleSheet(f"""
                QPushButton {{
                    padding: px {self.ui_styles[PADDINGS][SETTINGS_BUTTONS_HORIZONTAL]}px px {self.ui_styles[PADDINGS][SETTINGS_BUTTONS_HORIZONTAL]}px;
                    border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                    font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
                    border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                    background-color: {self.ui_styles[COLORS][RED]};
                    color: {self.ui_styles[COLORS][BLACK]};
                }}
                QPushButton:pressed {{
                    background-color: {self.ui_styles[COLORS][RED_PRESSED]};
                }}
            """)

        # Show the message box and return the user's response
        return msg.exec_()

    def warning(self, parent, title, text, ok_text="OK"):
        # Create a QMessageBox instance
        msg = QMessageBox(parent)
        # msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)

        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {self.ui_styles[COLORS][BACKGROUND]};
            }}
            QLabel {{
                font-family: {self.regular_font_family};
                font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
            }}
            QMessageBox QDialogButtonBox {{
                alignment: center;
            }}
        """)

        # Customize the OK button
        ok_button = msg.button(QMessageBox.Ok)
        ok_button.setIcon(QIcon())  # Remove any default icon
        ok_button.setText(ok_text)
        ok_button.setFixedSize(self.ui_styles[SIZES][POPUP_BUTTONS][WIDTH], self.ui_styles[SIZES][POPUP_BUTTONS][HEIGHT])

        ok_button.setStyleSheet(f"""
            QPushButton {{
                padding: px {self.ui_styles[PADDINGS][SETTINGS_BUTTONS_HORIZONTAL]}px px {self.ui_styles[PADDINGS][SETTINGS_BUTTONS_HORIZONTAL]}px;
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][ORANGE]};
                color: {self.ui_styles[COLORS][BLACK]};
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][ORANGE_PRESSED]};
            }}
        """)

        # Show the message box and return the user's response
        return msg.exec_()
    
class ModelSettingsDialog(QtWidgets.QDialog):
    def __init__(self, ui_styles, parent=None, title='Model Settings', model_name='', model_path=''):
        super(ModelSettingsDialog, self).__init__(parent)
        self.ui_styles = ui_styles
        self.setWindowTitle(title)

        self.setFixedSize(ui_styles[SIZES][POPUP_GENERATOR][WIDTH], ui_styles[SIZES][POPUP_GENERATOR][HEIGHT])
        
        self.model_name = model_name
        self.model_path = model_path

        # Load custom font
        regular_font_id = QtGui.QFontDatabase.addApplicationFont(ui_styles[FONTS][REGULAR_FONT_FILE])
        self.regular_font_family = QtGui.QFontDatabase.applicationFontFamilies(regular_font_id)[0]

        # Set stylesheet
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {self.ui_styles[COLORS][BACKGROUND]};
            }}
            QLabel {{
                font-family: {self.regular_font_family};
                font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
            }}
            QLineEdit {{
                font-family: {self.regular_font_family};
                font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
                border: 1px solid {self.ui_styles[COLORS][BLACK]};
                padding: 4px;
            }}
        """)

        # Layout
        layout = QtWidgets.QFormLayout(self)

        # Model Name Field
        name_label = QtWidgets.QLabel("Model Name:")
        name_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.nameLineEdit = QtWidgets.QLineEdit(self)
        self.nameLineEdit.setText(model_name)
        layout.addRow(name_label, self.nameLineEdit)

        # Model Path Field with Browse Button
        path_label = QtWidgets.QLabel("Model Path:")
        path_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.pathLineEdit = QtWidgets.QLineEdit(self)
        self.pathLineEdit.setText(model_path)
        self.browseButton = QtWidgets.QPushButton("Browse")
        self.browseButton.setStyleSheet(f"""
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][BLUE]};
                color: {self.ui_styles[COLORS][BLACK]};
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][BLUE_PRESSED]};
            }}
        """)

        self.browseButton.clicked.connect(self.browse_file)
        path_layout = QtWidgets.QHBoxLayout()
        path_layout.addWidget(self.pathLineEdit)
        path_layout.addWidget(self.browseButton)
        layout.addRow(path_label, path_layout)

        # Save and Cancel Buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.saveButton = QtWidgets.QPushButton("Save")
        self.saveButton.setStyleSheet(f"""
                QPushButton {{
                    border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                    font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
                    border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                    background-color: {self.ui_styles[COLORS][GREEN]};
                    color: {self.ui_styles[COLORS][BLACK]};
                }}
                QPushButton:pressed {{
                    background-color: {self.ui_styles[COLORS][GREEN_PRESSED]};
                }}
            """)
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.setStyleSheet(f"""
                QPushButton {{
                    border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                    font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
                    border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                    background-color: {self.ui_styles[COLORS][RED]};
                    color: {self.ui_styles[COLORS][BLACK]};
                }}
                QPushButton:pressed {{
                    background-color: {self.ui_styles[COLORS][RED_PRESSED]};
                }}
            """)
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

class QualityCheckerDialog(QtWidgets.QDialog):
    def __init__(self, ui_styles, parent=None, function_name='', file_path='', args='', is_editing=False):
        super(QualityCheckerDialog, self).__init__(parent)
        
        regular_font_id = QtGui.QFontDatabase.addApplicationFont(ui_styles[FONTS][REGULAR_FONT_FILE])
        self.regular_font_family = QtGui.QFontDatabase.applicationFontFamilies(regular_font_id)[0]

        # Set dynamic title based on whether it's editing or adding
        operation = "Edit" if is_editing else "Add New"
        self.setWindowTitle(f"{operation} Quality Function")
        self.setFixedSize(ui_styles[SIZES][POPUP_CHECKER][WIDTH], ui_styles[SIZES][POPUP_CHECKER][HEIGHT])

        self.function_name = function_name
        self.file_path = file_path
        self.args = args

        # Layout
        layout = QtWidgets.QFormLayout(self)

        # Function Name
        function_label = QtWidgets.QLabel("Function Name:")
        function_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.nameLineEdit = QtWidgets.QLineEdit(self)
        self.nameLineEdit.setStyleSheet(f"""
            border: {ui_styles[BORDERS][DEFAULT_BORDER]}px {ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-radius: {ui_styles[BORDERS][DEFAULT_RADIUS]}px;
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][TEXT_FONT_SIZE]}px; 
        """)
        self.nameLineEdit.setText(function_name)
        layout.addRow(function_label, self.nameLineEdit)

        # Function File Path with Browse Button
        self.pathLineEdit = QtWidgets.QLineEdit(self)
        self.pathLineEdit.setStyleSheet(f"""
            border: {ui_styles[BORDERS][DEFAULT_BORDER]}px {ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-radius: {ui_styles[BORDERS][DEFAULT_RADIUS]}px;
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][TEXT_FONT_SIZE]}px; 
        """)
        self.pathLineEdit.setText(file_path)
        self.browseButton = QtWidgets.QPushButton("Browse")
        self.browseButton.setStyleSheet(f"""
                QPushButton {{
                    border-radius: {ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                    font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
                    border: {ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                    background-color: {ui_styles[COLORS][BLUE]};
                    color: {ui_styles[COLORS][BLACK]};
                }}
                QPushButton:pressed {{
                    background-color: {ui_styles[COLORS][BLUE_PRESSED]};
                }}
            """)
        self.browseButton.clicked.connect(self.browse_file)
        path_layout = QtWidgets.QHBoxLayout()
        path_layout.addWidget(self.pathLineEdit)
        path_layout.addWidget(self.browseButton)
        function_file_label = QtWidgets.QLabel("Function File Path:")
        function_file_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        layout.addRow(function_file_label, path_layout)

        # Arguments Input
        self.argsLineEdit = QtWidgets.QLineEdit(self)
        self.argsLineEdit.setStyleSheet(f"""
            border: {ui_styles[BORDERS][DEFAULT_BORDER]}px {ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-radius: {ui_styles[BORDERS][DEFAULT_RADIUS]}px;
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][TEXT_FONT_SIZE]}px; 
        """)
        self.argsLineEdit.setText(args)
        arguments_label = QtWidgets.QLabel("Arguments (comma-separated):")
        arguments_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        layout.addRow(arguments_label, self.argsLineEdit)

        # Save and Cancel Buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.saveButton = QtWidgets.QPushButton("Save")
        self.saveButton.setStyleSheet(f"""
                QPushButton {{
                    border-radius: {ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                    font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
                    border: {ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                    background-color: {ui_styles[COLORS][GREEN]};
                    color: {ui_styles[COLORS][BLACK]};
                }}
                QPushButton:pressed {{
                    background-color: {ui_styles[COLORS][GREEN_PRESSED]};
                }}
            """)
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.setStyleSheet(f"""
                QPushButton {{
                    border-radius: {ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                    font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
                    border: {ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                    background-color: {ui_styles[COLORS][RED]};
                    color: {ui_styles[COLORS][BLACK]};
                }}
                QPushButton:pressed {{
                    background-color: {ui_styles[COLORS][RED_PRESSED]};
                }}
            """)
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

        return True

class AnnotatorModelDialog(QtWidgets.QDialog):
    def __init__(self, ui_styles, parent=None, model_data=None, is_editing=False):
        super(AnnotatorModelDialog, self).__init__(parent)
        
        regular_font_id = QtGui.QFontDatabase.addApplicationFont(ui_styles[FONTS][REGULAR_FONT_FILE])
        self.regular_font_family = QtGui.QFontDatabase.applicationFontFamilies(regular_font_id)[0]

        self.setWindowTitle("Edit Model" if is_editing else "Add New Model")
        self.setFixedSize(600, 400)

        self.is_editing = is_editing

        # Initialize model data
        self.model_data = model_data or {}

        # Layout
        layout = QtWidgets.QFormLayout(self)

        # Model Name
        model_name_label = QtWidgets.QLabel("Model Name:")
        model_name_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.nameLineEdit = QtWidgets.QLineEdit(self)
        self.nameLineEdit.setStyleSheet(f"""
            border: {ui_styles[BORDERS][DEFAULT_BORDER]}px {ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-radius: {ui_styles[BORDERS][DEFAULT_RADIUS]}px;
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][TEXT_FONT_SIZE]}px; 
        """)
        self.nameLineEdit.setText(self.model_data.get('Name', ''))
        layout.addRow(model_name_label, self.nameLineEdit)

        # Backbone Type
        backbone_type_label = QtWidgets.QLabel("Backbone Type:")
        backbone_type_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.backboneLineEdit = QtWidgets.QLineEdit(self)
        self.backboneLineEdit.setStyleSheet(f"""
            border: {ui_styles[BORDERS][DEFAULT_BORDER]}px {ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-radius: {ui_styles[BORDERS][DEFAULT_RADIUS]}px;
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][TEXT_FONT_SIZE]}px; 
        """)
        self.backboneLineEdit.setText(self.model_data.get('BACKBONE_TYPE', 'resnet50'))
        layout.addRow(backbone_type_label, self.backboneLineEdit)

        # Classifier Fields
        batchnorm_label = QtWidgets.QLabel("Use Batch Norm (BN):")
        batchnorm_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.bnCheckbox = CustomCheckBox(text='',
                                  width=ui_styles[SIZES][DEFAULT_CHECKBOX][WIDTH], 
                                  height=ui_styles[SIZES][DEFAULT_CHECKBOX][HEIGHT], 
                                  border=ui_styles[BORDERS][DEFAULT_BORDER], 
                                  border_radious=ui_styles[BORDERS][DEFAULT_RADIUS], 
                                  font=ui_styles[FONTS][LABEL_FONT_SIZE],
                                  font_family=self.regular_font_family)
        self.bnCheckbox.setChecked(self.model_data.get('CLASSIFIER', {}).get('BN', False))
        layout.addRow(batchnorm_label, self.bnCheckbox)

        classifier_name_label = QtWidgets.QLabel("Classifier Name:")
        classifier_name_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.classifierNameLineEdit = QtWidgets.QLineEdit(self)
        self.classifierNameLineEdit.setStyleSheet(f"""
            border: {ui_styles[BORDERS][DEFAULT_BORDER]}px {ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-radius: {ui_styles[BORDERS][DEFAULT_RADIUS]}px;
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][TEXT_FONT_SIZE]}px; 
        """)
        self.classifierNameLineEdit.setText(self.model_data.get('CLASSIFIER', {}).get('NAME', 'linear'))
        layout.addRow(classifier_name_label, self.classifierNameLineEdit)

        pooling_label = QtWidgets.QLabel("Pooling Method:")
        pooling_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.poolingLineEdit = QtWidgets.QLineEdit(self)
        self.poolingLineEdit.setStyleSheet(f"""
            border: {ui_styles[BORDERS][DEFAULT_BORDER]}px {ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-radius: {ui_styles[BORDERS][DEFAULT_RADIUS]}px;
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][TEXT_FONT_SIZE]}px; 
        """)
        self.poolingLineEdit.setText(self.model_data.get('CLASSIFIER', {}).get('POOLING', 'avg'))
        layout.addRow(pooling_label, self.poolingLineEdit)

        scale_label = QtWidgets.QLabel("Scale:")
        scale_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.scaleSpinBox = CustomSpinBox(width=ui_styles[SIZES][GENERATION_SPINBOX][WIDTH], 
                                         height=ui_styles[SIZES][GENERATION_SPINBOX][HEIGHT], 
                                         border=ui_styles[BORDERS][DEFAULT_BORDER], 
                                         border_radious=ui_styles[BORDERS][DEFAULT_RADIUS], 
                                         font=ui_styles[FONTS][TEXT_FONT_SIZE],
                                         font_family=self.regular_font_family)
        self.scaleSpinBox.setValue(self.model_data.get('CLASSIFIER', {}).get('SCALE', 1))
        layout.addRow(scale_label, self.scaleSpinBox)

        # Dataset Fields
        dataset_height_label = QtWidgets.QLabel("Dataset Height:")
        dataset_height_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.heightSpinBox = CustomSpinBox(width=ui_styles[SIZES][GENERATION_SPINBOX][WIDTH], 
                                         height=ui_styles[SIZES][GENERATION_SPINBOX][HEIGHT], 
                                         border=ui_styles[BORDERS][DEFAULT_BORDER], 
                                         border_radious=ui_styles[BORDERS][DEFAULT_RADIUS], 
                                         font=ui_styles[FONTS][TEXT_FONT_SIZE],
                                         font_family=self.regular_font_family)
        self.heightSpinBox.setValue(self.model_data.get('DATASET', {}).get('HEIGHT', 256))
        layout.addRow(dataset_height_label, self.heightSpinBox)

        dataset_width_label = QtWidgets.QLabel("Dataset Width:")
        dataset_width_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.widthSpinBox = CustomSpinBox(width=ui_styles[SIZES][GENERATION_SPINBOX][WIDTH], 
                                         height=ui_styles[SIZES][GENERATION_SPINBOX][HEIGHT], 
                                         border=ui_styles[BORDERS][DEFAULT_BORDER], 
                                         border_radious=ui_styles[BORDERS][DEFAULT_RADIUS], 
                                         font=ui_styles[FONTS][TEXT_FONT_SIZE],
                                         font_family=self.regular_font_family)
        self.widthSpinBox.setValue(self.model_data.get('DATASET', {}).get('WIDTH', 192))
        layout.addRow(dataset_width_label, self.widthSpinBox)

        # Model Path
        model_path_label = QtWidgets.QLabel("Model Path:")
        model_path_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.pathLineEdit = QtWidgets.QLineEdit(self)
        self.pathLineEdit.setStyleSheet(f"""
            border: {ui_styles[BORDERS][DEFAULT_BORDER]}px {ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-radius: {ui_styles[BORDERS][DEFAULT_RADIUS]}px;
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][TEXT_FONT_SIZE]}px; 
        """)
        self.pathLineEdit.setText(self.model_data.get('PATH', ''))
        self.browseButton = QtWidgets.QPushButton("Browse")
        self.browseButton.setStyleSheet(f"""
                QPushButton {{
                    border-radius: {ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                    font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
                    border: {ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                    background-color: {ui_styles[COLORS][BLUE]};
                    color: {ui_styles[COLORS][BLACK]};
                }}
                QPushButton:pressed {{
                    background-color: {ui_styles[COLORS][BLUE_PRESSED]};
                }}
            """)
        self.browseButton.clicked.connect(self.browse_file)
        path_layout = QtWidgets.QHBoxLayout()
        path_layout.addWidget(self.pathLineEdit)
        path_layout.addWidget(self.browseButton)
        layout.addRow(model_path_label, path_layout)

        # Color-assisted mode
        color_assisted_label = QtWidgets.QLabel("Color-Assisted Mode:")
        color_assisted_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.colorAssistCheckbox = CustomCheckBox(text='',
                                  width=ui_styles[SIZES][DEFAULT_CHECKBOX][WIDTH], 
                                  height=ui_styles[SIZES][DEFAULT_CHECKBOX][HEIGHT], 
                                  border=ui_styles[BORDERS][DEFAULT_BORDER], 
                                  border_radious=ui_styles[BORDERS][DEFAULT_RADIUS], 
                                  font=ui_styles[FONTS][LABEL_FONT_SIZE],
                                  font_family=self.regular_font_family)
        self.colorAssistCheckbox.setChecked(self.model_data.get('ColorAssist', False))
        layout.addRow(color_assisted_label, self.colorAssistCheckbox)

        # Confidence thresholds
        confidence_thresholds_label = QtWidgets.QLabel("Confidence Thresholds:")
        confidence_thresholds_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.confidenceLineEdit = QtWidgets.QLineEdit(self)
        self.confidenceLineEdit.setStyleSheet(f"""
            border: {ui_styles[BORDERS][DEFAULT_BORDER]}px {ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-radius: {ui_styles[BORDERS][DEFAULT_RADIUS]}px;
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][TEXT_FONT_SIZE]}px; 
        """)
        self.confidenceLineEdit.setText(self.model_data.get('ConfidenceThresholds', ''))
        layout.addRow(confidence_thresholds_label, self.confidenceLineEdit)

        # Save and Cancel Buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.saveButton = QtWidgets.QPushButton("Save")
        self.saveButton.setStyleSheet(f"""
                QPushButton {{
                    border-radius: {ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                    font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
                    border: {ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                    background-color: {ui_styles[COLORS][GREEN]};
                    color: {ui_styles[COLORS][BLACK]};
                }}
                QPushButton:pressed {{
                    background-color: {ui_styles[COLORS][GREEN_PRESSED]};
                }}
            """)
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.setStyleSheet(f"""
                QPushButton {{
                    border-radius: {ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                    font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
                    border: {ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                    background-color: {ui_styles[COLORS][RED]};
                    color: {ui_styles[COLORS][BLACK]};
                }}
                QPushButton:pressed {{
                    background-color: {ui_styles[COLORS][RED_PRESSED]};
                }}
            """)
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

class AddThresholdDialog(QtWidgets.QDialog):
    def __init__(self, ui_styles, min_value, max_value, color=None, value=None, parent=None, color_mapping=None):
        """
        Dialog for adding/editing a confidence threshold.
        If `color` and `value` are provided, the dialog works in edit mode.
        """
        super(AddThresholdDialog, self).__init__(parent)
        self.setWindowTitle("Edit Confidence Threshold" if color else "Add Confidence Threshold")
        self.setFixedSize(ui_styles[SIZES][POPUP_ANNOTATOR_CONFIDENCE][WIDTH], ui_styles[SIZES][POPUP_ANNOTATOR_CONFIDENCE][HEIGHT])

        regular_font_id = QtGui.QFontDatabase.addApplicationFont(ui_styles[FONTS][REGULAR_FONT_FILE])
        self.regular_font_family = QtGui.QFontDatabase.applicationFontFamilies(regular_font_id)[0]

        self.layout = QtWidgets.QVBoxLayout(self)

        # Color selection dropdown
        self.colorLabel = QtWidgets.QLabel("Select Color:")
        self.colorLabel.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.colorComboBox = CustomComboBox(width=ui_styles[SIZES][COMBO_MODELS][WIDTH], 
                                         height=ui_styles[SIZES][GENERATION_SPINBOX][HEIGHT], 
                                         border=ui_styles[BORDERS][DEFAULT_BORDER], 
                                         border_radius=ui_styles[BORDERS][DEFAULT_RADIUS], 
                                         font=ui_styles[FONTS][TEXT_FONT_SIZE],
                                         font_family=self.regular_font_family)
        if color and color_mapping:
            self.colorComboBox.addItems(color_mapping.keys())
            self.colorComboBox.setCurrentText(color)
        elif color:
            self.colorComboBox.addItems(["red", "green", "blue", "yellow", "orange", "purple"])
            self.colorComboBox.setCurrentText(color)
        else:
            self.colorComboBox.addItems(color_mapping.keys())
            self.colorComboBox.setCurrentText(list(color_mapping.keys())[0])

        # Threshold value spin box
        self.thresholdLabel = QtWidgets.QLabel(f"Enter Threshold Value ({min_value} - {max_value}):")
        self.thresholdLabel.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.thresholdSpinBox = CustomDoubleSpinBox(width=ui_styles[SIZES][DOUBLE_SPIN_BOX][WIDTH], 
                                         height=ui_styles[SIZES][GENERATION_SPINBOX][HEIGHT], 
                                         border=ui_styles[BORDERS][DEFAULT_BORDER], 
                                         border_radious=ui_styles[BORDERS][DEFAULT_RADIUS], 
                                         font=ui_styles[FONTS][TEXT_FONT_SIZE],
                                         font_family=self.regular_font_family)
        self.thresholdSpinBox.setRange(min_value, max_value)
        self.thresholdSpinBox.setSingleStep(0.01)
        self.thresholdSpinBox.setValue(value if value else min_value)

        # Buttons
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        ok_button = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        ok_button.setIcon(QIcon())
        ok_button.setFixedSize(ui_styles[SIZES][POPUP_ANNOTATOR_CONFIDENCE][WIDTH]//2-15, ui_styles[SIZES][POPUP_BUTTONS][HEIGHT])
        cancel_button = self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel)
        cancel_button.setIcon(QIcon())
        cancel_button.setFixedSize(ui_styles[SIZES][POPUP_ANNOTATOR_CONFIDENCE][WIDTH]//2-15, ui_styles[SIZES][POPUP_BUTTONS][HEIGHT])
        ok_button.setStyleSheet(f"""
                QPushButton {{
                    border-radius: {ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                    font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
                    border: {ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                    background-color: {ui_styles[COLORS][GREEN]};
                    color: {ui_styles[COLORS][BLACK]};
                }}
                QPushButton:pressed {{
                    background-color: {ui_styles[COLORS][GREEN_PRESSED]};
                }}
            """)
        cancel_button.setStyleSheet(f"""
                QPushButton {{
                    border-radius: {ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                    font-size: {ui_styles[FONTS][LABEL_FONT_SIZE]}px;
                    border: {ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                    background-color: {ui_styles[COLORS][RED]};
                    color: {ui_styles[COLORS][BLACK]};
                }}
                QPushButton:pressed {{
                    background-color: {ui_styles[COLORS][RED_PRESSED]};
                }}
            """)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Add widgets to layout
        self.layout.addWidget(self.colorLabel)
        self.layout.addWidget(self.colorComboBox)
        self.layout.addWidget(self.thresholdLabel)
        self.layout.addWidget(self.thresholdSpinBox)
        self.layout.addWidget(self.buttonBox)

    def get_data(self):
        """Return the selected color and threshold value."""
        return self.colorComboBox.currentText(), self.thresholdSpinBox.value()
