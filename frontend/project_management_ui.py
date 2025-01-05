from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QWidget
from PyQt5.QtCore import pyqtSignal, QObject
from ui_styles_constants import *
from config_constants import *

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
        self.topBar = QHBoxLayout()
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
        self.returnButton = QPushButton("Return")
        self.returnButton.setFixedSize(
            self.ui_styles[SIZES][RETURN_BUTTON][WIDTH],
            self.ui_styles[SIZES][RETURN_BUTTON][HEIGHT]
        )
        self.returnButton.setStyleSheet(f"""
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
        
        self.topBar.addWidget(self.returnButton)
        self.topBar.addWidget(self.addProjectButton)
        
        self.verticalLayout.addLayout(self.topBar)

        # Scroll area for projects
        self.scrollArea = QScrollArea(main_widget)
        self.scrollArea.setWidgetResizable(True)  # Make sure scroll area resizes dynamically
        self.scrollContent = QWidget()
        self.scrollContentLayout = QVBoxLayout(self.scrollContent)
        self.scrollContent.setLayout(self.scrollContentLayout)  # Set layout for scroll content
        self.scrollArea.setWidget(self.scrollContent)  # Attach scroll content to scroll area
        self.verticalLayout.addWidget(self.scrollArea)  # Add scroll area to main layout

        ProjectManagement.setCentralWidget(main_widget)

        # self.retranslateUi(ProjectManagement)
        QtCore.QMetaObject.connectSlotsByName(ProjectManagement)

    # def retranslateUi(self, ProjectManagement):
    #     _translate = QtCore.QCoreApplication.translate
    #     ProjectManagement.setWindowTitle(_translate("ProjectManagement", "Project Management"))
