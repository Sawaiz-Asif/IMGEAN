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
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 780, 1600))  # Adjust scroll area size
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Layout to place all sections vertically within the scrollable area
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)

        # Dataset Section
        self.datasetGroup = QtWidgets.QGroupBox("Dataset", self.scrollAreaWidgetContents)
        self.datasetLayout = QtWidgets.QFormLayout(self.datasetGroup)

        # Description (currently the name)
        self.descriptionLineEdit = QtWidgets.QLineEdit(self.datasetGroup)
        self.datasetLayout.addRow("Description:", self.descriptionLineEdit)

        # Pickle File Path
        self.pickleFilePathLineEdit = QtWidgets.QLineEdit(self.datasetGroup)
        self.pickleFilePathBrowseButton = QtWidgets.QPushButton("Browse", self.datasetGroup)
        self.pickleFilePathLayout = QtWidgets.QHBoxLayout()
        self.pickleFilePathLayout.addWidget(self.pickleFilePathLineEdit)
        self.pickleFilePathLayout.addWidget(self.pickleFilePathBrowseButton)
        self.datasetLayout.addRow("Pickle File Path:", self.pickleFilePathLayout)

        # Labels List
        self.labelsListWidget = QtWidgets.QListWidget(self.datasetGroup)
        self.addLabelButton = QtWidgets.QPushButton("Add Label", self.datasetGroup)
        self.editLabelButton = QtWidgets.QPushButton("Edit Label", self.datasetGroup)
        self.removeLabelButton = QtWidgets.QPushButton("Remove Label", self.datasetGroup)
        self.labelsButtonLayout = QtWidgets.QHBoxLayout()
        self.labelsButtonLayout.addWidget(self.addLabelButton)
        self.labelsButtonLayout.addWidget(self.editLabelButton)
        self.labelsButtonLayout.addWidget(self.removeLabelButton)
        self.datasetLayout.addRow("Labels:", self.labelsListWidget)
        self.datasetLayout.addRow("", self.labelsButtonLayout)

        # Save Button
        self.saveDatasetButton = QtWidgets.QPushButton("Save Dataset Settings", self.datasetGroup)
        self.datasetLayout.addRow("", self.saveDatasetButton)

        self.verticalLayout.addWidget(self.datasetGroup)

        # Image Generator Section
        self.imageGenGroup = QtWidgets.QGroupBox("Image Generator", self.scrollAreaWidgetContents)
        self.imageGenLayout = QtWidgets.QFormLayout(self.imageGenGroup)

        # Models List
        self.imageModelsList = QtWidgets.QListWidget(self.imageGenGroup)
        self.imageGenLayout.addRow("Models:", self.imageModelsList)

        # Buttons for model management
        self.addNewImageModelButton = QtWidgets.QPushButton("Add New Model", self.imageGenGroup)
        self.removeImageModelButton = QtWidgets.QPushButton("Remove Model", self.imageGenGroup)
        self.imageModelSettingsButton = QtWidgets.QPushButton("Model Settings", self.imageGenGroup)
        self.imageModelButtonLayout = QtWidgets.QHBoxLayout()
        self.imageModelButtonLayout.addWidget(self.addNewImageModelButton)
        self.imageModelButtonLayout.addWidget(self.removeImageModelButton)
        self.imageModelButtonLayout.addWidget(self.imageModelSettingsButton)
        self.imageGenLayout.addRow("", self.imageModelButtonLayout)

        # Default Output Folder
        self.outputFolderLineEdit = QtWidgets.QLineEdit(self.imageGenGroup)
        self.outputFolderBrowseButton = QtWidgets.QPushButton("Browse", self.imageGenGroup)
        self.outputFolderLayout = QtWidgets.QHBoxLayout()
        self.outputFolderLayout.addWidget(self.outputFolderLineEdit)
        self.outputFolderLayout.addWidget(self.outputFolderBrowseButton)
        self.imageGenLayout.addRow("Default Output Folder:", self.outputFolderLayout)

        # Default ComfyUI IP
        self.comfyUiIpLineEdit = QtWidgets.QLineEdit(self.imageGenGroup)
        self.imageGenLayout.addRow("Default ComfyUI IP:", self.comfyUiIpLineEdit)

        # Save Button
        self.saveImageGenButton = QtWidgets.QPushButton("Save Image Generator Settings", self.imageGenGroup)
        self.imageGenLayout.addRow("", self.saveImageGenButton)

        self.verticalLayout.addWidget(self.imageGenGroup)


        # Quality Checker Section
        self.qualityCheckerGroup = QtWidgets.QGroupBox("Quality Checker", self.scrollAreaWidgetContents)
        self.qualityCheckerLayout = QtWidgets.QFormLayout(self.qualityCheckerGroup)

        # Functions List
        self.qualityFunctionsList = QtWidgets.QListWidget(self.qualityCheckerGroup)
        self.qualityCheckerLayout.addRow("Functions:", self.qualityFunctionsList)

        # Buttons for function management
        self.addNewQualityFunctionButton = QtWidgets.QPushButton("Add New Function", self.qualityCheckerGroup)
        self.removeQualityFunctionButton = QtWidgets.QPushButton("Remove Function", self.qualityCheckerGroup)
        self.qualityFunctionSettingsButton = QtWidgets.QPushButton("Function Settings", self.qualityCheckerGroup)
        self.qualityFunctionButtonLayout = QtWidgets.QHBoxLayout()
        self.qualityFunctionButtonLayout.addWidget(self.addNewQualityFunctionButton)
        self.qualityFunctionButtonLayout.addWidget(self.removeQualityFunctionButton)
        self.qualityFunctionButtonLayout.addWidget(self.qualityFunctionSettingsButton)
        self.qualityCheckerLayout.addRow("", self.qualityFunctionButtonLayout)

        # Save Button
        self.saveQualityCheckerButton = QtWidgets.QPushButton("Save Quality Checker Settings", self.qualityCheckerGroup)
        self.qualityCheckerLayout.addRow("", self.saveQualityCheckerButton)

        self.verticalLayout.addWidget(self.qualityCheckerGroup)

        # Annotator Section
        self.annotatorGroup = QtWidgets.QGroupBox("Annotator", self.scrollAreaWidgetContents)
        self.annotatorLayout = QtWidgets.QFormLayout(self.annotatorGroup)

        self.currentSelectionComboBox = QtWidgets.QComboBox(self.annotatorGroup)
        self.annotatorLayout.addRow("Current Selection:", self.currentSelectionComboBox)


        # Models List
        self.annotatorModelsList = QtWidgets.QListWidget(self.annotatorGroup)
        self.annotatorLayout.addRow("Models:", self.annotatorModelsList)

        # Buttons for model management
        self.addModelButton = QtWidgets.QPushButton("Add Model", self.annotatorGroup)
        self.editModelButton = QtWidgets.QPushButton("Edit Model", self.annotatorGroup)
        self.removeModelButton = QtWidgets.QPushButton("Remove Model", self.annotatorGroup)

        self.modelsButtonLayout = QtWidgets.QHBoxLayout()
        self.modelsButtonLayout.addWidget(self.addModelButton)
        self.modelsButtonLayout.addWidget(self.editModelButton)
        self.modelsButtonLayout.addWidget(self.removeModelButton)

        self.annotatorLayout.addRow("", self.modelsButtonLayout)

        # Enable Color-Assisted Mode
        self.colorAssistCheckbox = QtWidgets.QCheckBox("Enable Color-Assisted Mode", self.annotatorGroup)
        self.annotatorLayout.addRow(self.colorAssistCheckbox)

        # Max Auto Label
        self.maxAutoLabelSpinBox = QtWidgets.QSpinBox(self.annotatorGroup)
        self.maxAutoLabelSpinBox.setMinimum(1)
        self.maxAutoLabelSpinBox.setMaximum(1000)
        self.annotatorLayout.addRow("MAX_AUTO_LABEL:", self.maxAutoLabelSpinBox)

        # Checkbox Threshold
        self.checkboxThresholdSpinBox = QtWidgets.QDoubleSpinBox(self.annotatorGroup)
        self.checkboxThresholdSpinBox.setMinimum(0.0)
        self.checkboxThresholdSpinBox.setMaximum(1.0)
        self.checkboxThresholdSpinBox.setSingleStep(0.01)
        self.annotatorLayout.addRow("CHECKBOX_THRESHOLD:", self.checkboxThresholdSpinBox)

        # Default Color
        self.defaultColorComboBox = QtWidgets.QComboBox(self.annotatorGroup)
        self.defaultColorComboBox.addItems(["red", "green", "blue", "yellow", "orange", "purple"])
        self.annotatorLayout.addRow("Default Color:", self.defaultColorComboBox)

        # Confidence Thresholds List
        self.confidenceThresholdList = QtWidgets.QListWidget(self.annotatorGroup)
        self.addConfidenceButton = QtWidgets.QPushButton("Add Threshold", self.annotatorGroup)
        self.editConfidenceButton = QtWidgets.QPushButton("Edit Threshold", self.annotatorGroup)
        self.removeConfidenceButton = QtWidgets.QPushButton("Remove Threshold", self.annotatorGroup)
        self.confidenceButtonLayout = QtWidgets.QHBoxLayout()
        self.confidenceButtonLayout.addWidget(self.addConfidenceButton)
        self.confidenceButtonLayout.addWidget(self.editConfidenceButton)
        self.confidenceButtonLayout.addWidget(self.removeConfidenceButton)
        self.annotatorLayout.addRow("Confidence Thresholds:", self.confidenceThresholdList)
        self.annotatorLayout.addRow("", self.confidenceButtonLayout)


        # Save Button
        self.saveAnnotatorButton = QtWidgets.QPushButton("Save Annotator Settings", self.annotatorGroup)
        self.annotatorLayout.addRow("", self.saveAnnotatorButton)

        # Add Annotator Section to Main Layout
        self.verticalLayout.addWidget(self.annotatorGroup)

        SettingsWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "Settings & Setup"))