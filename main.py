import sys
from PyQt5.QtWidgets import QApplication
from frontend.main_window import MainWindow  # Import the logic class (MainWindow)
from frontend.project_management import ProjectManagement

import backend.image_generator.comfyui_utils as cu

# Main entry point of the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    #process = cu.start_comfyui_server()
    # import shutil
    # shutil.rmtree('./data', ignore_errors=True)
    # shutil.copytree('./data_start', './data')

    try:
        # Create an instance of MainWindow (which includes both UI and logic)
        main_window = MainWindow()

        # Connect signals
        main_window.projectManagementScreen.project_changed.connect(main_window.refresh_on_project_change)

        main_window.show()  # Show the main window

        sys.exit(app.exec_())  # Execute the application
    finally:
        pass
        
        #cu.stop_comfyui_server(process)