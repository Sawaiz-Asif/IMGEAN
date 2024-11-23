from PyQt5 import QtCore, QtGui, QtWidgets
from backend.config_reader import read_config
from ui_styles_constants import *


import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase

UI_STYLES = 'UI_STYLES'
WINDOW_HEIGHT = 'window_height'
COLORS = 'colors'
BACKGROUND = 'background'

class Ui_MainScreen(object):
    def __init__(self, ui_styles):
        self.ui_styles = ui_styles

    def setupUi(self, MainScreen):
        MainScreen.setObjectName("MainScreen")

        main_widget = QWidget()

        # Layouts
        main_layout = QVBoxLayout(main_widget)
        button_layout = QGridLayout()
        button_layout.setHorizontalSpacing(self.ui_styles[PADDINGS][MAIN_BUTTONS_HORIZONTAL])
        button_layout.setVerticalSpacing(self.ui_styles[PADDINGS][MAIN_BUTTONS_VERTICAL])
        lower_layout = QHBoxLayout()

        # Title
        title = QLabel("IMGEAN")
        bold_font_id = QFontDatabase.addApplicationFont(self.ui_styles[FONTS][BOLD_FONT_FILE])
        bold_font_family = QFontDatabase.applicationFontFamilies(bold_font_id)[0]
        title.setStyleSheet(f"""
            font-family: '{bold_font_family}';
            font-size: {self.ui_styles[FONTS][TITLE_FONT_SIZE]}px;
            font-weight: bold;
            text-align: center;
        """)
        title.setAlignment(Qt.AlignCenter)

        # Subtitle
        subtitle = QLabel("¡Tool for augmenting datasets! ¡An Image Generator & Annotator!")
        regular_font_id = QFontDatabase.addApplicationFont(self.ui_styles[FONTS][REGULAR_FONT_FILE])
        regular_font_family = QFontDatabase.applicationFontFamilies(regular_font_id)[0]
        subtitle.setStyleSheet(f"""
            font-family: '{regular_font_family}';
            font-size: {self.ui_styles[FONTS][TITLE_FONT_SIZE]//3}px;
            text-align: center;
        """)
        subtitle.setAlignment(Qt.AlignCenter)

        # Buttons
        main_button_width = self.ui_styles[SIZES][MAIN_BUTTONS][WIDTH]
        main_button_height = self.ui_styles[SIZES][MAIN_BUTTONS][HEIGHT]
        main_button_font_size = self.ui_styles[FONTS][BUTTON_FONT_SIZE]
        main_button_border = self.ui_styles[BORDERS][MAIN_BUTTON_BORDER]
        main_button_style = self.ui_styles[BORDERS][MAIN_BUTTON_STYLE]
        main_button_radius = self.ui_styles[BORDERS][MAIN_BUTTON_RADIUS]

        base_button_stylesheet = f"""
            border-radius: {main_button_radius}px; 
            font-size: {main_button_font_size}px; 
            border: {main_button_border}px {main_button_style};
        """

        btn_generate = QPushButton("Generate Images")
        btn_generate.setFixedSize(main_button_width, main_button_height)
        btn_generate.setStyleSheet(base_button_stylesheet + f"""
            background-color: {self.ui_styles[COLORS][YELLOW]}; 
        """)
        self.btn_generate = btn_generate

        btn_quality = QPushButton("Check Image Quality")
        btn_quality.setFixedSize(main_button_width, main_button_height)
        btn_quality.setStyleSheet(base_button_stylesheet + f"""
            background-color: {self.ui_styles[COLORS][ORANGE]}; 
        """)
        self.btn_quality = btn_quality

        btn_annotate = QPushButton("Annotate Images")
        btn_annotate.setFixedSize(main_button_width, main_button_height)
        btn_annotate.setStyleSheet(base_button_stylesheet + f"""
            background-color: {self.ui_styles[COLORS][GREEN]}; 
        """)
        self.btn_annotate = btn_annotate

        btn_settings = QPushButton("Settings and Setup")
        btn_settings.setFixedSize(main_button_width, main_button_height)
        btn_settings.setStyleSheet(base_button_stylesheet + f"""
            background-color: {self.ui_styles[COLORS][PURPLE]}; 
        """)
        self.btn_settings = btn_settings

        # Adding buttons to button layout
        button_layout.addWidget(btn_generate, 0, 0, alignment=Qt.AlignRight)
        button_layout.addWidget(btn_quality, 0, 1, alignment=Qt.AlignLeft)
        button_layout.addWidget(btn_annotate, 1, 0, alignment=Qt.AlignRight)
        button_layout.addWidget(btn_settings, 1, 1, alignment=Qt.AlignLeft)

        # Current project info and button
        project_label = QLabel('Currently working on: "My custom project 2.0":')
        project_label.setStyleSheet(f"""
            font-family: '{regular_font_family}';
            font-size: {self.ui_styles[FONTS][TITLE_FONT_SIZE]//4}px;
            text-align: center;
        """)
        change_project_btn = QPushButton("Change project")
        change_project_btn.setFixedSize(2*main_button_width//3, main_button_height//2)
        change_project_btn.setStyleSheet(f"""
            background-color: {self.ui_styles[COLORS][BLUE]}; 
            border-radius: {main_button_radius}px; 
            font-size: {self.ui_styles[FONTS][TITLE_FONT_SIZE]//4}px; 
            border: {main_button_border}px {main_button_style};
        """)
        self.change_project_btn = change_project_btn

        # Adding project info and button to lower layout
        lower_layout.addWidget(project_label)
        lower_layout.addSpacing(10)
        lower_layout.addWidget(change_project_btn)
        lower_layout.setAlignment(Qt.AlignCenter)

        # Assembling the main layout
        main_layout.addSpacing(self.ui_styles[PADDINGS][BEFORE_TITLE])
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addSpacing(self.ui_styles[PADDINGS][AFTER_TITLE])
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        main_layout.addLayout(lower_layout)
        main_layout.addSpacing(self.ui_styles[PADDINGS][SCREEN_ENDING])
        
        MainScreen.setLayout(main_layout)