from PyQt5 import QtWidgets, QtGui, QtCore
from frontend.generator_window_ui import Ui_genrate_images
from backend.image_generator.image_generation_thread import ImageGenerationThread
from backend.image_generator.comfyui_utils import execute_prompt
from backend.config_reader import save_config
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QSystemTrayIcon
import os
from PyQt5.QtCore import QThread, pyqtSignal
import shutil
import time


class GeneratorWindow(QtWidgets.QMainWindow, Ui_genrate_images):
    def __init__(self, stacked_widget, config):
        super(GeneratorWindow, self).__init__()
        self.setupUi(self, config)
        self.stacked_widget = stacked_widget
        self.config = config

        # Set up the QGraphicsScene
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        # Initialize system tray icon for notifications
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon("./assets/icon.png"))

        # Connect buttons
        self.return_button.clicked.connect(self.go_back)
        self.generate_button.clicked.connect(self.generate_images)
        self.cancel_button.clicked.connect(self.cancel_generation)

        self.cancel_button.setDisabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.generation_thread = None

        self.show_image()
        self.load_initial_values()

    def load_initial_values(self):
        """Load saved values from the configuration."""
        # Load prompts
        self.text_prompt.setPlainText(self.config['GENERATION']['PROMPTS'].get('positive', ''))
        self.text_negative_prompt.setPlainText(self.config['GENERATION']['PROMPTS'].get('negative', ''))
        self.spin_images.setValue(self.config['GENERATION'].get('num_images', 1))
        self.combo_model.setCurrentText(self.config['GENERATION'].get('model', ''))
        self.spin_steps.setValue(self.config['GENERATION'].get('steps', 20))
        self.text_filename.setText(self.config['GENERATION'].get('filename', 'generated_image'))

        # Load seed
        seed = self.config['GENERATION'].get('seed', '')
        self.text_seed.setText(str(seed) if seed else "")
        self.text_seed.setPlaceholderText("Optional")

        # Load manual quality check status
        self.checkbox_manual.setChecked(self.config['GENERATION'].get('manual_quality_check', False))

        # Load the automatic quality check items state using selected_checks list
        selected_checks = self.config['QUALITY_CHECKS'].get('selected_checks', [])
        for i in range(self.auto_check_list.count()):
            item = self.auto_check_list.item(i)
            if i < len(selected_checks):
                item.setCheckState(QtCore.Qt.Checked if selected_checks[i] == 1 else QtCore.Qt.Unchecked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)

    def generate_images(self):
        """Handle image generation logic."""
        print("Generating images...")

        # Disable the Generate button and enable Cancel button
        self.generate_button.setDisabled(True)
        self.cancel_button.setDisabled(False)

        # Save the current state to the configuration file
        self.save_current_state()

        # Retrieve input values
        positive_prompt = self.text_prompt.toPlainText()
        negative_prompt = self.text_negative_prompt.toPlainText()
        num_images = self.spin_images.value()
        model_name = self.combo_model.currentText()
        steps = self.spin_steps.value()
        filename = self.text_filename.text()
        seed = int(self.text_seed.text()) if self.text_seed.text().isdigit() else None
        self.last_img_gen_num=num_images

        # Reset progress bar and start thread
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat(f"Generating 0/{num_images}")

        self.generation_thread = ImageGenerationThread(
            positive_prompt, negative_prompt, num_images, model_name, steps, filename, seed, self.config
        )
        self.generation_thread.progress_signal.connect(self.update_progress_bar)
        self.generation_thread.image_signal.connect(self.show_image)
        self.generation_thread.finished.connect(self.on_generation_complete)
        self.generation_thread.start()

    def update_progress_bar(self, current, total):
        """Update the progress bar with 'Generating {current}/{total}'."""
        percentage = int((current / total) * 100)
        self.progress_bar.setValue(percentage)
        self.progress_bar.setFormat(f"Generating {current}/{total}")
        if current == total:
            self.progress_bar.setFormat("Complete")

    def show_image(self, image_path=None):
        """Display an image or show placeholder text if not available."""
        self.scene.clear()
        
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if pixmap and not pixmap.isNull():
                item = QGraphicsPixmapItem(pixmap)
                self.scene.addItem(item)
                self.graphics_view.fitInView(item, QtCore.Qt.KeepAspectRatio)
                return
        
        # If no valid image or path, show placeholder text
        self.show_placeholder_text()

    def show_placeholder_text(self):
        """Display placeholder text if no image is available."""
        self.scene.clear()
        text_item = self.scene.addText("No Image Available")
        text_item.setDefaultTextColor(QtGui.QColor("#888"))
        text_item.setFont(QtGui.QFont("Arial", 14))
        self.graphics_view.fitInView(text_item, QtCore.Qt.KeepAspectRatio)

    def on_generation_complete(self):
        """Handle completion of the generation."""
        print("Generation complete!")
        self.progress_bar.setFormat("Complete")

        # If no images were generated, show the placeholder
        if not os.path.exists(self.config['GENERATION'].get('filename', '')):
            self.show_image()  # Show the placeholder

         # Move generated files and add them to the annotation system
        try:
            self.move_and_process_all_generated_images(self.config)
        except FileNotFoundError as e:
            print(e)

        self.show_notification("Image Generation", "Generation completed successfully!")
        self.generate_button.setDisabled(False)
        self.cancel_button.setDisabled(True)
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
        self.progress_bar.setValue(0)
        self.generate_button.setDisabled(False)
        self.cancel_button.setDisabled(True)

        # Show the placeholder image since generation was canceled
        self.show_image()

    def save_current_state(self):
        """Save the current state of the UI to the configuration."""
        # Save prompts, number of images, model, steps, filename, and seed
        self.config['GENERATION']['PROMPTS']['positive'] = self.text_prompt.toPlainText()
        self.config['GENERATION']['PROMPTS']['negative'] = self.text_negative_prompt.toPlainText()
        self.config['GENERATION']['num_images'] = self.spin_images.value()
        self.config['GENERATION']['model'] = self.combo_model.currentText()
        self.config['GENERATION']['steps'] = self.spin_steps.value()
        self.config['GENERATION']['filename'] = self.text_filename.text()
        
        seed = self.text_seed.text()
        self.config['GENERATION']['seed'] = int(seed) if seed.isdigit() else None

        self.config['GENERATION']['manual_quality_check'] = self.checkbox_manual.isChecked()

        # Save the automatic quality checks using a compact list format
        checks = [1 if self.auto_check_list.item(i).checkState() == QtCore.Qt.Checked else 0
                for i in range(self.auto_check_list.count())]
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
        self.stacked_widget.setCurrentIndex(0)

    def move_and_process_all_generated_images(self, config):
        """
        Move all generated images to the labeling directory, 
        rename them with a unique identifier in the source folder first, 
        and add them to the annotation manager.
        
        Args:
            config (dict): Configuration dictionary containing file paths.
        """

        # Check if the config is provided
        if config is None:
            print("Error: Configuration is missing.")
            return

        # Extract source and destination directories from config
        source_dir = config['FILES']['GENERATED_DIR']
        dest_dir = config['FILES']['LABELING_DIR']
        
        print(f"Source directory: {source_dir}")
        print(f"Destination directory: {dest_dir}")

        # Check if the source directory exists
        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"Output directory not found: {source_dir}")

        # Get the list of all files in the source directory
        files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
        
        if not files:
            print("No generated files found")
            return

        print(f"Total files to be moved and renamed: {len(files)}")

        for filename in files:
            source_path = os.path.join(source_dir, filename)

            # Generate a unique identifier using the current timestamp
            unique_id = str(int(time.time()))
            new_filename = f"{os.path.splitext(filename)[0]}_{unique_id}.png"
            new_source_path = os.path.join(source_dir, new_filename)
            dest_path = os.path.join(dest_dir, new_filename)

            # Rename the file in the source directory
            os.rename(source_path, new_source_path)
            print(f"Renamed file: {filename} -> {new_filename}")

            # Add the renamed image to the annotation manager

            print(f"Image added to annotation manager: {new_source_path}")

            # Move the renamed file to the destination directory
            shutil.move(new_source_path, dest_path)
            print(f"File moved: {new_source_path} -> {dest_path}")

        print("All files have been renamed, moved, and processed successfully.")