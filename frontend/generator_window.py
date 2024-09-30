from PyQt5 import QtWidgets
from frontend.generator_window_ui import Ui_genrate_images  # Import the UI class

class GeneratorWindow(QtWidgets.QMainWindow, Ui_genrate_images):
    def __init__(self, stacked_widget):
        super(GeneratorWindow, self).__init__()
        self.setupUi(self)  # Set up the UI
        self.stacked_widget = stacked_widget

        # Connect the return button to go back to the main screen
        self.return_button.clicked.connect(self.go_back)

        # Connect the generate and cancel buttons
        self.generate_button.clicked.connect(self.generate_images)
        self.cancel_button.clicked.connect(self.cancel_generation)

    def go_back(self):
        """Navigate back to the main screen"""
        self.stacked_widget.setCurrentIndex(0)  # Assuming index 0 is the main screen

    def generate_images(self):
        """Handle image generation logic"""
        print("Generating images...")
        # Add your logic for generating images here

    def cancel_generation(self):
        """Cancel the current image generation process"""
        print("Generation canceled")