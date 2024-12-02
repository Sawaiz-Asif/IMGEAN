from PyQt5 import QtWidgets
from frontend.main_window_ui import Ui_MainWindow  # Import the UI class
from frontend.settings import SettingsWindow
from frontend.img_quality_check import CheckImgQuality
from frontend.annotate_img import AnnotateImg  # Import Annotate Image logic
from frontend.generator_window import GeneratorWindow  # Import the logic class
from frontend.main_screen import MainScreen

FILES = 'FILES'
CHECKING_DIR = 'CHECKING_DIR'
DISCARDED_DIR = 'DISCARDED_DIR'
LABELING_DIR = 'LABELING_DIR'

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, config, ui_styles):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow(ui_styles)
        self.ui.setupUi(self)

        self.config = config
        self.ui_styles = ui_styles

        self.setup_screens()

    def setup_screens(self):
        """Add additional screens to the QStackedWidget."""

        cfg = self.config[FILES]


        # Generate Images Screen
        self.generator_window = GeneratorWindow(self, self.config, self.ui_styles)

        # Img Quality Check Screen
        self.imgQualityCheckScreen = CheckImgQuality(self, self.config, self.ui_styles)  # Pass the stacked widget
        # Annotate image Screen
        self.annotateImgSelectScreen = AnnotateImg(self, self.config, self.ui_styles)  # Pass the stacked widget

        # Setting Screen
        self.settingsScreen = SettingsWindow(self.ui.stackedWidget, self.config, self.ui_styles)

        # Create the main screen after the others (need them to be properly setted up)
        self.main_screen = MainScreen(self, self.ui_styles)

        # Add the third screen (Generate Images) to the stacked widget
        self.ui.stackedWidget.addWidget(self.settingsScreen)
        self.ui.stackedWidget.addWidget(self.main_screen)
        self.ui.stackedWidget.addWidget(self.generator_window)
        self.ui.stackedWidget.addWidget(self.imgQualityCheckScreen)
        self.ui.stackedWidget.addWidget(self.annotateImgSelectScreen)

    def change_current_screen(self, idx):
        # 0 is the main screen
        # 1 is generate images
        # 2 is quality check
        # 3 is annotate images
        # 4 is settings 

        if idx == 2:
            self.imgQualityCheckScreen.refresh_window_info()
        elif idx == 3:
            self.annotateImgSelectScreen.refresh_window_info()
        
        self.ui.stackedWidget.setCurrentIndex(idx)

# Run the application
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())