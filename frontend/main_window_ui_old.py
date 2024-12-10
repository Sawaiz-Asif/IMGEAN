from PyQt5 import QtCore, QtWidgets
from ui_styles_constants import *


from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout
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
        central_widget = QWidget(MainWindow)
        self.centralwidget = QWidget(central_widget)
        self.centralwidget.setObjectName("centralwidget")

        # Layouts
        main_layout = QVBoxLayout(central_widget)
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



        # Create a QStackedWidget to hold multiple screens
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.stackedWidget.setObjectName("stackedWidget")

        # Create the first screen (Main Window)
        self.mainScreen = QtWidgets.QWidget()
        self.mainScreen.setObjectName("mainScreen")

        # Add buttons and labels
        self.pushButton = QtWidgets.QPushButton(self.mainScreen)
        self.pushButton.setGeometry(QtCore.QRect(90, 190, 170, 60))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Generate Images")

        self.pushButton_2 = QtWidgets.QPushButton(self.mainScreen)
        self.pushButton_2.setGeometry(QtCore.QRect(360, 190, 170, 60))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Check Image Quality")

        self.pushButton_3 = QtWidgets.QPushButton(self.mainScreen)
        self.pushButton_3.setGeometry(QtCore.QRect(90, 270, 170, 60))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("Annotate Images")

        self.pushButton_4 = QtWidgets.QPushButton(self.mainScreen)
        self.pushButton_4.setGeometry(QtCore.QRect(360, 270, 170, 60))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setText("Settings & Setup")

        self.label_2 = QtWidgets.QLabel(self.mainScreen)
        self.label_2.setGeometry(QtCore.QRect(90, 80, 441, 61))
        self.label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("¡Tool for augmenting datasets! ¡An Image Generator & Annotator!")

        # Add the first screen to the stacked widget
        self.stackedWidget.addWidget(self.mainScreen)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "IMGEAN"))