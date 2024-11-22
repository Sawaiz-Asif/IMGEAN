from PyQt5 import QtWidgets, QtGui, QtCore
from frontend.main_screen_ui import Ui_MainScreen  # Import the UI
import os
import backend.file_utils as fu
from backend.annotation_manager.automatic_labeling import open_model,get_predictions_with_confidence

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget

class MainScreen(QtWidgets.QWidget):
    def __init__(self, main_window, ui_styles):
        super(MainScreen, self).__init__()
        self.ui = Ui_MainScreen(ui_styles)  # Initialize the UI  # Reference to the QStackedWidget for navigation
        self.ui.setupUi(self)

        self.main_window = main_window

        self.ui.btn_generate.clicked.connect(lambda: main_window.change_current_screen(1))
        self.ui.btn_quality.clicked.connect(lambda: main_window.change_current_screen(2))
        self.ui.btn_annotate.clicked.connect(lambda: main_window.change_current_screen(3))
        self.ui.btn_settings.clicked.connect(lambda: main_window.change_current_screen(4))