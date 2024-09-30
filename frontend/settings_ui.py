from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(SettingsWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Title Section (outside scrollable area)
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(200, 10, 400, 40))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setText("Settings & Setup")

        # Return Button (outside scrollable area)
        self.returnButton = QtWidgets.QPushButton(self.centralwidget)
        self.returnButton.setGeometry(QtCore.QRect(20, 10, 100, 30))
        self.returnButton.setText("Return")

        # Create a scrollable area for the main content
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 60, 800, 540))  # Adjust to fit below the title and return button
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 780, 1200))  # Adjust scroll area size
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Layout to place all sections vertically within the scrollable area
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)

        # Dataset Section
        self.datasetGroup = QtWidgets.QGroupBox("Dataset", self.scrollAreaWidgetContents)
        self.datasetLayout = QtWidgets.QFormLayout(self.datasetGroup)
        self.basePath = QtWidgets.QLineEdit(self.datasetGroup)
        self.datasetLayout.addRow("Base path:", self.basePath)
        self.testValCheckbox = QtWidgets.QCheckBox("Test/Val have different paths", self.datasetGroup)
        self.datasetLayout.addRow(self.testValCheckbox)
        self.trainPath = QtWidgets.QLineEdit(self.datasetGroup)
        self.valPath = QtWidgets.QLineEdit(self.datasetGroup)
        self.datasetLayout.addRow("Train:", self.trainPath)
        self.datasetLayout.addRow("Val:", self.valPath)
        self.taskDropdown = QtWidgets.QComboBox(self.datasetGroup)
        self.taskDropdown.addItems(["Classification", "Object Detection", "Segmentation"])
        self.datasetLayout.addRow("Task:", self.taskDropdown)
        self.classesDropdown = QtWidgets.QComboBox(self.datasetGroup)
        self.classesDropdown.addItems(["3", "4", "5"])
        self.datasetLayout.addRow("Classes:", self.classesDropdown)
        self.addClassesButton = QtWidgets.QPushButton("Add more classes", self.datasetGroup)
        self.datasetLayout.addRow(self.addClassesButton)
        self.annotationFormat = QtWidgets.QLineEdit(self.datasetGroup)
        self.datasetLayout.addRow("Annotation format:", self.annotationFormat)
        self.verticalLayout.addWidget(self.datasetGroup)

        # Annotator Section
        self.annotatorGroup = QtWidgets.QGroupBox("Annotator", self.scrollAreaWidgetContents)
        self.annotatorLayout = QtWidgets.QVBoxLayout(self.annotatorGroup)
        self.modelsList = QtWidgets.QListWidget(self.annotatorGroup)
        self.modelsList.addItems(["Model 1", "Model 2", "Model 3"])
        self.annotatorLayout.addWidget(self.modelsList)
        self.removeModelButton = QtWidgets.QPushButton("Remove model", self.annotatorGroup)
        self.modelSettingsButton = QtWidgets.QPushButton("Model settings", self.annotatorGroup)
        self.addNewModelButton = QtWidgets.QPushButton("Add new model", self.annotatorGroup)
        self.annotatorButtonLayout = QtWidgets.QHBoxLayout()
        self.annotatorButtonLayout.addWidget(self.removeModelButton)
        self.annotatorButtonLayout.addWidget(self.modelSettingsButton)
        self.annotatorButtonLayout.addWidget(self.addNewModelButton)
        self.annotatorLayout.addLayout(self.annotatorButtonLayout)
        self.colorAssistCheckbox = QtWidgets.QCheckBox("Use color-assisted mode", self.annotatorGroup)
        self.annotatorLayout.addWidget(self.colorAssistCheckbox)
        self.verticalLayout.addWidget(self.annotatorGroup)

        # Image Generator Section
        self.imageGenGroup = QtWidgets.QGroupBox("Image Generator", self.scrollAreaWidgetContents)
        self.imageGenLayout = QtWidgets.QVBoxLayout(self.imageGenGroup)
        self.imageModelsList = QtWidgets.QListWidget(self.imageGenGroup)
        self.imageModelsList.addItems(["Stable Diffusion 1", "Stable Diffusion 2", "Stable Diffusion 3"])
        self.imageGenLayout.addWidget(self.imageModelsList)
        self.removeImageModelButton = QtWidgets.QPushButton("Remove model", self.imageGenGroup)
        self.imageModelSettingsButton = QtWidgets.QPushButton("Model settings", self.imageGenGroup)
        self.addNewImageModelButton = QtWidgets.QPushButton("Add new model", self.imageGenGroup)
        self.imageModelButtonLayout = QtWidgets.QHBoxLayout()
        self.imageModelButtonLayout.addWidget(self.removeImageModelButton)
        self.imageModelButtonLayout.addWidget(self.imageModelSettingsButton)
        self.imageModelButtonLayout.addWidget(self.addNewImageModelButton)
        self.imageGenLayout.addLayout(self.imageModelButtonLayout)
        self.verticalLayout.addWidget(self.imageGenGroup)

        # Quality Checker Section
        self.qualityCheckerGroup = QtWidgets.QGroupBox("Quality Checker", self.scrollAreaWidgetContents)
        self.qualityCheckerLayout = QtWidgets.QVBoxLayout(self.qualityCheckerGroup)
        self.qualityModelsList = QtWidgets.QListWidget(self.qualityCheckerGroup)
        self.qualityModelsList.addItems(["B&W", "Pose Estimator", "CustomModel3"])
        self.qualityCheckerLayout.addWidget(self.qualityModelsList)
        self.removeQualityModelButton = QtWidgets.QPushButton("Remove model", self.qualityCheckerGroup)
        self.qualityModelSettingsButton = QtWidgets.QPushButton("Model settings", self.qualityCheckerGroup)
        self.addNewQualityModelButton = QtWidgets.QPushButton("Add new model", self.qualityCheckerGroup)
        self.qualityModelButtonLayout = QtWidgets.QHBoxLayout()
        self.qualityModelButtonLayout.addWidget(self.removeQualityModelButton)
        self.qualityModelButtonLayout.addWidget(self.qualityModelSettingsButton)
        self.qualityModelButtonLayout.addWidget(self.addNewQualityModelButton)
        self.qualityCheckerLayout.addLayout(self.qualityModelButtonLayout)
        self.verticalLayout.addWidget(self.qualityCheckerGroup)

        SettingsWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "Settings & Setup"))