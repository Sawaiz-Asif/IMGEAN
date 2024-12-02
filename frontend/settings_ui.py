from PyQt5 import QtCore, QtGui, QtWidgets
from ui_styles_constants import *
from config_constants import *

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QGridLayout, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase

class Ui_SettingsWindow(object):
    def __init__(self, config, ui_styles):
        self.config = config
        self.ui_styles = ui_styles

        regular_font_id = QFontDatabase.addApplicationFont(self.ui_styles[FONTS][REGULAR_FONT_FILE])
        self.regular_font_family = QFontDatabase.applicationFontFamilies(regular_font_id)[0]

    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")

        self.centralwidget = QtWidgets.QWidget(SettingsWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.main_layout = QtWidgets.QGridLayout(self.centralwidget)

        self.setup_top_section()

        # Create a scrollable area for the main content
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setStyleSheet(f"""
                font-family: '{self.regular_font_family}'; /* Title font family */
                font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; /* Title font size */
                border: none;
        """) # TODO format the vertical bar
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.main_layout.addWidget(self.scrollArea, 1, 0, 1, 2)

        # Layout to place all sections vertically within the scrollable area
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(10, 0, 10, 0)  # No margin around the layout
        self.verticalLayout.setSpacing(0)

        # Dataset Section
        self.datasetGroup = QtWidgets.QGroupBox("Dataset")
        self.datasetGroup.setStyleSheet(f"""
            QGroupBox {{
                background-color: {self.ui_styles[COLORS][BACKGROUND]};
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-top-right-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px;
                border-bottom-left-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px;
                margin-top: {self.ui_styles[PADDINGS][SETTINGS_BOX_FROM_TITLE]}px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: {self.ui_styles[PADDINGS][SETTINGS_TITLE_VERTICAL]}px {self.ui_styles[PADDINGS][SETTINGS_TITLE_HORIZONTAL]}px;
                background-color: {self.ui_styles[COLORS][LIGHT_GRAY]};
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-top-left-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px;
                border-top-right-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px;
            }}
        """)
        self.datasetLayout = QtWidgets.QFormLayout(self.datasetGroup)

        # Description (currently the name)
        self.descriptionLineEdit = QtWidgets.QLineEdit(self.datasetGroup)
        self.descriptionLineEdit.setStyleSheet(f"""
            QLineEdit {{
                border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            }}
        """)
        self.datasetLayout.addRow("Description:", self.descriptionLineEdit)

        # Pickle File Path
        self.pickleFilePathLineEdit = QtWidgets.QLineEdit(self.datasetGroup)
        self.pickleFilePathLineEdit.setStyleSheet(f"""
            QLineEdit {{
                border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            }}
        """)
        self.pickleFilePathBrowseButton = QtWidgets.QPushButton("Browse", self.datasetGroup)
        self.pickleFilePathBrowseButton.setStyleSheet(f"""
            padding: px {self.ui_styles[PADDINGS][SETTINGS_BUTTONS_HORIZONTAL]}px px {self.ui_styles[PADDINGS][SETTINGS_BUTTONS_HORIZONTAL]}px;
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][BLUE]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.pickleFilePathLayout = QtWidgets.QHBoxLayout()
        self.pickleFilePathLayout.addWidget(self.pickleFilePathLineEdit)
        self.pickleFilePathLayout.addWidget(self.pickleFilePathBrowseButton)
        self.datasetLayout.addRow("Pickle File Path:", self.pickleFilePathLayout)

        # Labels List
        self.labelsListWidget = QtWidgets.QListWidget(self.datasetGroup)
        self.labelsListWidget.setStyleSheet(f"""
            QListWidget {{
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
            }}
            QListWidget::item {{
                border: none;
                padding: 5px;
            }}
        """)
        self.addLabelButton = QtWidgets.QPushButton("Add Label", self.datasetGroup)
        self.addLabelButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][GREEN]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.editLabelButton = QtWidgets.QPushButton("Edit Label", self.datasetGroup)
        self.editLabelButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][YELLOW]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.removeLabelButton = QtWidgets.QPushButton("Remove Label", self.datasetGroup)
        self.removeLabelButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][RED]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.labelsButtonLayout = QtWidgets.QHBoxLayout()
        self.labelsButtonLayout.addWidget(self.addLabelButton)
        self.labelsButtonLayout.addWidget(self.editLabelButton)
        self.labelsButtonLayout.addWidget(self.removeLabelButton)
        self.datasetLayout.addRow("Labels:", self.labelsListWidget)
        self.datasetLayout.addRow("", self.labelsButtonLayout)

        self.verticalLayout.addWidget(self.datasetGroup)

        # Save Button
        self.saveDatasetButton = QtWidgets.QPushButton("Save Dataset Settings")
        self.saveDatasetButton.setStyleSheet(f"""
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border-bottom-left-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
            border-bottom-right-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
            border-right: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-left: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-bottom: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][BLUE]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.saveDatasetButton.setFixedSize(self.ui_styles[SIZES][SETTINGS_SAVE_BUTTONS][WIDTH], self.ui_styles[SIZES][SETTINGS_SAVE_BUTTONS][HEIGHT])
        self.verticalLayout.addWidget(self.saveDatasetButton, alignment=Qt.AlignBottom | Qt.AlignRight)


        # Image Generator Section
        self.imageGenGroup = QtWidgets.QGroupBox("Image Generator")
        self.imageGenGroup.setStyleSheet(f"""
            QGroupBox {{
                background-color: {self.ui_styles[COLORS][BACKGROUND]};
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-top-right-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px;
                border-bottom-left-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px;
                margin-top: {self.ui_styles[PADDINGS][SETTINGS_BOX_FROM_TITLE]}px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: {self.ui_styles[PADDINGS][SETTINGS_TITLE_VERTICAL]}px {self.ui_styles[PADDINGS][SETTINGS_TITLE_HORIZONTAL]}px;
                background-color: {self.ui_styles[COLORS][LIGHT_GRAY]};
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-top-left-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px;
                border-top-right-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px;
            }}
        """)
        self.imageGenLayout = QtWidgets.QFormLayout(self.imageGenGroup)

        # Default Output Folder
        self.outputFolderLineEdit = QtWidgets.QLineEdit(self.imageGenGroup)
        self.outputFolderLineEdit.setStyleSheet(f"""
            QLineEdit {{
                border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            }}
        """)
        self.outputFolderBrowseButton = QtWidgets.QPushButton("Browse", self.imageGenGroup)
        self.outputFolderBrowseButton.setStyleSheet(f"""
            padding: px {self.ui_styles[PADDINGS][SETTINGS_BUTTONS_HORIZONTAL]}px px {self.ui_styles[PADDINGS][SETTINGS_BUTTONS_HORIZONTAL]}px;
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][BLUE]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.outputFolderLayout = QtWidgets.QHBoxLayout()
        self.outputFolderLayout.addWidget(self.outputFolderLineEdit)
        self.outputFolderLayout.addWidget(self.outputFolderBrowseButton)
        self.imageGenLayout.addRow("Default Output Folder:", self.outputFolderLayout)

        # Default ComfyUI IP
        self.comfyUiIpLineEdit = QtWidgets.QLineEdit(self.imageGenGroup)
        self.comfyUiIpLineEdit.setStyleSheet(f"""
            QLineEdit {{
                border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            }}
        """)
        self.imageGenLayout.addRow("Default ComfyUI IP:", self.comfyUiIpLineEdit)

        # Models List
        self.imageModelsList = QtWidgets.QListWidget(self.imageGenGroup)
        self.imageModelsList.setStyleSheet(f"""
            QListWidget {{
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
            }}
            QListWidget::item {{
                border: none;
                padding: 5px;
            }}
        """)
        self.imageGenLayout.addRow("Models:", self.imageModelsList)

        # Buttons for model management
        self.addNewImageModelButton = QtWidgets.QPushButton("Add New Model", self.imageGenGroup)
        self.addNewImageModelButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][GREEN]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.imageModelSettingsButton = QtWidgets.QPushButton("Model Settings", self.imageGenGroup)
        self.imageModelSettingsButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][YELLOW]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.removeImageModelButton = QtWidgets.QPushButton("Remove Model", self.imageGenGroup)
        self.removeImageModelButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][RED]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.imageModelButtonLayout = QtWidgets.QHBoxLayout()
        self.imageModelButtonLayout.addWidget(self.addNewImageModelButton)
        self.imageModelButtonLayout.addWidget(self.imageModelSettingsButton)
        self.imageModelButtonLayout.addWidget(self.removeImageModelButton)
        self.imageGenLayout.addRow("", self.imageModelButtonLayout)

        self.verticalLayout.addWidget(self.imageGenGroup)

        # Save Button
        self.saveImageGenButton = QtWidgets.QPushButton("Save Image Generator Settings")
        self.saveImageGenButton.setStyleSheet(f"""
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border-bottom-left-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
            border-bottom-right-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
            border-right: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-left: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-bottom: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][BLUE]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.saveImageGenButton.setFixedSize(self.ui_styles[SIZES][SETTINGS_SAVE_BUTTONS][WIDTH], self.ui_styles[SIZES][SETTINGS_SAVE_BUTTONS][HEIGHT])
        self.verticalLayout.addWidget(self.saveImageGenButton, alignment=Qt.AlignBottom | Qt.AlignRight)


        # Quality Checker Section
        self.qualityCheckerGroup = QtWidgets.QGroupBox("Quality Checker")
        self.qualityCheckerGroup.setStyleSheet(f"""
            QGroupBox {{
                background-color: {self.ui_styles[COLORS][BACKGROUND]};
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-top-right-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px;
                border-bottom-left-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px;
                margin-top: {self.ui_styles[PADDINGS][SETTINGS_BOX_FROM_TITLE]}px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: {self.ui_styles[PADDINGS][SETTINGS_TITLE_VERTICAL]}px {self.ui_styles[PADDINGS][SETTINGS_TITLE_HORIZONTAL]}px;
                background-color: {self.ui_styles[COLORS][LIGHT_GRAY]};
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-top-left-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px;
                border-top-right-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px;
            }}
        """)
        self.qualityCheckerLayout = QtWidgets.QFormLayout(self.qualityCheckerGroup)

        # Functions List
        self.qualityFunctionsList = QtWidgets.QListWidget(self.qualityCheckerGroup)
        self.qualityFunctionsList.setStyleSheet(f"""
            QListWidget {{
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
            }}
            QListWidget::item {{
                border: none;
                padding: 5px;
            }}
        """)
        self.qualityCheckerLayout.addRow("Functions:", self.qualityFunctionsList)

        # Buttons for function management
        self.addNewQualityFunctionButton = QtWidgets.QPushButton("Add New Function", self.qualityCheckerGroup)
        self.addNewQualityFunctionButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][GREEN]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.qualityFunctionSettingsButton = QtWidgets.QPushButton("Function Settings", self.qualityCheckerGroup)
        self.qualityFunctionSettingsButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][YELLOW]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.removeQualityFunctionButton = QtWidgets.QPushButton("Remove Function", self.qualityCheckerGroup)
        self.removeQualityFunctionButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][RED]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.qualityFunctionButtonLayout = QtWidgets.QHBoxLayout()
        self.qualityFunctionButtonLayout.addWidget(self.addNewQualityFunctionButton)
        self.qualityFunctionButtonLayout.addWidget(self.qualityFunctionSettingsButton)
        self.qualityFunctionButtonLayout.addWidget(self.removeQualityFunctionButton)
        self.qualityCheckerLayout.addRow("", self.qualityFunctionButtonLayout)

        self.verticalLayout.addWidget(self.qualityCheckerGroup)

        # Save Button
        self.saveQualityCheckerButton = QtWidgets.QPushButton("Save Quality Checker Settings")
        self.saveQualityCheckerButton.setStyleSheet(f"""
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border-bottom-left-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
            border-bottom-right-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
            border-right: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-left: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-bottom: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][BLUE]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.saveQualityCheckerButton.setFixedSize(self.ui_styles[SIZES][SETTINGS_SAVE_BUTTONS][WIDTH], self.ui_styles[SIZES][SETTINGS_SAVE_BUTTONS][HEIGHT])
        self.verticalLayout.addWidget(self.saveQualityCheckerButton, alignment=Qt.AlignBottom | Qt.AlignRight)


        # Annotator Section
        self.annotatorGroup = QtWidgets.QGroupBox("Annotator")
        self.annotatorGroup.setStyleSheet(f"""
            QGroupBox {{
                background-color: {self.ui_styles[COLORS][BACKGROUND]};
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-top-right-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px;
                border-bottom-left-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px;
                margin-top: {self.ui_styles[PADDINGS][SETTINGS_BOX_FROM_TITLE]}px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: {self.ui_styles[PADDINGS][SETTINGS_TITLE_VERTICAL]}px {self.ui_styles[PADDINGS][SETTINGS_TITLE_HORIZONTAL]}px;
                background-color: {self.ui_styles[COLORS][LIGHT_GRAY]};
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-top-left-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px;
                border-top-right-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px;
            }}
        """)
        self.annotatorLayout = QtWidgets.QFormLayout(self.annotatorGroup)

        self.currentSelectionComboBox = QtWidgets.QComboBox(self.annotatorGroup)
        self.currentSelectionComboBox.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
            background-color: {self.ui_styles[COLORS][BACKGROUND]};
            color: {self.ui_styles[COLORS][BLACK]};
            padding: 5px;
        """)
        self.annotatorLayout.addRow("Current Selection:", self.currentSelectionComboBox)

        # Annotator Options Widget Creation
        annotator_options_widget = QtWidgets.QWidget()
        annotator_options_layout = QtWidgets.QHBoxLayout(annotator_options_widget)  # Use layout for the widget
        annotator_options_widget.setLayout(annotator_options_layout)


        color_assist_label = QtWidgets.QLabel("Enable Color-Assisted Mode", annotator_options_widget)
        self.colorAssistCheckbox = QtWidgets.QCheckBox("", annotator_options_widget)  # Empty label for the checkbox itself

        annotator_options_layout.addWidget(color_assist_label, alignment=Qt.AlignRight)
        annotator_options_layout.addWidget(self.colorAssistCheckbox, alignment=Qt.AlignLeft)

        # Max Auto Label (SpinBox with Label)
        max_auto_label_label = QtWidgets.QLabel("MAX_AUTO_LABEL:", annotator_options_widget)
        self.maxAutoLabelSpinBox = QtWidgets.QSpinBox(annotator_options_widget)
        self.maxAutoLabelSpinBox.setStyleSheet(f"""
        font-family: '{self.regular_font_family}';
        font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
        background-color: {self.ui_styles[COLORS][BACKGROUND]};
        border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
        """) # TODO Add arrows here
        self.maxAutoLabelSpinBox.setRange(1, 1000)
        self.maxAutoLabelSpinBox.setFixedWidth(self.ui_styles[SIZES][SPIN_BOX][WIDTH])
        self.maxAutoLabelSpinBox.setMaximumWidth(self.ui_styles[SIZES][SPIN_BOX][WIDTH])

        annotator_options_layout.addWidget(max_auto_label_label, alignment=Qt.AlignRight)
        annotator_options_layout.addWidget(self.maxAutoLabelSpinBox, alignment=Qt.AlignLeft)

        # Checkbox Threshold (DoubleSpinBox with Label)
        checkbox_threshold_label = QtWidgets.QLabel("CHECKBOX_THRESHOLD:", annotator_options_widget)
        self.checkboxThresholdSpinBox = QtWidgets.QDoubleSpinBox(annotator_options_widget)
        self.checkboxThresholdSpinBox.setStyleSheet(f"""
        font-family: '{self.regular_font_family}';
        font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
        background-color: {self.ui_styles[COLORS][BACKGROUND]};
        border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
        """) # TODO Add arrows here
        self.checkboxThresholdSpinBox.setMinimum(0.0)
        self.checkboxThresholdSpinBox.setMaximum(1.0)
        self.checkboxThresholdSpinBox.setSingleStep(0.01)
        self.checkboxThresholdSpinBox.setFixedWidth(self.ui_styles[SIZES][SPIN_BOX][WIDTH]+self.ui_styles[PADDINGS][MIN_SIDES])
        self.checkboxThresholdSpinBox.setMaximumWidth(self.ui_styles[SIZES][SPIN_BOX][WIDTH])

        # Add both label and spinbox to layout
        annotator_options_layout.addWidget(checkbox_threshold_label, alignment=Qt.AlignRight)
        annotator_options_layout.addWidget(self.checkboxThresholdSpinBox, alignment=Qt.AlignLeft)

        # Default Color (ComboBox with Label)
        default_color_label = QtWidgets.QLabel("Default Color:", annotator_options_widget)
        self.defaultColorComboBox = QtWidgets.QComboBox(annotator_options_widget)
        self.defaultColorComboBox.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
            background-color: {self.ui_styles[COLORS][BACKGROUND]};
            color: {self.ui_styles[COLORS][BLACK]};
            padding: 5px;
        """)
        self.defaultColorComboBox.addItems(["red", "green", "blue", "yellow", "orange", "purple"])

        # Add both label and combobox to layout
        annotator_options_layout.addWidget(default_color_label, alignment=Qt.AlignRight)
        annotator_options_layout.addWidget(self.defaultColorComboBox, alignment=Qt.AlignLeft)

        # Add the annotator options widget to the form layout (assuming annotatorLayout is already defined)
        self.annotatorLayout.addRow(annotator_options_widget)

        # Confidence Thresholds List
        self.confidenceThresholdList = QtWidgets.QListWidget(self.annotatorGroup)
        self.confidenceThresholdList.setStyleSheet(f"""
            QListWidget {{
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
            }}
            QListWidget::item {{
                border: none;
                padding: 5px;
            }}
        """)
        self.addConfidenceButton = QtWidgets.QPushButton("Add Threshold", self.annotatorGroup)
        self.addConfidenceButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][GREEN]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.editConfidenceButton = QtWidgets.QPushButton("Edit Threshold", self.annotatorGroup)
        self.editConfidenceButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][YELLOW]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.removeConfidenceButton = QtWidgets.QPushButton("Remove Threshold", self.annotatorGroup)
        self.removeConfidenceButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][RED]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        
        self.confidenceButtonLayout = QtWidgets.QHBoxLayout()
        self.confidenceButtonLayout.addWidget(self.addConfidenceButton)
        self.confidenceButtonLayout.addWidget(self.editConfidenceButton)
        self.confidenceButtonLayout.addWidget(self.removeConfidenceButton)
        self.annotatorLayout.addRow("Confidence Thresholds:", self.confidenceThresholdList)
        self.annotatorLayout.addRow("", self.confidenceButtonLayout)

        # Models List
        self.annotatorModelsList = QtWidgets.QListWidget(self.annotatorGroup)
        self.annotatorModelsList.setStyleSheet(f"""
            QListWidget {{
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
            }}
            QListWidget::item {{
                border: none;
                padding: 5px;
            }}
        """)
        self.annotatorLayout.addRow("Models:", self.annotatorModelsList)

        # Buttons for model management
        self.addModelButton = QtWidgets.QPushButton("Add Model", self.annotatorGroup)
        self.addModelButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][GREEN]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.editModelButton = QtWidgets.QPushButton("Edit Model", self.annotatorGroup)
        self.editModelButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][YELLOW]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.removeModelButton = QtWidgets.QPushButton("Remove Model", self.annotatorGroup)
        self.removeModelButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][RED]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)

        self.modelsButtonLayout = QtWidgets.QHBoxLayout()
        self.modelsButtonLayout.addWidget(self.addModelButton)
        self.modelsButtonLayout.addWidget(self.editModelButton)
        self.modelsButtonLayout.addWidget(self.removeModelButton)

        self.annotatorLayout.addRow("", self.modelsButtonLayout)

        self.verticalLayout.addWidget(self.annotatorGroup)

        # Save Button
        self.saveAnnotatorButton = QtWidgets.QPushButton("Save Annotator Settings")
        self.saveAnnotatorButton.setStyleSheet(f"""
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border-bottom-left-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
            border-bottom-right-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
            border-right: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-left: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            border-bottom: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][BLUE]}; 
            color: {self.ui_styles[COLORS][BLACK]}
        """)
        self.saveAnnotatorButton.setFixedSize(self.ui_styles[SIZES][SETTINGS_SAVE_BUTTONS][WIDTH], self.ui_styles[SIZES][SETTINGS_SAVE_BUTTONS][HEIGHT])
        self.verticalLayout.addWidget(self.saveAnnotatorButton, alignment=Qt.AlignBottom | Qt.AlignRight)


        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

        """ def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "Settings & Setup")) """
        SettingsWindow.setCentralWidget(self.centralwidget)

    def setup_top_section(self):
        # General top layout
        self.top_section_layout = QtWidgets.QGridLayout()
        self.top_section_layout.setContentsMargins(0, 5, 0, 0)
        self.top_section_layout.setSpacing(0)

        # This are weights for each column, so we can center the title
        self.top_section_layout.setColumnStretch(0, 1)  # Left side
        self.top_section_layout.setColumnStretch(1, 2)  # Center column
        self.top_section_layout.setColumnStretch(2, 1)  # Right side

        # Return Button in the Top-Left
        returnButton = QPushButton("Return")
        returnButton.setFixedSize(
            self.ui_styles[SIZES][RETURN_BUTTON][WIDTH],
            self.ui_styles[SIZES][RETURN_BUTTON][HEIGHT]
        )
        returnButton.setStyleSheet(f"""
            border-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][RETURN_BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][ORANGE]}; 
        """)
        self.returnButton = returnButton
        self.top_section_layout.addWidget(self.returnButton, 0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Title Fully Centered
        title = QLabel("Settings & setup")
        bold_font_id = QFontDatabase.addApplicationFont(self.ui_styles[FONTS][BOLD_FONT_FILE])
        bold_font_family = QFontDatabase.applicationFontFamilies(bold_font_id)[0]
        title.setStyleSheet(f"""
            font-family: '{bold_font_family}';
            font-size: {self.ui_styles[FONTS][TITLE_FONT_SIZE]}px;
            text-align: center;
        """)
        title.setAlignment(Qt.AlignCenter)
        self.top_section_layout.addWidget(title, 0, 1, alignment=Qt.AlignCenter)

        # Add the top section layout to the main grid
        self.main_layout.addLayout(self.top_section_layout, 0, 0)