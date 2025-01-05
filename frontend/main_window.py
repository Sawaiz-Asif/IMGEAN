from PyQt5 import QtWidgets
from frontend.main_window_ui import Ui_MainWindow  # Import the UI class
from frontend.settings import SettingsWindow
from frontend.img_quality_check import CheckImgQuality
from frontend.annotate_img import AnnotateImg  # Import Annotate Image logic
from frontend.generator_window import GeneratorWindow  # Import the logic class
from frontend.project_management import ProjectManagement
import backend.file_utils as fu
from backend.config_reader import read_config,create_projects_file
from frontend.main_screen import MainScreen
from backend.annotation_manager.dataset_utils import DatasetManager
import json
import os

FILES = 'FILES'
CHECKING_DIR = 'CHECKING_DIR'
DISCARDED_DIR = 'DISCARDED_DIR'
LABELING_DIR = 'LABELING_DIR'
CONFIG_FILE = 'config.yaml'

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, ui_styles):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow(ui_styles)
        self.ui.setupUi(self)

        # self.config = config
        self.ui_styles = ui_styles
        # Read the active project from the projects.json file
        self.active_project = self.read_active_project()
        config_path = os.path.join(self.active_project['path'], CONFIG_FILE)

        self.config  = read_config(config_path)
        fu.verify_or_create_dirs(self.config)

        dataset_path = self.config['DATASET']['PATH']
        self.dataset_manager = DatasetManager(dataset_path, self.config)

        # self.setupUi(self)  # Set up the UI

        self.setup_screens()

        # # Connect button clicks to screen navigation methods
        # self.pushButton.clicked.connect(self.goToGenerateImages)  # Button 1 (set as Go to Main)
        # self.pushButton_2.clicked.connect(self.goToImgQualityCheckScreen)   # Button 2 (navigate to Screen 2)
        # self.pushButton_3.clicked.connect(self.goToAnnotateImgSelectScreen)  # Button 3 (go to Generate Images)
        # self.pushButton_4.clicked.connect(self.goToSettingScreen)  # Button 4 (go back to Main)

        # Connect Change Project button to the navigation method
        #self.changeProjectButton.clicked.connect(self.goToProjectManagement)      

    def setup_screens(self):
        """Add additional screens to the QStackedWidget."""

        cfg = self.config[FILES]


        # Generate Images Screen
        self.generator_window = GeneratorWindow(self, self.config, self.ui_styles,self.active_project)

        # Img Quality Check Screen
        self.imgQualityCheckScreen = CheckImgQuality(self, self.config, self.ui_styles)  # Pass the stacked widget
        # Annotate image Screen
        self.annotateImgSelectScreen = AnnotateImg(self, self.config,self.dataset_manager, self.ui_styles)  # Pass the stacked widget

        # Setting Screen
        self.settingsScreen = SettingsWindow(self, self.config,self.dataset_manager,self.ui_styles,self.active_project)

        # Add Project Management Screen
        self.projectManagementScreen = ProjectManagement(self.ui.stackedWidget, self.config)

        # Create the main screen after the others (need them to be properly setted up)
        self.main_screen = MainScreen(self, self.ui_styles)

        self.main_screen.ui.project_label.setText(f'Currently working on: "{self.active_project["name"]}"')

        # Add the third screen (Generate Images) to the stacked widget
        self.ui.stackedWidget.addWidget(self.main_screen)
        self.ui.stackedWidget.addWidget(self.generator_window)
        self.ui.stackedWidget.addWidget(self.imgQualityCheckScreen)
        self.ui.stackedWidget.addWidget(self.annotateImgSelectScreen)
        self.ui.stackedWidget.addWidget(self.settingsScreen)
        self.ui.stackedWidget.addWidget(self.projectManagementScreen)  # Add the new screen

    def change_current_screen(self, idx):
        # 0 is the main screen
        # 1 is generate images
        # 2 is quality checkself.ui.main_screen
        # 3 is annotate images
        # 4 is settings 

        if idx == 2:
            self.imgQualityCheckScreen.refresh_window_info()
        elif idx == 3:
            self.annotateImgSelectScreen.refresh_window_info()
        
        self.ui.stackedWidget.setCurrentIndex(idx)
    def goToProjectManagement(self):
        # Switch to the Project Management screen
        self.stackedWidget.setCurrentWidget(self.projectManagementScreen)
    def read_active_project(self):
        """Read the projects.json file and return the active project."""
        projects_file='./projects/projects.json'
        # Check if the projects file exists
        if not os.path.exists(projects_file):
            print(f"{projects_file} not found. Creating the file...")
            create_projects_file()  # Call the function to create the file and directories
        try:
            with open(projects_file, 'r') as f:
                data = json.load(f)

            # Find the active project (marked by 'is_active': True)
            active_project = None
            for project in data.get("projects", []):
                if project.get("is_active", False):
                    active_project = project
                    break

            if active_project:
                print(f"Active project found: {active_project['name']} at {active_project['path']}")
            else:
                print("No active project found.")
            
            return active_project  # Returns the active project or None

        except Exception as e:
            print(f"Error reading projects file: {e}")
            return None
    def refresh_on_project_change(self):
        # Read the active project from the projects.json file
        print("Project is Changed Refreshing all the important data")
        self.active_project.clear()

        self.active_project.update(self.read_active_project())
        self.main_screen.ui.project_label.setText(f'Currently working on: "{self.active_project["name"]}"')
        config_path = os.path.join(self.active_project['path'], CONFIG_FILE)
        self.config.clear()  # Clear current config
        self.config.update(read_config(config_path))  # Update in place to preserve references

        # self.config  = read_config(config_path)
        fu.verify_or_create_dirs(self.config)
        dataset_path = self.config['DATASET']['PATH']
        self.dataset_manager.update_with_new_file(dataset_path, self.config)
        # self.dataset_manager.clear()
        # self.dataset_manager.update(DatasetManager(dataset_path, self.config))
        # Refresh the setting UI
        self.settingsScreen.refresh_ui()
        self.generator_window.load_initial_values()
        self.annotateImgSelectScreen.refresh_on_project_change()
        self.imgQualityCheckScreen.refresh_window_info()
# Run the application
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())