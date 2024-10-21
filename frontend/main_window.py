from PyQt5 import QtWidgets
from frontend.main_window_ui import Ui_MainWindow  # Import the UI class
from frontend.settings import SettingsWindow
from frontend.img_quality_check import CheckImgQuality
from frontend.annotate_img import AnnotateImg  # Import Annotate Image logic
from frontend.generator_window import GeneratorWindow  # Import the logic class

FILES = 'FILES'
CHECKING_DIR = 'CHECKING_DIR'
DISCARDED_DIR = 'DISCARDED_DIR'
LABELING_DIR = 'LABELING_DIR'

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, config):
        super(MainWindow, self).__init__()

        self.config = config

        self.setupUi(self)  # Set up the UI

        # Set up the additional screens
        self.setup_screens()

        # Connect button clicks to screen navigation methods
        self.pushButton.clicked.connect(self.goToGenerateImages)  # Button 1 (set as Go to Main)
        self.pushButton_2.clicked.connect(self.goToImgQualityCheckScreen)   # Button 2 (navigate to Screen 2)
        self.pushButton_3.clicked.connect(self.goToAnnotateImgSelectScreen)  # Button 3 (go to Generate Images)
        self.pushButton_4.clicked.connect(self.goToSettingScreen)  # Button 4 (go back to Main)

    def setup_screens(self):
        """Add additional screens to the QStackedWidget."""

        cfg = self.config[FILES]

        # Generate Images Screen
        self.generator_window = GeneratorWindow(self.stackedWidget)

        # Img Quality Check Screen
        self.imgQualityCheckScreen = CheckImgQuality(self.stackedWidget, self.config, images_checking_dir=cfg[CHECKING_DIR],  images_discarded_dir=cfg[DISCARDED_DIR])  # Pass the stacked widget
        # Annotate image Screen
        self.annotateImgSelectScreen = AnnotateImg(self.stackedWidget, self.config, images_labeling_dir=cfg[LABELING_DIR])  # Pass the stacked widget

        # Setting Screen
        self.settingsScreen = SettingsWindow(self.stackedWidget)

        # Add the third screen (Generate Images) to the stacked widget
        
        self.stackedWidget.addWidget(self.generator_window)  # Index 2 for Generate Images screen
        self.stackedWidget.addWidget(self.imgQualityCheckScreen)
        self.stackedWidget.addWidget(self.annotateImgSelectScreen)  # Add Annotate Image Select screen
        self.stackedWidget.addWidget(self.settingsScreen)

    def goToGenerateImages(self):
        # Switch to the second screen
        self.stackedWidget.setCurrentIndex(1)

    def goToImgQualityCheckScreen(self):
        # Switch back to the main screen
        self.imgQualityCheckScreen.refresh_window_info()

        self.stackedWidget.setCurrentIndex(2)

    def goToAnnotateImgSelectScreen(self):
        # Switch back to the main screen
        self.annotateImgSelectScreen.refresh_window_info()

        self.stackedWidget.setCurrentIndex(3)

    def goToSettingScreen(self):
        # Switch to the 'Generate Images' screen
        self.stackedWidget.setCurrentIndex(4)

# Run the application
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())