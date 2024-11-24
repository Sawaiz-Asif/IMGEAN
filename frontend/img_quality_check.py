import os
from PyQt5 import QtWidgets, QtGui, QtCore
from frontend.img_quality_check_ui import Ui_CheckImgQuality  # Import the UI file
import backend.file_utils as fu

from config_constants import *

# Custom QLabel to handle image clicks
class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()  # Custom signal to emit when clicked

    def mousePressEvent(self, event):
        self.clicked.emit()  # Emit signal when label is clicked
        super().mousePressEvent(event)

class CheckImgQuality(QtWidgets.QMainWindow):
    def __init__(self, main_window, config, ui_styles):
        super(CheckImgQuality, self).__init__()
        self.main_window = main_window  # Reference to the QStackedWidget for navigation
        self.images_checking_dir = config[FILES][CHECKING_DIR]  # Folder where the images are stored
        self.images_discarded_dir = config[FILES][DISCARDED_DIR]

        self.config = config

        self.ui = Ui_CheckImgQuality(config, ui_styles)  # Initialize the UI
        self.ui.setupUi(self)


        self.current_tab_index = self.ui.tab_widget.currentIndex()

        # Load image file names from the dataset folder
        self.current_checking_index = 0  # Tracks the current image being displayed
        self.current_discarded_index = 0
        self.images_to_check =  self.get_checking_images()
        self.discarded_images = self.get_discarded_images()


        # Populate both tabs with images
        self.populate_image_grid(self.ui.gridLayoutToCheck, self.images_to_check, is_discarded=False)
        self.populate_image_grid(self.ui.gridLayoutDiscarded, self.discarded_images, is_discarded=True)

        # Initially load the first image in the image preview area
        self.load_current_image()

        # Connect navigation buttons to their respective methods
        for tab_name in self.ui.tab_components:
            tab = self.ui.tab_components[tab_name]
            tab["prev_button"].clicked.connect(self.on_prev_click)
            tab["next_button"].clicked.connect(self.on_next_click)
            tab["first_button"].clicked.connect(self.on_first_action_click)  # Discard/Delete
            tab["second_button"].clicked.connect(self.on_accept_click)  # Accept action
            tab["red_all_button"].clicked.connect(self.on_all_button_click)
            if tab_name == "checking":
                tab["accept_all"].clicked.connect(self.on_accept_all_click)
                
        
        self.ui.returnButton.clicked.connect(self.on_return_click)  # Return button to go back to previous screen
        self.ui.tab_widget.currentChanged.connect(self.on_tab_change)

    # Populates the grid with image thumbnails
    def populate_image_grid(self, grid_layout, image_list, is_discarded):
        # Clear existing widgets from the grid layout
        for i in reversed(range(grid_layout.count())):
            widget_to_remove = grid_layout.itemAt(i).widget()
            grid_layout.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()

        if not image_list:  # If no images exist, show a message
            label = QtWidgets.QLabel("No images to display")
            label.setStyleSheet("""
                padding: 20px;
            """)
            label.setAlignment(QtCore.Qt.AlignCenter)
            grid_layout.addWidget(label, 0, 0, 1, 4)  # Spans the entire grid
            return

        # Populate the grid with images
        for i, image_name in enumerate(image_list):
            if is_discarded == False:
                image_path = os.path.join(self.images_checking_dir, image_name)
            else:
                image_path = os.path.join(self.images_discarded_dir, image_name)
            pixmap = QtGui.QPixmap(image_path)

            # Create a ClickableLabel to display the image
            label = ClickableLabel()
            label.setPixmap(pixmap.scaled(80, 80, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            label.setFixedSize(80, 80)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setFrameShape(QtWidgets.QFrame.Box)
            label.clicked.connect(lambda idx=i: self.on_image_clicked(idx, is_discarded))

            # Add the label to the grid layout
            grid_layout.addWidget(label, i // 4, i % 4)

    # Loads the current image into the image preview area
    def load_current_image(self):
        if self.current_tab_index == 1:  # "Images to Check" tab
            if self.images_to_check:
                image_name = self.images_to_check[self.current_checking_index]
                image_path = os.path.join(self.images_checking_dir, image_name)
                pixmap = QtGui.QPixmap(image_path)
                self.ui.tab_components["checking"]["image_preview"].setPixmap(
                    pixmap.scaled(self.ui.tab_components["checking"]["image_preview"].size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                )
            else:
                self.ui.tab_components["checking"]["image_preview"].setText("No images to display")  # Display message if no images
        else:  # "Discarded" tab
            if self.discarded_images:
                image_name = self.discarded_images[self.current_discarded_index]
                image_path = os.path.join(self.images_discarded_dir, image_name)
                pixmap = QtGui.QPixmap(image_path)
                self.ui.tab_components["discarded"]["image_preview"].setPixmap(
                    pixmap.scaled(self.ui.tab_components["discarded"]["image_preview"].size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                )

                self.ui.reasonLabel.setText(f"Reason: {fu.get_discarded_reasons(self.config, image_name)}")
            else:
                self.ui.tab_components["discarded"]["image_preview"].setText("No discarded images")

    # Slot for when an image is clicked in the grid
    def on_image_clicked(self, index, is_discarded):
        # Update current_image_index based on the clicked image
        if self.current_tab_index == 1:
            self.current_checking_index = index
        else:
            self.current_discarded_index = index

        # Display the clicked image in the preview area
        self.load_current_image()

    # Button logic: Move to the previous image
    def on_prev_click(self):
        if self.current_tab_index == 1:
            if self.current_checking_index > 0:
                self.current_checking_index -= 1
        elif self.current_tab_index == 0:
            if self.current_discarded_index > 0:
                self.current_discarded_index -= 1
 
        self.load_current_image()

    # Button logic: Move to the next image
    def on_next_click(self):

        if self.current_tab_index == 1:
            if self.current_checking_index < len(self.images_to_check) - 1:
                self.current_checking_index += 1
        elif self.current_tab_index == 0:
            if self.current_discarded_index < len(self.discarded_images) - 1:
                self.current_discarded_index += 1
 
        self.load_current_image()


    # Button logic: First action (Discard/Delete based on the tab)
    def on_first_action_click(self):
        current_tab_index = self.ui.tab_widget.currentIndex()

        if current_tab_index == 1:  # "Images to Check" tab (Discard action)
            if self.images_to_check:
                discarded_image = self.images_to_check.pop(self.current_checking_index)
                if (self.current_checking_index>0):
                    self.current_checking_index -= 1
                self.discarded_images.append(discarded_image)
                fu.move_checking_discard(self.config, discarded_image)
                self.populate_image_grid(self.ui.gridLayoutToCheck, self.images_to_check, is_discarded=False)
                self.populate_image_grid(self.ui.gridLayoutDiscarded, self.discarded_images, is_discarded=True)
                self.load_current_image()
        else:  # "Discarded" tab (Delete action)
            if self.discarded_images:
                discarded_image = self.discarded_images.pop(self.current_discarded_index)
                if (self.current_discarded_index>0):
                    self.current_discarded_index -= 1
                fu.delete_single_discarded(self.config, discarded_image)
                self.populate_image_grid(self.ui.gridLayoutDiscarded, self.discarded_images, is_discarded=True)
                self.load_current_image()

    # Button logic: Accept the current image (removes it from the list)
    def on_accept_click(self):
        current_tab_index = self.ui.tab_widget.currentIndex()

        if current_tab_index == 1:  # "Images to Check" tab (Accept action)
            if self.images_to_check:
                accepted_image = self.images_to_check.pop(self.current_checking_index)
                if (self.current_checking_index>0):
                    self.current_checking_index -= 1
                fu.move_checking_labeling(self.config, accepted_image)
                self.populate_image_grid(self.ui.gridLayoutToCheck, self.images_to_check, is_discarded=False)
                self.load_current_image()
        else:  # "Discarded" tab (Re-accept action)
            if self.discarded_images:
                reaccepted_image = self.discarded_images.pop(self.current_discarded_index)
                if (self.current_discarded_index>0):
                    self.current_discarded_index -= 1
                fu.move_discarded_labeling(self.config, reaccepted_image)
                self.populate_image_grid(self.ui.gridLayoutDiscarded, self.discarded_images, is_discarded=True)
                self.load_current_image()

    def on_all_button_click(self):
        current_tab_index = self.ui.tab_widget.currentIndex()

        if current_tab_index == 1:  # "Images to Check" tab (Accept action)
            fu.accept_all_checking(self.config)
            self.images_to_check = []
            self.populate_image_grid(self.ui.gridLayoutToCheck, self.images_to_check, is_discarded=False)
        else:  # "Discarded" tab (Re-accept action)
            fu.delete_all_discarded(self.config)
            self.discarded_images = []
            self.populate_image_grid(self.ui.gridLayoutDiscarded, self.discarded_images, is_discarded=True)
            self.ui.reasonLabel.setText(f"")

        self.load_current_image()

    def on_accept_all_click(self):
        fu.accept_all_checking(self.config)
        self.images_to_check = []
        self.populate_image_grid(self.ui.gridLayoutToCheck, self.images_to_check, is_discarded=False)
        self.load_current_image()

    # Button logic: Return to the previous screen
    def on_return_click(self):
        # You can modify this logic depending on what screen the user should return to
        # Example: Move to the main screen of the stacked widget
        self.main_window.change_current_screen(0)

    def on_tab_change(self, index):
        self.current_tab_index = self.ui.tab_widget.currentIndex()
        self.load_current_image()
 

    def get_checking_images(self):
        return [f for f in os.listdir(self.images_checking_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    def get_discarded_images(self):
        return [f for f in os.listdir(self.images_discarded_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    def refresh_window_info(self):
        #self.current_checking_index = 0  # Tracks the current image being displayed
        #self.current_discarded_index = 0
        self.images_to_check =  self.get_checking_images()
        self.discarded_images = self.get_discarded_images()


        # Populate both tabs with images
        self.populate_image_grid(self.ui.gridLayoutToCheck, self.images_to_check, is_discarded=False)
        self.populate_image_grid(self.ui.gridLayoutDiscarded, self.discarded_images, is_discarded=True)

        # Initially load the first image in the image preview area
        self.load_current_image()

# Run the application
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    stacked_widget = QtWidgets.QStackedWidget()  # Dummy stacked widget for navigation
    window = CheckImgQuality(stacked_widget, images_folder="data")
    window.show()
    sys.exit(app.exec_())