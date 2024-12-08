from PyQt5 import QtCore, QtGui, QtWidgets
from ui_styles_constants import *
from config_constants import *

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QGridLayout, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase

from frontend.custom_ui_widgets import CustomCheckBox, CustomSpinBox, CustomDoubleSpinBox, CustomComboBox

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
                QScrollArea {{
                    font-family: '{self.regular_font_family}'; /* Title font family */
                    font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; /* Title font size */
                    border: none;
                }}
                QScrollBar:vertical {{              
                width: 6px;
                margin: 0px 0px 0px 0px;
                }}
                QScrollBar::handle:vertical {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop: 0 {self.ui_styles[COLORS][BLACK]}, stop: 0.5 {self.ui_styles[COLORS][BLACK]}, stop:1 {self.ui_styles[COLORS][BLACK]});
                    min-height: 0px;
                }}
                QScrollBar::add-line:vertical {{
                    height: 0px;
                }}
                QScrollBar::sub-line:vertical {{
                    height: 0 px;
                }}
        """)
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
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][SETTING_GROUP_TITLE]}px; 
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
        label_description = QLabel("Description:")
        label_description.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.descriptionLineEdit = QtWidgets.QLineEdit(self.datasetGroup)
        self.descriptionLineEdit.setStyleSheet(f"""
            QLineEdit {{
                border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
            }}
        """)
        self.datasetLayout.addRow(label_description, self.descriptionLineEdit)

        # Pickle File Path
        label_pickle = QLabel("Pickle File Path:")
        label_pickle.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.pickleFilePathLineEdit = QtWidgets.QLineEdit(self.datasetGroup)
        self.pickleFilePathLineEdit.setStyleSheet(f"""
            QLineEdit {{
                border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
            }}
        """)
        self.pickleFilePathBrowseButton = QtWidgets.QPushButton("Browse", self.datasetGroup)
        self.pickleFilePathBrowseButton.setStyleSheet(f"""
            QPushButton {{
                padding: px {self.ui_styles[PADDINGS][SETTINGS_BUTTONS_HORIZONTAL]}px px {self.ui_styles[PADDINGS][SETTINGS_BUTTONS_HORIZONTAL]}px;
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][BLUE]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][BLUE_PRESSED]};
            }}
        """)
        self.pickleFilePathLayout = QtWidgets.QHBoxLayout()
        self.pickleFilePathLayout.addWidget(self.pickleFilePathLineEdit)
        self.pickleFilePathLayout.addWidget(self.pickleFilePathBrowseButton)
        self.datasetLayout.addRow(label_pickle, self.pickleFilePathLayout)

        # Labels List
        label_dataset_labels = QLabel("Labels:")
        label_dataset_labels.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.labelsListWidget = QtWidgets.QListWidget(self.datasetGroup)
        self.labelsListWidget.setStyleSheet(f"""
            QListWidget {{
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
            }}
            QListWidget::item {{
                background-color: {self.ui_styles[COLORS][BACKGROUND]};
            }}
            QListWidget::item:selected {{
                background-color: {self.ui_styles[COLORS][BACKGROUND_PRESSED]};
                color: black;
            }}
        """)
        self.labelsListWidget.setFixedHeight(self.ui_styles[SIZES][SETTINGS_LISTS][HEIGHT])
        self.addLabelButton = QtWidgets.QPushButton("Add Label", self.datasetGroup)
        self.addLabelButton.setStyleSheet(f"""
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][GREEN]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][GREEN_PRESSED]};
            }}
        """)
        self.editLabelButton = QtWidgets.QPushButton("Edit Label", self.datasetGroup)
        self.editLabelButton.setStyleSheet(f"""
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][YELLOW]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][YELLOW_PRESSED]};
            }}
        """)
        self.removeLabelButton = QtWidgets.QPushButton("Remove Label", self.datasetGroup)
        self.removeLabelButton.setStyleSheet(f"""
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][RED]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][RED_PRESSED]};
            }}
        """)
        self.labelsButtonLayout = QtWidgets.QHBoxLayout()
        self.labelsButtonLayout.addWidget(self.addLabelButton)
        self.labelsButtonLayout.addWidget(self.editLabelButton)
        self.labelsButtonLayout.addWidget(self.removeLabelButton)
        self.datasetLayout.addRow(label_dataset_labels, self.labelsListWidget)
        self.datasetLayout.addRow("", self.labelsButtonLayout)

        self.verticalLayout.addWidget(self.datasetGroup)

        # Save Button
        self.saveDatasetButton = QtWidgets.QPushButton("Save Dataset Settings")
        self.saveDatasetButton.setStyleSheet(f"""
            QPushButton {{
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border-bottom-left-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                border-bottom-right-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                border-right: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-left: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-bottom: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][BLUE]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][BLUE_PRESSED]};
            }}
        """)
        self.saveDatasetButton.setFixedSize(self.ui_styles[SIZES][SETTINGS_SAVE_BUTTONS][WIDTH], self.ui_styles[SIZES][SETTINGS_SAVE_BUTTONS][HEIGHT])
        self.verticalLayout.addWidget(self.saveDatasetButton, alignment=Qt.AlignBottom | Qt.AlignRight)


        # Image Generator Section
        self.imageGenGroup = QtWidgets.QGroupBox("Image Generator")
        self.imageGenGroup.setStyleSheet(f"""
            QGroupBox {{
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][SETTING_GROUP_TITLE]}px; 
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
        label_output = QLabel("Default Output Folder:")
        label_output.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.outputFolderLineEdit = QtWidgets.QLineEdit(self.imageGenGroup)
        self.outputFolderLineEdit.setStyleSheet(f"""
            QLineEdit {{
                border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
            }}
        """)
        self.outputFolderBrowseButton = QtWidgets.QPushButton("Browse", self.imageGenGroup)
        self.outputFolderBrowseButton.setStyleSheet(f"""
            QPushButton {{
                padding: px {self.ui_styles[PADDINGS][SETTINGS_BUTTONS_HORIZONTAL]}px px {self.ui_styles[PADDINGS][SETTINGS_BUTTONS_HORIZONTAL]}px;
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][BLUE]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][BLUE_PRESSED]};
            }}
        """)
        self.outputFolderLayout = QtWidgets.QHBoxLayout()
        self.outputFolderLayout.addWidget(self.outputFolderLineEdit)
        self.outputFolderLayout.addWidget(self.outputFolderBrowseButton)
        self.imageGenLayout.addRow(label_output, self.outputFolderLayout)

        # Default ComfyUI IP
        label_comfy_ip = QLabel("Default ComfyUI IP:")
        label_comfy_ip.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.comfyUiIpLineEdit = QtWidgets.QLineEdit(self.imageGenGroup)
        self.comfyUiIpLineEdit.setStyleSheet(f"""
            QLineEdit {{
                border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px; 
            }}
        """)
        self.imageGenLayout.addRow(label_comfy_ip, self.comfyUiIpLineEdit)

        # Models List
        label_models = QLabel("Models:")
        label_models.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.imageModelsList = QtWidgets.QListWidget(self.imageGenGroup)
        self.imageModelsList.setStyleSheet(f"""
            QListWidget {{
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
            }}
            QListWidget::item {{
                background-color: {self.ui_styles[COLORS][BACKGROUND]};
            }}
            QListWidget::item:selected {{
                background-color: {self.ui_styles[COLORS][BACKGROUND_PRESSED]};
                color: black;
            }}
        """)
        self.imageModelsList.setFixedHeight(self.ui_styles[SIZES][SETTINGS_LISTS][HEIGHT])
        self.imageGenLayout.addRow(label_models, self.imageModelsList)

        # Buttons for model management
        self.addNewImageModelButton = QtWidgets.QPushButton("Add New Model", self.imageGenGroup)
        self.addNewImageModelButton.setStyleSheet(f"""
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][GREEN]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][GREEN_PRESSED]};
            }}
        """)
        self.imageModelSettingsButton = QtWidgets.QPushButton("Model Settings", self.imageGenGroup)
        self.imageModelSettingsButton.setStyleSheet(f"""
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][YELLOW]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][YELLOW_PRESSED]};
            }}
        """)
        self.removeImageModelButton = QtWidgets.QPushButton("Remove Model", self.imageGenGroup)
        self.removeImageModelButton.setStyleSheet(f"""
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][RED]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][RED_PRESSED]};
            }}
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
            QPushButton {{
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border-bottom-left-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                border-bottom-right-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                border-right: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-left: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-bottom: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][BLUE]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][BLUE_PRESSED]};
            }}
        """)
        self.saveImageGenButton.setFixedSize(self.ui_styles[SIZES][SETTINGS_SAVE_BUTTONS][WIDTH], self.ui_styles[SIZES][SETTINGS_SAVE_BUTTONS][HEIGHT])
        self.verticalLayout.addWidget(self.saveImageGenButton, alignment=Qt.AlignBottom | Qt.AlignRight)


        # Quality Checker Section
        self.qualityCheckerGroup = QtWidgets.QGroupBox("Quality Checker")
        self.qualityCheckerGroup.setStyleSheet(f"""
            QGroupBox {{
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][SETTING_GROUP_TITLE]}px; 
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
        label_functions = QLabel("Functions:")
        label_functions.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.qualityFunctionsList = QtWidgets.QListWidget(self.qualityCheckerGroup)
        self.qualityFunctionsList.setStyleSheet(f"""
            QListWidget {{
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][TEXT_FONT_SIZE]}px;
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-radius: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px;
            }}
            QListWidget::item {{
                background-color: {self.ui_styles[COLORS][BACKGROUND]};
            }}
            QListWidget::item:selected {{
                background-color: {self.ui_styles[COLORS][BACKGROUND_PRESSED]};
                color: black;
            }}
        """)
        self.qualityFunctionsList.setFixedHeight(self.ui_styles[SIZES][SETTINGS_LISTS][HEIGHT])
        self.qualityCheckerLayout.addRow(label_functions, self.qualityFunctionsList)

        # Buttons for function management
        self.addNewQualityFunctionButton = QtWidgets.QPushButton("Add New Function", self.qualityCheckerGroup)
        self.addNewQualityFunctionButton.setStyleSheet(f"""
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][GREEN]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][GREEN_PRESSED]};
            }}
        """)
        self.qualityFunctionSettingsButton = QtWidgets.QPushButton("Function Settings", self.qualityCheckerGroup)
        self.qualityFunctionSettingsButton.setStyleSheet(f"""
            QPushButton {{
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][YELLOW]}; 
            color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][YELLOW_PRESSED]};
            }}
        """)
        self.removeQualityFunctionButton = QtWidgets.QPushButton("Remove Function", self.qualityCheckerGroup)
        self.removeQualityFunctionButton.setStyleSheet(f"""
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][RED]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][RED_PRESSED]};
            }}
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
            QPushButton {{
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border-bottom-left-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                border-bottom-right-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                border-right: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-left: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-bottom: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][BLUE]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][BLUE_PRESSED]};
            }}
        """)
        self.saveQualityCheckerButton.setFixedSize(self.ui_styles[SIZES][SETTINGS_SAVE_BUTTONS][WIDTH], self.ui_styles[SIZES][SETTINGS_SAVE_BUTTONS][HEIGHT])
        self.verticalLayout.addWidget(self.saveQualityCheckerButton, alignment=Qt.AlignBottom | Qt.AlignRight)


        # Annotator Section
        self.annotatorGroup = QtWidgets.QGroupBox("Annotator")
        self.annotatorGroup.setStyleSheet(f"""
            QGroupBox {{
                font-family: '{self.regular_font_family}';
                font-size: {self.ui_styles[FONTS][SETTING_GROUP_TITLE]}px; 
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

        label_current_selection = QLabel("Current Selection:")
        label_current_selection.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.currentSelectionComboBox = CustomComboBox(width=self.ui_styles[SIZES][SETTINGS_ANNOTATOR_COMBO][WIDTH], 
                                         height=self.ui_styles[SIZES][SETTINGS_ANNOTATOR_COMBO][HEIGHT], 
                                         border=self.ui_styles[BORDERS][DEFAULT_BORDER], 
                                         border_radius=self.ui_styles[BORDERS][DEFAULT_RADIUS], 
                                         font=self.ui_styles[FONTS][TEXT_FONT_SIZE],
                                         font_family=self.regular_font_family)
        self.annotatorLayout.addRow(label_current_selection, self.currentSelectionComboBox)

        # Annotator Options Widget Creation
        annotator_options_widget = QtWidgets.QWidget()
        annotator_options_layout = QtWidgets.QHBoxLayout(annotator_options_widget)
        annotator_options_widget.setLayout(annotator_options_layout)


        # color_assist_label = QtWidgets.QLabel("Enable Color-Assisted Mode", annotator_options_widget)
        # self.colorAssistCheckbox = QtWidgets.QCheckBox("", annotator_options_widget)  # Empty label for the checkbox itself

        self.colorAssistCheckbox = CustomCheckBox("Enable Color-Assisted Mode",
                                  width=self.ui_styles[SIZES][SETTINGS_COLOR_CHECKBOX][WIDTH], 
                                  height=self.ui_styles[SIZES][DEFAULT_CHECKBOX][HEIGHT],  
                                  border=self.ui_styles[BORDERS][DEFAULT_BORDER], 
                                  border_radious=self.ui_styles[BORDERS][DEFAULT_RADIUS], 
                                  font=self.ui_styles[FONTS][LABEL_FONT_SIZE],
                                  font_family=self.regular_font_family)

        #annotator_options_layout.addWidget(color_assist_label, alignment=Qt.AlignRight)
        annotator_options_layout.addWidget(self.colorAssistCheckbox, alignment=Qt.AlignLeft)

        annotator_options_layout.addStretch() 

        # Max Auto Label (SpinBox with Label)
        max_auto_label_label = QtWidgets.QLabel("Max auto label:", annotator_options_widget)
        max_auto_label_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.maxAutoLabelSpinBox = CustomSpinBox(width=self.ui_styles[SIZES][SPIN_BOX][WIDTH], 
                                         height=self.ui_styles[SIZES][GENERATION_SPINBOX][HEIGHT], 
                                         border=self.ui_styles[BORDERS][DEFAULT_BORDER], 
                                         border_radious=self.ui_styles[BORDERS][DEFAULT_RADIUS], 
                                         font=self.ui_styles[FONTS][TEXT_FONT_SIZE],
                                         font_family=self.regular_font_family)
        self.maxAutoLabelSpinBox.setRange(1, 1000)

        annotator_options_layout.addWidget(max_auto_label_label, alignment=Qt.AlignRight)
        annotator_options_layout.addWidget(self.maxAutoLabelSpinBox, alignment=Qt.AlignLeft)

        annotator_options_layout.addStretch() 

        # Checkbox Threshold (DoubleSpinBox with Label)
        checkbox_threshold_label = QtWidgets.QLabel("Checkbox threshold:", annotator_options_widget)
        checkbox_threshold_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.checkboxThresholdSpinBox = CustomDoubleSpinBox(width=self.ui_styles[SIZES][DOUBLE_SPIN_BOX][WIDTH], 
                                         height=self.ui_styles[SIZES][GENERATION_SPINBOX][HEIGHT], 
                                         border=self.ui_styles[BORDERS][DEFAULT_BORDER], 
                                         border_radious=self.ui_styles[BORDERS][DEFAULT_RADIUS], 
                                         font=self.ui_styles[FONTS][TEXT_FONT_SIZE],
                                         font_family=self.regular_font_family)
        self.checkboxThresholdSpinBox.setRange(0.0, 1.0)
        self.checkboxThresholdSpinBox.setSingleStep(0.01)

        # Add both label and spinbox to layout
        annotator_options_layout.addWidget(checkbox_threshold_label, alignment=Qt.AlignRight)
        annotator_options_layout.addWidget(self.checkboxThresholdSpinBox, alignment=Qt.AlignLeft)

        annotator_options_layout.addStretch() 

        # Default Color (ComboBox with Label)
        default_color_label = QtWidgets.QLabel("Default Color:", annotator_options_widget)
        default_color_label.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.defaultColorComboBox = CustomComboBox(width=self.ui_styles[SIZES][SETTINGS_COLOR_COMBO][WIDTH], 
                                         height=self.ui_styles[SIZES][GENERATION_SPINBOX][HEIGHT], 
                                         border=self.ui_styles[BORDERS][DEFAULT_BORDER], 
                                         border_radius=self.ui_styles[BORDERS][DEFAULT_RADIUS], 
                                         font=self.ui_styles[FONTS][TEXT_FONT_SIZE],
                                         font_family=self.regular_font_family)
        self.defaultColorComboBox.addItems(['red'] + [color for color in self.ui_styles[COLORS] if color != 'red']) # All colors in config + red at the front

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
                background-color: {self.ui_styles[COLORS][BACKGROUND]};
            }}
            QListWidget::item:selected {{
                background-color: {self.ui_styles[COLORS][BACKGROUND_PRESSED]};
                color: black;
            }}
        """)
        self.confidenceThresholdList.setFixedHeight(self.ui_styles[SIZES][SETTINGS_LISTS][HEIGHT])
        self.addConfidenceButton = QtWidgets.QPushButton("Add Threshold", self.annotatorGroup)
        self.addConfidenceButton.setStyleSheet(f"""
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][GREEN]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][GREEN_PRESSED]};
            }}
        """)
        self.editConfidenceButton = QtWidgets.QPushButton("Edit Threshold", self.annotatorGroup)
        self.editConfidenceButton.setStyleSheet(f"""
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][YELLOW]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][YELLOW_PRESSED]};
            }}
        """)
        self.removeConfidenceButton = QtWidgets.QPushButton("Remove Threshold", self.annotatorGroup)
        self.removeConfidenceButton.setStyleSheet(f"""
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][RED]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][RED_PRESSED]};
            }}
        """)
        
        label_confidence = QLabel("Confidence Thresholds:")
        label_confidence.setStyleSheet(f"""
            font-family: '{self.regular_font_family}';
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px;
        """)
        self.confidenceButtonLayout = QtWidgets.QHBoxLayout()
        self.confidenceButtonLayout.addWidget(self.addConfidenceButton)
        self.confidenceButtonLayout.addWidget(self.editConfidenceButton)
        self.confidenceButtonLayout.addWidget(self.removeConfidenceButton)
        self.annotatorLayout.addRow(label_confidence, self.confidenceThresholdList)
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
                background-color: {self.ui_styles[COLORS][BACKGROUND]};
            }}
            QListWidget::item:selected {{
                background-color: {self.ui_styles[COLORS][BACKGROUND_PRESSED]};
                color: black;
            }}
        """)
        self.annotatorModelsList.setFixedHeight(self.ui_styles[SIZES][SETTINGS_LISTS][HEIGHT])
        self.annotatorLayout.addRow(label_models, self.annotatorModelsList)

        # Buttons for model management
        self.addModelButton = QtWidgets.QPushButton("Add Model", self.annotatorGroup)
        self.addModelButton.setStyleSheet(f"""
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][GREEN]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][GREEN_PRESSED]};
            }}
        """)
        self.editModelButton = QtWidgets.QPushButton("Edit Model", self.annotatorGroup)
        self.editModelButton.setStyleSheet(f"""
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][YELLOW]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][YELLOW_PRESSED]};
            }}
        """)
        self.removeModelButton = QtWidgets.QPushButton("Remove Model", self.annotatorGroup)
        self.removeModelButton.setStyleSheet(f"""
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][RED]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][RED_PRESSED]};
            }}
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
            QPushButton {{
                font-size: {self.ui_styles[FONTS][BUTTON_FONT_SIZE]}px; 
                border-bottom-left-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                border-bottom-right-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px;
                border-right: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-left: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                border-bottom: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][BLUE]}; 
                color: {self.ui_styles[COLORS][BLACK]}
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][BLUE_PRESSED]};
            }}
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
            QPushButton {{
                border-radius: {self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]}px; 
                font-size: {self.ui_styles[FONTS][RETURN_BUTTON_FONT_SIZE]}px; 
                border: {self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
                background-color: {self.ui_styles[COLORS][ORANGE]}; 
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][ORANGE_PRESSED]};
            }}
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

    def getPosibleColorsMapping(self):
        return self.ui_styles[COLORS]