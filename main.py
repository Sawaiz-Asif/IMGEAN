# main.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from frontend.main_window import Ui_MainWindow  # Import the generated UI class

# Define a MainMenu class to encapsulate the main window setup
class MainMenu(QMainWindow):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.ui = Ui_MainWindow()  # Create an instance of the generated UI class
        self.ui.setupUi(self)      # Set up the UI inside this QMainWindow

# Main entry point of the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainMenu()  # Create an instance of MainMenu
    main_window.show()        # Show the main window
    sys.exit(app.exec_())     # Execute the application