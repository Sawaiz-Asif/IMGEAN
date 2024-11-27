from PyQt5 import QtCore, QtGui, QtWidgets
import backend.annotation_manager.dataset_utils as du

DATASET = 'DATASET'
PATH = 'PATH'

class Ui_AnnotateImg(object):
    def __init__(self, config):
        self.config = config
        self.dataset_manager = du.DatasetManager(config[DATASET][PATH], config)

    def setupUi(self, AnnotateImg):
        AnnotateImg.setObjectName("AnnotateImg")
        AnnotateImg.resize(800, 600)

        # Return button
        self.returnButton = QtWidgets.QPushButton(AnnotateImg)
        self.returnButton.setGeometry(QtCore.QRect(20, 20, 100, 40))
        self.returnButton.setText("Return")

        # Image Placeholder (This will display the image to annotate)
        self.imageLabel = QtWidgets.QLabel(AnnotateImg)
        self.imageLabel.setGeometry(QtCore.QRect(100, 100, 300, 300))
        self.imageLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel.setText("Image Placeholder")

        # Navigation buttons below the image
        self.prevButton = QtWidgets.QPushButton(AnnotateImg)
        self.prevButton.setGeometry(QtCore.QRect(100, 420, 80, 40))
        self.prevButton.setText("Prev")

        self.discardButton = QtWidgets.QPushButton(AnnotateImg)
        self.discardButton.setGeometry(QtCore.QRect(200, 420, 80, 40))
        self.discardButton.setText("Discard")

        self.nextButton = QtWidgets.QPushButton(AnnotateImg)
        self.nextButton.setGeometry(QtCore.QRect(300, 420, 80, 40))
        self.nextButton.setText("Next")

        # Auto-label buttons (on the right side)
        self.autoLabelImgButton = QtWidgets.QPushButton(AnnotateImg)
        self.autoLabelImgButton.setGeometry(QtCore.QRect(500, 100, 120, 40))
        self.autoLabelImgButton.setText("Auto-label img")

        self.autoLabelAllButton = QtWidgets.QPushButton(AnnotateImg)
        self.autoLabelAllButton.setGeometry(QtCore.QRect(640, 100, 120, 40))
        self.autoLabelAllButton.setText("Auto-label all")

        # List of checkboxes (labels) below auto-label buttons
        self.labelList = QtWidgets.QListWidget(AnnotateImg)
        _, list_labels = self.dataset_manager.get_dataset_labels()  # Retrieve the actual labels
        self.labelList.setGeometry(QtCore.QRect(500, 160, 260, 200))

        # Iterate through the actual labels and create a checkbox for each one
        for label in list_labels:
            # Create a widget to hold both the checkbox and the label name
            widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(widget)
            
            checkbox = QtWidgets.QCheckBox()
            label_widget = QtWidgets.QLabel(label)
            
            layout.addWidget(checkbox)
            layout.addWidget(label_widget)
            
            layout.setAlignment(QtCore.Qt.AlignLeft)  # Align items to the left
            layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for a compact look
            
            # Add the custom widget (with checkbox and label) to the list
            item = QtWidgets.QListWidgetItem()
            self.labelList.addItem(item)
            self.labelList.setItemWidget(item, widget)


        # Confirm labeling button
        self.confirmLabelButton = QtWidgets.QPushButton(AnnotateImg)
        self.confirmLabelButton.setGeometry(QtCore.QRect(560, 400, 200, 40))
        self.confirmLabelButton.setText("Confirm labeling")

        # Long vertical button on the left (opens image grid)
        self.openImageGridButton = QtWidgets.QPushButton(AnnotateImg)
        self.openImageGridButton.setGeometry(QtCore.QRect(20, 150, 60, 300))
        self.openImageGridButton.setText("Images")

        # Image grid overlay (initially hidden)
        scroll_area = QtWidgets.QScrollArea(AnnotateImg)
        scroll_area.setGeometry(QtCore.QRect(20, 100, 380, 380))
        scroll_area.setWidgetResizable(True)

        # Scroll widget to contain the grid layout
        scroll_widget = QtWidgets.QWidget()

        # Create a layout to contain both the button and the image grid
        layout = QtWidgets.QVBoxLayout(scroll_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins to push the button closer to the top
        layout.setSpacing(0)  # Remove spacing between the button and the grid

        # Button to import dataset images (placed at the top left inside the scroll area)
        self.importButton = QtWidgets.QPushButton("Import dataset images", scroll_widget)
        layout.addWidget(self.importButton, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # Grid layout for images
        self.imageGridLayout = QtWidgets.QGridLayout()
        self.imageGridLayout.setContentsMargins(0, 0, 0, 0)  # No margins for grid layout
        layout.addLayout(self.imageGridLayout)

        scroll_area.setWidget(scroll_widget)
        scroll_area.setHidden(True)  # Initially hidden

        self.imageGridOverlay = scroll_area





        """ self.imageGridOverlay = QtWidgets.QListWidget(AnnotateImg)
        self.imageGridOverlay.setGeometry(QtCore.QRect(20, 100, 380, 380))  # Covering left half of the screen
        self.imageGridOverlay.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.imageGridOverlay.setHidden(True)  # Initially hidden """
        """ for i in range(1, 25):
            item = QtWidgets.QListWidgetItem(f"Img {i}")
            self.imageGridOverlay.addItem(item) """

    def retranslateUi(self, AnnotateImg):
        _translate = QtCore.QCoreApplication.translate
        AnnotateImg.setWindowTitle(_translate("AnnotateImg", "Annotate Images"))
        