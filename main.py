import sys
from PyQt5.QtWidgets import QApplication
from frontend.main_window import MainWindow  # Import the logic class (MainWindow)

# Main entry point of the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create an instance of MainWindow (which includes both UI and logic)
    main_window = MainWindow()
    main_window.show()  # Show the main window

    sys.exit(app.exec_())  # Execute the application