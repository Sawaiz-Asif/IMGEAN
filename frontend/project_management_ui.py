from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QWidget
from PyQt5.QtCore import pyqtSignal, QObject
from ui_styles_constants import *
from config_constants import *

from PyQt5.QtWidgets import (
    QPushButton, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase

class Ui_ProjectManagement(object):
    def __init__(self, config, ui_styles):
        self.config = config
        self.ui_styles = ui_styles
        
    def setupUi(self, ProjectManagement):
        ProjectManagement.setObjectName("ProjectManagement")
        ProjectManagement.resize(800, 600)

        # Main layout
        main_widget = QWidget(ProjectManagement)
        self.verticalLayout = QVBoxLayout(main_widget)

        # Top buttons
        self.setup_top_section()

        # Scroll area for projects
        self.scrollArea = QScrollArea(main_widget)
        self.scrollArea.setWidgetResizable(True)  # Make sure scroll area resizes dynamically
        self.scrollContent = QWidget()
        self.scrollContentLayout = QVBoxLayout(self.scrollContent)
        self.scrollContent.setLayout(self.scrollContentLayout)  # Set layout for scroll content
        self.scrollArea.setWidget(self.scrollContent)  # Attach scroll content to scroll area
        self.verticalLayout.addWidget(self.scrollArea)  # Add scroll area to main layout

        self.addProjectButton = QPushButton("Add New Project")
        self.addProjectButton.setStyleSheet(f"""
            QPushButton {{
            border-radius: {self.ui_styles[BORDERS][DEFAULT_RADIUS]}px; 
            font-size: {self.ui_styles[FONTS][LABEL_FONT_SIZE]}px; 
            border: {self.ui_styles[BORDERS][DEFAULT_BORDER]}px {self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]};
            background-color: {self.ui_styles[COLORS][BLUE]}; 
            }}
            QPushButton:pressed {{
                background-color: {self.ui_styles[COLORS][BLUE_PRESSED]};
            }}
        """)

        self.verticalLayout.addWidget(self.addProjectButton)
        self.verticalLayout.setContentsMargins(self.ui_styles[PADDINGS][MIN_SIDES], 5, self.ui_styles[PADDINGS][MIN_SIDES], self.ui_styles[PADDINGS][MIN_SIDES])
        ProjectManagement.setCentralWidget(main_widget)

        # self.retranslateUi(ProjectManagement)
        QtCore.QMetaObject.connectSlotsByName(ProjectManagement)

    # def retranslateUi(self, ProjectManagement):
    #     _translate = QtCore.QCoreApplication.translate
    #     ProjectManagement.setWindowTitle(_translate("ProjectManagement", "Project Management"))

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
            title = QLabel("Project management")
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
            self.verticalLayout.addLayout(self.top_section_layout)