from PyQt5 import QtWidgets, QtGui, QtCore
from frontend.annotate_img_ui import Ui_AnnotateImg  # Import the UI
import os
import backend.file_utils as fu

# Custom QLabel to handle image clicks
class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()  # Custom signal to emit when clicked

    def mousePressEvent(self, event):
        self.clicked.emit()  # Emit signal when label is clicked
        super().mousePressEvent(event)

class AnnotateImg(QtWidgets.QWidget):
    def __init__(self, stacked_widget, config, images_labeling_dir="data"):
        super(AnnotateImg, self).__init__()
        self.ui = Ui_AnnotateImg()  # Initialize the UI
        self.ui.setupUi(self)
        self.stacked_widget = stacked_widget  # Reference to the QStackedWidget for navigation

        self.config = config

        self.images_labeling_dir = images_labeling_dir

        # Connect the buttons to their respective methods
        self.ui.returnButton.clicked.connect(self.on_return_click)
        self.ui.prevButton.clicked.connect(self.on_prev_click)
        self.ui.discardButton.clicked.connect(self.on_discard_click)
        self.ui.nextButton.clicked.connect(self.on_next_click)
        self.ui.autoLabelImgButton.clicked.connect(self.on_auto_label_img_click)
        self.ui.autoLabelAllButton.clicked.connect(self.on_auto_label_all_click)
        self.ui.confirmLabelButton.clicked.connect(self.on_confirm_label_click)
        self.ui.openImageGridButton.clicked.connect(self.on_open_image_grid_click)
        #self.ui.imageGridLayout.itemClicked.connect(self.on_image_selected)

        # Track the current image index for navigation
        self.current_image_index = 0
        self.images_to_label =  self.get_labeling_images()

        self.update_image_display()

    def on_return_click(self):
        # Return to the main screen

        self.ui.imageGridOverlay.setHidden(True)
        self.ui.imageLabel.setHidden(False)

        self.stacked_widget.setCurrentIndex(0)

    def on_prev_click(self):
        # Go to the previous image
        if self.current_image_index > 0:
                self.current_image_index -= 1
        self.update_image_display()

    def on_discard_click(self):
        # Discard the current image
        discarded_image = self.images_to_label.pop(self.current_image_index)
        if (self.current_image_index>0):
            self.current_image_index -= 1
        fu.move_labeling_discard(self.config, discarded_image)
        self.populate_image_grid(self.ui.imageGridLayout, self.images_to_label)
        self.update_image_display()

    def on_next_click(self):
        # Go to the next image
        if self.current_image_index < len(self.images_to_label) - 1:
                self.current_image_index += 1
        self.update_image_display()

    def on_auto_label_img_click(self):
        # Auto-label the current image
        print(f"Auto-labeling image {self.current_image_index + 1}")

    def on_auto_label_all_click(self):
        # Auto-label all images
        print("Auto-labeling all images")

    def on_confirm_label_click(self):
        # Confirm the selected labels
        print("Labels confirmed")

    def on_open_image_grid_click(self):
        # Show the image grid overlay
        self.ui.imageGridOverlay.setHidden(False)

        self.populate_image_grid(self.ui.imageGridLayout, self.images_to_label)

        self.ui.imageLabel.setHidden(True)  # Hide the image display

    def update_image_display(self):
        # Update the image display based on the current image index
        self.ui.imageLabel.setText(f"Image {self.current_image_index + 1}")
        if self.images_to_label:
            image_name = self.images_to_label[self.current_image_index]
            image_path = os.path.join(self.images_labeling_dir, image_name)
            pixmap = QtGui.QPixmap(image_path)
            self.ui.imageLabel.setPixmap(
                pixmap.scaled(self.ui.imageLabel.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            )
        else:
            self.ui.imageLabel.setText("No images to display")  # Display message if no images

    # Slot for when an image is clicked in the grid
    def on_image_clicked(self, index):
        # Update current_image_index based on the clicked image
        self.current_image_index = index

        # Display the clicked image in the preview area
        self.update_image_display()

        self.ui.imageGridOverlay.setHidden(True)
        self.ui.imageLabel.setHidden(False)

    # Populates the grid with image thumbnails
    def populate_image_grid(self, grid_layout, image_list):
        # Clear existing widgets from the grid layout
        for i in reversed(range(grid_layout.count())):
            widget_to_remove = grid_layout.itemAt(i).widget()
            grid_layout.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()

        if not image_list:  # If no images exist, show a message
            label = QtWidgets.QLabel("No images to display")
            label.setAlignment(QtCore.Qt.AlignCenter)
            grid_layout.addWidget(label, 0, 0, 1, 4)  # Spans the entire grid
            return

        # Populate the grid with images
        for i, image_name in enumerate(image_list):
            image_path = os.path.join(self.images_labeling_dir, image_name)
            pixmap = QtGui.QPixmap(image_path)

            # Create a ClickableLabel to display the image
            label = ClickableLabel()
            label.setPixmap(pixmap.scaled(80, 80, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            label.setFixedSize(80, 80)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setFrameShape(QtWidgets.QFrame.Box)
            label.clicked.connect(lambda idx=i: self.on_image_clicked(idx))

            # Add the label to the grid layout
            grid_layout.addWidget(label, i // 4, i % 4)

    def refresh_window_info(self):
        self.images_to_label =  self.get_labeling_images()

        self.update_image_display()

    def get_labeling_images(self):
        return [f for f in os.listdir(self.images_labeling_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]