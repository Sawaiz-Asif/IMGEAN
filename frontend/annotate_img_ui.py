from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AnnotateImg(object):
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
        self.labelList.setGeometry(QtCore.QRect(500, 160, 260, 200))
        for i in range(1, 13):
            item = QtWidgets.QListWidgetItem(f"Label {i}")
            self.labelList.addItem(item)

        # Confirm labeling button
        self.confirmLabelButton = QtWidgets.QPushButton(AnnotateImg)
        self.confirmLabelButton.setGeometry(QtCore.QRect(560, 400, 200, 40))
        self.confirmLabelButton.setText("Confirm labeling")

        # Long vertical button on the left (opens image grid)
        self.openImageGridButton = QtWidgets.QPushButton(AnnotateImg)
        self.openImageGridButton.setGeometry(QtCore.QRect(20, 150, 60, 300))
        self.openImageGridButton.setText("Images")

        # Image grid overlay (initially hidden)
        # Now spans the left half of the screen (including image area and below)
        self.imageGridOverlay = QtWidgets.QListWidget(AnnotateImg)
        self.imageGridOverlay.setGeometry(QtCore.QRect(20, 100, 380, 380))  # Covering left half of the screen
        self.imageGridOverlay.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.imageGridOverlay.setHidden(True)  # Initially hidden
        for i in range(1, 25):
            item = QtWidgets.QListWidgetItem(f"Img {i}")
            self.imageGridOverlay.addItem(item)

    def retranslateUi(self, AnnotateImg):
        _translate = QtCore.QCoreApplication.translate
        AnnotateImg.setWindowTitle(_translate("AnnotateImg", "Annotate Images"))