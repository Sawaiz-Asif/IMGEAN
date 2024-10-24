import sys
from PyQt5.QtWidgets import QApplication
from frontend.main_window import MainWindow  # Import the logic class (MainWindow)
from backend.config_reader import read_config
import backend.file_utils as fu

# Main entry point of the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    config = read_config('./config.yaml')

    # import shutil
    # shutil.rmtree('./data', ignore_errors=True)
    # shutil.copytree('./data_start', './data')

    fu.verify_or_create_dirs(config)

    # Create an instance of MainWindow (which includes both UI and logic)
    main_window = MainWindow(config)
    main_window.show()  # Show the main window

    sys.exit(app.exec_())  # Execute the application