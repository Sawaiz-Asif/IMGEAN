from PyQt5 import QtWidgets
from frontend.annotate_img_ui import Ui_AnnotateImg  # Import the UI

class AnnotateImg(QtWidgets.QWidget, Ui_AnnotateImg):
    def __init__(self, stacked_widget):
        super(AnnotateImg, self).__init__()
        self.setupUi(self)
        self.stacked_widget = stacked_widget  # Reference to the QStackedWidget for navigation

        # Connect the buttons to their respective methods
        self.returnButton.clicked.connect(self.on_return_click)
        self.prevButton.clicked.connect(self.on_prev_click)
        self.discardButton.clicked.connect(self.on_discard_click)
        self.nextButton.clicked.connect(self.on_next_click)
        self.autoLabelImgButton.clicked.connect(self.on_auto_label_img_click)
        self.autoLabelAllButton.clicked.connect(self.on_auto_label_all_click)
        self.confirmLabelButton.clicked.connect(self.on_confirm_label_click)
        self.openImageGridButton.clicked.connect(self.on_open_image_grid_click)
        self.imageGridOverlay.itemClicked.connect(self.on_image_selected)

        # Track the current image index for navigation
        self.currentImageIndex = 0

    def on_return_click(self):
        # Return to the main screen
        self.stacked_widget.setCurrentIndex(0)

    def on_prev_click(self):
        # Go to the previous image
        self.currentImageIndex = max(0, self.currentImageIndex - 1)
        self.update_image_display()

    def on_discard_click(self):
        # Discard the current image
        print(f"Image {self.currentImageIndex + 1} discarded")

    def on_next_click(self):
        # Go to the next image
        self.currentImageIndex = min(self.imageGridOverlay.count() - 1, self.currentImageIndex + 1)
        self.update_image_display()

    def on_auto_label_img_click(self):
        # Auto-label the current image
        print(f"Auto-labeling image {self.currentImageIndex + 1}")

    def on_auto_label_all_click(self):
        # Auto-label all images
        print("Auto-labeling all images")

    def on_confirm_label_click(self):
        # Confirm the selected labels
        print("Labels confirmed")

    def on_open_image_grid_click(self):
        # Show the image grid overlay
        self.imageGridOverlay.setHidden(False)
        self.imageLabel.setHidden(True)  # Hide the image display

    def on_image_selected(self, item):
        # When an image is selected from the grid, hide the grid and show the selected image
        self.currentImageIndex = self.imageGridOverlay.row(item)
        self.update_image_display()
        self.imageGridOverlay.setHidden(True)
        self.imageLabel.setHidden(False)

    def update_image_display(self):
        # Update the image display based on the current image index
        self.imageLabel.setText(f"Image {self.currentImageIndex + 1}")