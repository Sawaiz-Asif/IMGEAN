from PyQt5 import QtWidgets, QtGui, QtCore
from frontend.generator_window_ui import Ui_generate_images
#from backend.image_generator.image_generation_thread import ImageGenerationThread
# from backend.image_generator.comfyui_utils import execute_prompt
from backend.config_reader import save_config
import backend.file_utils as fu
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QSystemTrayIcon, QMessageBox
import os
from PyQt5.QtCore import QThread, pyqtSignal
from backend.quality_checker.quality_checker_loader import load_quality_checkers
import shutil
import time


class GeneratorWindow(QtWidgets.QMainWindow):
    def __init__(self, main_window, config, ui_styles):
        super(GeneratorWindow, self).__init__()
        self.config = config
        self.main_window = main_window

        self.ui = Ui_generate_images(config, ui_styles)  # Initialize the UI  # Reference to the QStackedWidget for navigation
        self.ui.setupUi(self)

        # Set up the QGraphicsScene
        self.scene = QGraphicsScene()
        self.ui.graphics_view.setScene(self.scene)
        self.scene

        # Initialize system tray icon for notifications
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon("./assets/icon.png"))

        # Connect buttons
        self.ui.return_button.clicked.connect(self.go_back)
        self.ui.generate_button.clicked.connect(self.generate_images)
        self.ui.cancel_button.clicked.connect(self.cancel_generation)

        self.ui.cancel_button.setDisabled(True)
        self.ui.progress_bar.setVisible(True)
        self.ui.progress_bar.setValue(0)
        self.generation_thread = None

        self.show_image()
        self.load_initial_values()

    def load_initial_values(self):
        """Load saved values from the configuration."""
        # Load prompts
        self.ui.text_prompt.setPlainText(self.config['GENERATION']['PROMPTS'].get('positive', ''))
        self.ui.text_negative_prompt.setPlainText(self.config['GENERATION']['PROMPTS'].get('negative', ''))
        self.ui.spin_images.setValue(self.config['GENERATION'].get('num_images', 1))
        self.ui.combo_model.setCurrentText(self.config['GENERATION'].get('model', ''))
        self.ui.spin_steps.setValue(self.config['GENERATION'].get('steps', 20))
        self.ui.text_filename.setText(self.config['GENERATION'].get('filename', 'generated_image'))

        # Load seed
        seed = self.config['GENERATION'].get('seed', '')
        self.ui.text_seed.setText(str(seed) if seed else "")
        self.ui.text_seed.setPlaceholderText("Optional")

        # Load manual quality check status
        self.ui.checkbox_manual.setChecked(self.config['GENERATION'].get('manual_quality_check', False))

        # Load the automatic quality check items state using selected_checks list
        selected_checks = self.config['QUALITY_CHECKS'].get('selected_checks', [])
        for i in range(self.ui.auto_check_list.count()):
            item = self.ui.auto_check_list.item(i)
            custom_checkbox = self.ui.auto_check_list.itemWidget(item)  # Retrieve the custom checkbox widget
            if custom_checkbox:
                if i < len(selected_checks):
                    # Set the checkbox state based on the selected_checks list
                    custom_checkbox.setChecked(selected_checks[i] == 1)
                else:
                    # Set the checkbox to unchecked if the index is out of bounds
                    custom_checkbox.setChecked(False)

    def generate_images(self):
        """Handle image generation logic."""
        print("Generating images...")

        # Disable the Generate button and enable Cancel button
        self.ui.generate_button.setDisabled(True)
        self.ui.cancel_button.setDisabled(False)

        # Save the current state to the configuration file
        self.save_current_state()

        # Retrieve input values
        positive_prompt = self.ui.text_prompt.toPlainText()
        negative_prompt = self.ui.text_negative_prompt.toPlainText()
        num_images = self.ui.spin_images.value()
        model_name = self.ui.combo_model.currentText()
        steps = self.ui.spin_steps.value()
        filename = self.ui.text_filename.text()
        seed = int(self.ui.text_seed.text()) if self.ui.text_seed.text().isdigit() else None
        self.last_img_gen_num=num_images

        # Reset progress bar and start thread
        self.ui.progress_bar.setValue(0)
        self.ui.progress_bar.setTextVisible(True)
        self.ui.progress_bar.setFormat(f"Generating 0/{num_images}")

        # self.generation_thread = ImageGenerationThread(
        #     positive_prompt, negative_prompt, num_images, model_name, steps, filename, seed, self.config
        # )
        # self.generation_thread.progress_signal.connect(self.update_progress_bar)
        # self.generation_thread.image_signal.connect(self.show_image)
        # self.generation_thread.finished.connect(self.on_generation_complete)
        # self.generation_thread.start()

    def update_progress_bar(self, current, total):
        """Update the progress bar with 'Generating {current}/{total}'."""
        percentage = int((current / total) * 100)
        self.ui.progress_bar.setValue(percentage)
        self.ui.progress_bar.setFormat(f"Generating {current}/{total}")
        if current == total:
            self.ui.progress_bar.setFormat("Complete")

    def show_image(self, image_path=None):
        """Display an image or show placeholder text if not available."""
        self.scene.clear()
        
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if pixmap and not pixmap.isNull():
                item = QGraphicsPixmapItem(pixmap)
                self.scene.addItem(item)

                scene_rect = self.scene.sceneRect()
                item_rect = item.boundingRect()

                # Center the item within the scene
                item.setPos(scene_rect.center() - item_rect.center())

                self.ui.graphics_view.fitInView(item, QtCore.Qt.KeepAspectRatio)
                return
        
        # If no valid image or path, show placeholder text
        self.show_placeholder_text()

    def show_placeholder_text(self):
        """Display placeholder text if no image is available."""
        self.scene.clear()
        text_item = self.scene.addText("No Image Available")
        text_item.setDefaultTextColor(QtGui.QColor("#888"))
        text_item.setFont(QtGui.QFont("Arial", 14))
        self.ui.graphics_view.fitInView(text_item, QtCore.Qt.KeepAspectRatio)

    def on_generation_complete(self):
        """Handle completion of the generation."""
        print("Generation complete!")
        self.ui.progress_bar.setFormat("Complete")

        # If no images were generated, show the placeholder
        if not os.path.exists(self.config['GENERATION'].get('filename', '')):
            self.show_image()  # Show the placeholder

        fu.ensure_unique_id_generation(self.config)

        # --- Automatic quality checking starts here ---
        # Get the selection of the quality functions to be used
        selected_quality_function_checkboxes = []
        for i in range(self.ui.auto_check_list.count()):
            item = self.ui.auto_check_list.item(i)
            custom_checkbox = self.ui.auto_check_list.itemWidget(item)
            if custom_checkbox.checkState() == True:
                selected_quality_function_checkboxes.append(custom_checkbox.text())

        # Get the pointers to all the quality functions (on the directory)
        quality_checkers_functions = load_quality_checkers(self.config)
        # Get the configurations for the quality checkers (config file)
        config_quality_checkers = self.config.get('QUALITY_CHECKS', {}).get('FUNCTIONS', [])

        success = True
        # For each function on the configuration file (the ones showed to the user)
        for config_function in config_quality_checkers:
            function_user_name = config_function['name']
            if function_user_name in selected_quality_function_checkboxes: #If it is selected
                filename = os.path.basename(config_function['path'])
                function = quality_checkers_functions[filename] # Get the pointer
                success = fu.discard_generated_images_based_on_function(self.config, function, config_function['args']) # Use it
                if (not success):
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setWindowTitle("Error")
                    msg.setText(f"There was an exception when executing \"{function_user_name}\" auto-checker function. Aborting process.")
                    msg.exec_()
                    break
        # --- Automatic quality checking ends here ---
        if (not success):
            self.ui.generate_button.setDisabled(False)
            self.ui.cancel_button.setDisabled(True)
            return


        # Move generated files and add them to the annotation system
        if self.ui.checkbox_manual.isChecked():
            fu.move_all_generated_images_checking(self.config)
        else:
            fu.move_all_generated_images_labeling(self.config)


        self.show_notification("Image Generation", "Generation completed successfully!")
        self.ui.generate_button.setDisabled(False)
        self.ui.cancel_button.setDisabled(True)
        self.show_image()



    def show_notification(self, title, message):
        """Show a system tray notification."""
        self.tray_icon.show()
        self.tray_icon.showMessage(title, message, QtWidgets.QSystemTrayIcon.Information, 5000)

    def cancel_generation(self):
        """Cancel the current generation process."""
        if self.generation_thread and self.generation_thread.isRunning():
            self.generation_thread.terminate()
            self.generation_thread.wait()
        print("Generation canceled")
        self.ui.progress_bar.setValue(0)
        self.ui.generate_button.setDisabled(False)
        self.ui.cancel_button.setDisabled(True)

        # Show the placeholder image since generation was canceled
        self.show_image()

    def save_current_state(self):
        """Save the current state of the UI to the configuration."""
        # Save prompts, number of images, model, steps, filename, and seed
        self.config['GENERATION']['PROMPTS']['positive'] = self.ui.text_prompt.toPlainText()
        self.config['GENERATION']['PROMPTS']['negative'] = self.ui.text_negative_prompt.toPlainText()
        self.config['GENERATION']['num_images'] = self.ui.spin_images.value()
        self.config['GENERATION']['model'] = self.ui.combo_model.currentText()
        self.config['GENERATION']['steps'] = self.ui.spin_steps.value()
        self.config['GENERATION']['filename'] = self.ui.text_filename.text()
        
        seed = self.ui.text_seed.text()
        self.config['GENERATION']['seed'] = int(seed) if seed.isdigit() else None

        self.config['GENERATION']['manual_quality_check'] = self.ui.checkbox_manual.isChecked()

        # Save the automatic quality checks using a compact list format
        checks = [1 if self.ui.auto_check_list.item(i).checkState() == QtCore.Qt.Checked else 0
                for i in range(self.ui.auto_check_list.count())]
        self.config['QUALITY_CHECKS']['selected_checks'] = checks

        self.save_config()

    def save_config(self):
        """Save the updated configuration to the YAML file."""
        config_path = './config.yaml'
        save_config(self.config, config_path)
        print("Configuration saved!")
    
    def go_back(self):
        """Navigate back to the main screen."""
        print("Returning to the main screen...")
        self.save_current_state()
        self.main_window.change_current_screen(0)