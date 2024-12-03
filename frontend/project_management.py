import os
import json
import re
import shutil
from backend.config_reader import create_default_config
from PyQt5.QtCore import pyqtSignal
from datetime import datetime
from PyQt5 import QtWidgets, QtCore  # <-- Import QtCore here
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QMainWindow,
    QMessageBox,
    QInputDialog,
    QGridLayout
)
from frontend.project_management_ui import Ui_ProjectManagement


class ProjectManagement(QMainWindow):
    project_changed = pyqtSignal(dict)
    def __init__(self, stacked_widget, config, parent=None):
        super().__init__(parent)
        self.ui = Ui_ProjectManagement()
        self.ui.setupUi(self)

        self.stacked_widget = stacked_widget
        self.config = config

        self.projects_file = "projects/projects.json"
        self.projects = []
        self.current_active_project = None  # Track the currently active project
        self.initial_active_project = None  # Track the initially active project
        self.load_projects()




        # Connect buttons
        self.ui.addProjectButton.clicked.connect(self.add_new_project)
        self.ui.returnButton.clicked.connect(self.return_to_main)

    def load_projects(self):
        """Load projects from the JSON file."""
        if not os.path.exists(self.projects_file):
            os.makedirs(os.path.dirname(self.projects_file), exist_ok=True)
            with open(self.projects_file, "w") as f:
                json.dump({"projects": []}, f)

        with open(self.projects_file, "r") as f:
            data = json.load(f)
            self.projects = data.get("projects", [])

        # Set the current active project from loaded data
        self.current_active_project = next(
            (project for project in self.projects if project.get("is_active", False)),
            None,
        )
        self.initial_active_project = self.current_active_project  # Save the initially active project


        self.refresh_projects_ui()

    def refresh_projects_ui(self):
        """Refresh the scroll area with project cards in a grid layout."""
        existing_layout = self.ui.scrollContent.layout()
        if existing_layout is not None:
            QtWidgets.QWidget().setLayout(existing_layout)

        grid_layout = QGridLayout()
        grid_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.ui.scrollContent.setLayout(grid_layout)

        columns = 3
        row = 0
        for index, project in enumerate(self.projects):
            column = index % columns
            card = self.create_project_card(project)
            grid_layout.addWidget(card, row, column)

            # If the column is the last in the row, move to the next row
            if column == columns - 1:
                row += 1

        # Ensure the extra space on the right is not stretched
        for i in range(columns):
            grid_layout.setColumnStretch(i, 0)  # No stretching in columns

        grid_layout.setRowStretch(row, 0)  # No stretching for the last row either

    def create_project_card(self, project):
        """Create a single project card with active state handling."""
        card = QWidget()
        card.setFixedSize(250, 250)
        # Apply active or inactive color based on project state
        if project.get("is_active", False):
            card.setStyleSheet("""
                QWidget {
                    background-color: lightgreen;
                    border: 1px solid #dcdcdc;
                    border-radius: 8px;
                    padding: 8px;
                    margin: 4px;
                    width: 50px;
                    height: 50px;
                }
                QWidget:hover {
                    background-color: #90e090;  # Slightly darker green on hover
                }
            """)
        else:
            card.setStyleSheet("""
                QWidget {
                    background-color: #ffffff;
                    border: 1px solid #dcdcdc;
                    border-radius: 8px;
                    padding: 8px;
                    margin: 4px;
                    width: 50px;
                    height: 50px;
                }
                QWidget:hover {
                    background-color: #f0f0f0;  # Light gray on hover for inactive projects
                }
            """)

        card_layout = QVBoxLayout(card)
        
        # Project Name Label (Clickable)
        project_label = QPushButton(f"Project Name: {project['name']}")
        project_label.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
                color: #333;
            }
        """)
        project_label.clicked.connect(lambda: self.set_active_project(project))
        card_layout.addWidget(project_label)

        # Created On Label
        created_on_label = QPushButton(f"Created On: {project['last_modified']}")
        created_on_label.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 10px;
                font-weight: normal;
                text-align: center;
                color: #777;
            }
        """)
        created_on_label.setEnabled(False)
        card_layout.addWidget(created_on_label)

        # Buttons Layout (Edit and Delete)
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(5)

        edit_button = QPushButton("Edit")
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #a71d2a;
            }
        """)

        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        card_layout.addLayout(button_layout)

        # Connect button signals
        edit_button.clicked.connect(lambda: self.edit_project_name(project))
        delete_button.clicked.connect(lambda: self.delete_project(project))

        return card

    def set_active_project(self, project):
        """Set a project as active."""
        for p in self.projects:
            p["is_active"] = False
        project["is_active"] = True

        self.current_active_project = project
        self.save_projects()
        self.refresh_projects_ui()

    def save_projects(self):
        """Save the current project list to the JSON file."""
        with open(self.projects_file, "w") as f:
            json.dump({"projects": self.projects}, f, indent=4)

    def add_new_project(self):
        """Handle adding a new project."""
        name, ok = QInputDialog.getText(self, "Add New Project", "Enter project name:")
        if ok and name:
            if not self.is_valid_project_name(name):
                QMessageBox.warning(self, "Error", "Invalid project name. It may contain forbidden characters.")
                return
            if any(p["name"] == name for p in self.projects):
                QMessageBox.warning(self, "Error", f"Project '{name}' already exists.")
                return
            new_project = {
                "name": name,
                "path": f"projects/{name}",
                "last_modified": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            }
            os.makedirs(new_project["path"], exist_ok=True)  # Create the project folder
            self.projects.append(new_project)
            self.save_projects()
            create_default_config(new_project['path']+'/config.yaml')
            self.refresh_projects_ui()

    def is_valid_project_name(self, name):
        """Check if the project name is valid (doesn't contain invalid folder characters)."""
        invalid_chars = r'[\/:*?"<>|]'  # Common invalid folder characters
        return not bool(re.search(invalid_chars, name))

    def edit_project_name(self, project):
        """Handle editing a project's name."""
        new_name, ok = QInputDialog.getText(self, "Edit Project Name", "Enter new project name:", text=project["name"])
        if ok and new_name:
            if not self.is_valid_project_name(new_name):
                QMessageBox.warning(self, "Error", "Invalid project name. It may contain forbidden characters.")
                return
            if any(p["name"] == new_name for p in self.projects):
                QMessageBox.warning(self, "Error", f"Project '{new_name}' already exists.")
                return
            old_name = project["name"]
            project["name"] = new_name
            project["last_modified"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            # Update the project path to reflect the new name
            old_path = project["path"]
            new_path = f"projects/{new_name}"
            project["path"] = new_path

            # Rename the folder on the filesystem
            self.rename_project_folder(old_path, new_path)
            
            self.save_projects()
            self.refresh_projects_ui()

    def rename_project_folder(self, old_path, new_path):
        """Rename the project folder to match the new name."""
        if os.path.exists(old_path):
            try:
                os.rename(old_path, new_path)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to rename folder: {e}")
                return

    def delete_project(self, project):
        """Handle deleting a project."""
        confirm = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete '{project['name']}'?")
        if confirm == QMessageBox.Yes:
            # Check if the project to delete is the active project
            was_active = project.get("is_active", False)

            # Remove the project from the list
            self.projects = [p for p in self.projects if p["name"] != project["name"]]
            
            # Delete the project folder
            self.delete_project_folder(project["path"])

            # If the deleted project was active, make the previous project active
            if was_active and self.projects:
                # Set the last project in the list as active
                self.set_active_project(self.projects[-1])

            # Save and refresh the UI
            self.save_projects()
            self.refresh_projects_ui()

    def delete_project_folder(self, project_path):
        """Delete the folder associated with the project."""
        if os.path.exists(project_path):
            try:
                shutil.rmtree(project_path)  # Remove the folder
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete folder: {e}")
    def return_to_main(self):
        """Navigate back to the main screen."""
        if self.initial_active_project != self.current_active_project:
            # Emit the signal only if the active project has changed
            self.project_changed.emit(self.current_active_project)
            self.initial_active_project = self.current_active_project
        self.stacked_widget.setCurrentIndex(0)