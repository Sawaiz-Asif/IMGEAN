from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QWidget
from PyQt5.QtCore import pyqtSignal, QObject

class Ui_ProjectManagement(object):
    def setupUi(self, ProjectManagement):
        ProjectManagement.setObjectName("ProjectManagement")
        ProjectManagement.resize(800, 600)

        # Main layout
        main_widget = QWidget(ProjectManagement)
        self.verticalLayout = QVBoxLayout(main_widget)

        # Top buttons
        self.topBar = QHBoxLayout()
        self.addProjectButton = QPushButton("Add New Project")
        self.returnButton = QPushButton("Return to Main")
        self.topBar.addWidget(self.addProjectButton)
        self.topBar.addWidget(self.returnButton)
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
