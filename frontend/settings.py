from PyQt5 import QtWidgets
from frontend.settings_ui import Ui_SettingsWindow  # Import the UI class

class SettingsWindow(QtWidgets.QMainWindow, Ui_SettingsWindow):
    def __init__(self,stacked_widget):
        super(SettingsWindow, self).__init__()
        self.setupUi(self)

        self.stacked_widget = stacked_widget  # Store reference to the stacked widget

        # Connect button clicks to methods
        self.returnButton.clicked.connect(self.on_return)
        self.addClassesButton.clicked.connect(self.add_class)
        self.removeModelButton.clicked.connect(self.remove_model)
        self.modelSettingsButton.clicked.connect(self.open_model_settings)
        self.addNewModelButton.clicked.connect(self.add_new_model)
        self.removeImageModelButton.clicked.connect(self.remove_image_model)
        self.imageModelSettingsButton.clicked.connect(self.open_image_model_settings)
        self.addNewImageModelButton.clicked.connect(self.add_new_image_model)
        self.removeQualityModelButton.clicked.connect(self.remove_quality_model)
        self.qualityModelSettingsButton.clicked.connect(self.open_quality_model_settings)
        self.addNewQualityModelButton.clicked.connect(self.add_new_quality_model)

    # Methods to handle button actions
    def on_return(self):
        self.stacked_widget.setCurrentIndex(0)
        print("Returning to the main menu")
        # Logic to return to the main screen can be added here

    def add_class(self):
        print("Adding new class...")

    def remove_model(self):
        print("Removing selected annotator model...")

    def open_model_settings(self):
        print("Opening annotator model settings...")

    def add_new_model(self):
        print("Adding a new annotator model...")

    def remove_image_model(self):
        print("Removing selected image model...")

    def open_image_model_settings(self):
        print("Opening image model settings...")

    def add_new_image_model(self):
        print("Adding a new image model...")

    def remove_quality_model(self):
        print("Removing selected quality checker model...")

    def open_quality_model_settings(self):
        print("Opening quality checker model settings...")

    def add_new_quality_model(self):
        print("Adding a new quality checker model...")

# Run the application
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec_())