from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        # Create a central widget that will hold the QStackedWidget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

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

        self.label = QtWidgets.QLabel(self.mainScreen)
        self.label.setGeometry(QtCore.QRect(210, 30, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setText("IMGEAN")

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