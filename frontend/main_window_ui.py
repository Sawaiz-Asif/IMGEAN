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

class Ui_MainWindow(object):
    def __init__(self, ui_styles):
        self.ui_styles = ui_styles

    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("IMGEAN")

        window_height = self.ui_styles[WINDOW_HEIGHT]
        MainWindow.resize(int(window_height*16/9), window_height)
        MainWindow.setStyleSheet(f"background-color: {self.ui_styles[COLORS][BACKGROUND]};")

        # Central widget
        self.central_widget = QWidget()

        # Create a QStackedWidget to hold multiple screens
        self.stackedWidget = QtWidgets.QStackedWidget(self.central_widget)
        self.stackedWidget.setObjectName("stackedWidget")
        MainWindow.setCentralWidget(self.stackedWidget)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "IMGEAN"))