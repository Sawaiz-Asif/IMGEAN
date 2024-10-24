from PyQt5 import QtWidgets, QtGui, QtCore
from frontend.annotate_img_ui import Ui_AnnotateImg  # Import the UI
import os
import backend.file_utils as fu
from backend.annotation_manager.automatic_labeling import open_model,get_predictions_with_confidence

# Custom QLabel to handle image clicks
class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()  # Custom signal to emit when clicked

    def mousePressEvent(self, event):
        self.clicked.emit()  # Emit signal when label is clicked
        super().mousePressEvent(event)

class AnnotateImg(QtWidgets.QWidget):
    def __init__(self, stacked_widget, config, images_labeling_dir="data"):
        super(AnnotateImg, self).__init__()
        self.ui = Ui_AnnotateImg(config)  # Initialize the UI
        self.ui.setupUi(self)
        self.stacked_widget = stacked_widget  # Reference to the QStackedWidget for navigation

        self.config = config

        self.images_labeling_dir = images_labeling_dir

        # Initialize predictions storage
        self.predictions_for_images = {}  # Initialize an empty dictionary to store predictions for all images


        # Connect the buttons to their respective methods
        self.ui.returnButton.clicked.connect(self.on_return_click)
        self.ui.prevButton.clicked.connect(self.on_prev_click)
        self.ui.discardButton.clicked.connect(self.on_discard_click)
        self.ui.nextButton.clicked.connect(self.on_next_click)
        self.ui.autoLabelImgButton.clicked.connect(self.on_auto_label_img_click)
        self.ui.autoLabelAllButton.clicked.connect(self.on_auto_label_all_click)
        self.ui.confirmLabelButton.clicked.connect(self.on_confirm_label_click)
        self.ui.openImageGridButton.clicked.connect(self.on_open_image_grid_click)
        self.ui.importButton.clicked.connect(self.on_import_dataset_click)

        # Track the current image index for navigation
        self.current_image_index = 0
        self.images_to_label =  self.get_labeling_images()

        self.update_image_display()
        self.update_checkboxes_selection()

    def on_return_click(self):
        # Return to the main screen

        self.ui.imageGridOverlay.setHidden(True)
        self.ui.imageLabel.setHidden(False)

        self.stacked_widget.setCurrentIndex(0)

    def on_prev_click(self):
        # Go to the previous image
        if self.current_image_index > 0:
                self.current_image_index -= 1
        self.update_image_display()
        self.update_checkboxes_selection()

    def on_discard_click(self):
        # Discard the current image
        discarded_image = self.images_to_label.pop(self.current_image_index)
        if (self.current_image_index>0):
            self.current_image_index -= 1
        fu.move_labeling_discard(self.config, discarded_image)
        self.populate_image_grid(self.ui.imageGridLayout, self.images_to_label)
        self.update_image_display()
        self.update_checkboxes_selection()

    def on_next_click(self):
        # Go to the next image
        if self.current_image_index < len(self.images_to_label) - 1:
                self.current_image_index += 1
        self.update_image_display()
        self.update_checkboxes_selection()

    def on_auto_label_img_click(self):
        # Auto-label the current image
        print(f"Auto-labeling image {self.current_image_index + 1}")

        # Check if there are images to label
        if not self.images_to_label:
            print("No images to label.")
            QtWidgets.QMessageBox.warning(self, "Warning", "No images to label.")
            return

        # Get the image path
        image_path = self.images_to_label[self.current_image_index]
        image_path = self.ui.dataset_manager.config['FILES']['LABELING_DIR'] + '/' + image_path
        print(f"Image path: {image_path}")
        
        # Get class labels
        class_labels = self.ui.dataset_manager.annotation.attr_name

        # For opening the model, we just need the config file and how many labels are there
        model = open_model(self.ui.dataset_manager.config, number_attributes=len(class_labels))

        # Get confidence thresholds and colors from the config (list of thresholds and corresponding colors)
        thresholds = self.config['AUTO_LABEL']['CONFIDENCE_THRESHOLDS']
        default_color = self.config['AUTO_LABEL'].get('DEFAULT_COLOR', 'black')  # Default to black if not found

        # Get the checkbox threshold from the config
        checkbox_threshold = self.config['AUTO_LABEL'].get('CHECKBOX_THRESHOLD', 0.5)  # Default to 0.5 if not set

        try:
            # Call the automatic labeling function
            predictions = get_predictions_with_confidence(self.config, model, image_path, class_labels)

            # Update checkboxes and labels based on the predictions
            for i in range(self.ui.labelList.count()):
                item = self.ui.labelList.item(i)
                widget = self.ui.labelList.itemWidget(item)
                checkbox = widget.findChild(QtWidgets.QCheckBox)
                label_widget = widget.findChild(QtWidgets.QLabel)

                # Get the label and confidence for this prediction
                label, confidence = predictions[i]

                # Update the checkbox based on the threshold from the config
                checkbox.setChecked(confidence > checkbox_threshold)

                # Update the label text to show the confidence percentage
                percentage_text = f"{confidence * 100:.0f}%"
                label_widget.setText(f"{label} ({percentage_text})")

                # Find the appropriate color based on confidence
                color = default_color  # Default color if no threshold matches
                for threshold in thresholds:
                    if confidence > threshold['value']:
                        color = threshold.get('color', default_color)  # Use default if color is missing

                # Apply color to the label
                label_widget.setStyleSheet(f"color: {color};")

            QtWidgets.QMessageBox.information(self, "Success", f"Auto-labeled image {self.current_image_index + 1}")

        except Exception as e:
            print(f"Error during auto-labeling: {str(e)}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error during auto-labeling: {str(e)}")

    def on_auto_label_all_click(self):
        # Auto-label all images
        print("Auto-labeling all images")

        # Check if there are images to label
        if not self.images_to_label:
            print("No images to label.")
            QtWidgets.QMessageBox.warning(self, "Warning", "No images to label.")
            return

        # Dictionary to store predictions for each image
        self.predictions_for_images = {}

        # Determine how many images to label, starting from the current index
        # Get the batch size from the config
        num_images_to_label = self.ui.dataset_manager.config.get('AUTO_LABEL', {}).get('BATCH_SIZE', 10)  # Default to 10 if not set

        # Create a modal progress dialog (loader)
        progress_dialog = QtWidgets.QProgressDialog(f"Auto-labeling {num_images_to_label} images...", None, 0, num_images_to_label)
        progress_dialog.setWindowTitle("Please wait")
        progress_dialog.setWindowModality(QtCore.Qt.ApplicationModal)  # Block interaction with the app
        progress_dialog.setCancelButton(None)  # Optionally, disable the cancel button
        progress_dialog.setMinimumDuration(0)  # Show the loader immediately
        progress_dialog.setValue(0)  # Start at 0 progress
        progress_dialog.show()

        try:
            class_labels = self.ui.dataset_manager.annotation.attr_name

            # For opening the model, we just need the config file and how many labels there are
            model = open_model(self.ui.dataset_manager.config, number_attributes=len(class_labels))

            # Loop through the images starting from the current image index
            for idx, image_index in enumerate(range(self.current_image_index, self.current_image_index + num_images_to_label)):
                image_path = self.images_to_label[image_index]
                image_path_full = os.path.join(self.ui.dataset_manager.config['FILES']['LABELING_DIR'], image_path)

                # Run predictions
                predictions = get_predictions_with_confidence(self.config, model, image_path_full, class_labels)

                # Store the predictions for this image
                self.predictions_for_images[image_path] = predictions

                # Update the UI with the new predictions for the current image
                if image_index == self.current_image_index:
                    self.update_checkboxes_selection()

                # Allow the UI to update after processing each image
                QtWidgets.QApplication.processEvents()

                # Update progress bar after each image is processed
                progress_dialog.setValue(idx + 1)

            QtWidgets.QMessageBox.information(self, "Success", f"Auto-labeled {num_images_to_label} images successfully.")

        except Exception as e:
            print(f"Error during auto-labeling: {str(e)}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error during auto-labeling: {str(e)}")

        finally:
            # Hide the progress dialog when done
            progress_dialog.close()

    def on_confirm_label_click(self):
        # Confirm the selected labels
        labels_selection = self.get_labels_selection()
        dm = self.ui.dataset_manager
        image_path = self.images_to_label[self.current_image_index]
        if (not dm.is_image_in_dataset(image_path)):
            image_name = os.path.basename(image_path)
            fu.move_labeling_dataset(self.config, image_name, dm.root)
            new_image_path = os.path.join(dm.root, image_name)
            dm.add_image(new_image_path, labels_selection)
            self.images_to_label[self.images_to_label.index(image_name)] = new_image_path # Modify the name on the array so it points to the new location
        else:
            _, image_index = dm.get_image_index(image_path)
            self.ui.dataset_manager.edit_label_for_image(image_index, labels_selection)

    def on_open_image_grid_click(self):
        # Show the image grid overlay
        self.ui.imageGridOverlay.setHidden(False)

        self.populate_image_grid(self.ui.imageGridLayout, self.images_to_label)

        self.ui.imageLabel.setHidden(True)  # Hide the image display

    def on_image_clicked(self, index):
        # Update current_image_index based on the clicked image
        self.current_image_index = index

        # Display the clicked image in the preview area
        self.update_image_display()
        self.update_checkboxes_selection()

        self.ui.imageGridOverlay.setHidden(True)
        self.ui.imageLabel.setHidden(False)

    def on_import_dataset_click(self):
        _, dataset_images = self.ui.dataset_manager.fetch_batch_of_images_paths(-1)
        self.images_to_label.extend(image for image in dataset_images if image not in set(self.images_to_label))
        self.populate_image_grid(self.ui.imageGridLayout, self.images_to_label)
        self.update_image_display()
        self.update_checkboxes_selection()

    def update_image_display(self):
        # Update the image display based on the current image index
        self.ui.imageLabel.setText(f"Image {self.current_image_index + 1}")
        if self.images_to_label:
            image_name = self.images_to_label[self.current_image_index]
            if not os.path.dirname(image_name) not in ("", "."):
                image_path = os.path.join(self.images_labeling_dir, image_name)
            else:
                image_path = image_name
            pixmap = QtGui.QPixmap(image_path)
            self.ui.imageLabel.setPixmap(
                pixmap.scaled(self.ui.imageLabel.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            )
        else:
            self.ui.imageLabel.setText("No images to display")  # Display message if no images

    def update_checkboxes_selection(self):
        """
        This function updates the checkboxes and label colors based on predictions (if available)
        or falls back to the existing dataset labels if predictions are not found.
        """
        image_path = self.images_to_label[self.current_image_index]

        # Check if the image has already been auto-labeled
        if image_path in self.predictions_for_images:
            predictions = self.predictions_for_images[image_path]
        else:
            # If not auto-labeled, fallback to the current labels in the dataset
            if self.ui.dataset_manager.is_image_in_dataset(image_path):
                _, labels_select = self.ui.dataset_manager.get_labels_by_image_path(image_path)
            else:
                # If the image is not in the dataset, initialize labels to 0 (unchecked)
                labels_select = [0] * len(self.ui.dataset_manager.get_dataset_labels()[1])
            predictions = [(label, None) for label in labels_select]  # No confidence available

        # Iterate over the checkboxes and apply predictions or default dataset labels
        for i in range(self.ui.labelList.count()):
            item = self.ui.labelList.item(i)
            widget = self.ui.labelList.itemWidget(item)
            checkbox = widget.findChild(QtWidgets.QCheckBox)
            label_widget = widget.findChild(QtWidgets.QLabel)

            # If predictions exist, use them; otherwise, fall back to dataset labels
            if predictions[i][1] is not None:  # If confidence is available
                label, confidence = predictions[i]
                # Set checkbox based on confidence threshold from config
                checkbox_threshold = self.config['AUTO_LABEL'].get('CHECKBOX_THRESHOLD', 0.5)
                checkbox.setChecked(confidence > checkbox_threshold)

                # Update the label text with the confidence score
                percentage_text = f"{confidence * 100:.0f}%"
                label_widget.setText(f"{label} ({percentage_text})")

                # Apply color based on confidence score and thresholds
                thresholds = self.config['AUTO_LABEL']['CONFIDENCE_THRESHOLDS']
                default_color = self.config['AUTO_LABEL'].get('DEFAULT_COLOR', 'black')
                color = default_color
                for threshold in thresholds:
                    if confidence > threshold['value']:
                        color = threshold.get('color', default_color)
                label_widget.setStyleSheet(f"color: {color};")
            else:
                # No predictions, fall back to the dataset labels (default behavior)
                checkbox.setChecked(bool(labels_select[i]))

                # Reset the label text to its original without confidence score
                label_widget.setText(self.ui.dataset_manager.annotation.attr_name[i])

                label_widget.setStyleSheet("color: black;")

    def populate_image_grid(self, grid_layout, image_list):
        # Clear existing widgets from the grid layout
        for i in reversed(range(grid_layout.count())):
            widget_to_remove = grid_layout.itemAt(i).widget()
            grid_layout.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()

        if not image_list:  # If no images exist, show a message
            label = QtWidgets.QLabel("No images to display")
            label.setAlignment(QtCore.Qt.AlignCenter)
            grid_layout.addWidget(label, 0, 0, 1, 4)  # Spans the entire grid
            return

        # Populate the grid with images
        for i, image_name in enumerate(image_list):
            if not os.path.dirname(image_name) not in ("", "."):
                image_path = os.path.join(self.images_labeling_dir, image_name)
            else:
                image_path = image_name
            pixmap = QtGui.QPixmap(image_path)

            # Create a ClickableLabel to display the image
            label = ClickableLabel()
            label.setPixmap(pixmap.scaled(80, 80, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            label.setFixedSize(80, 80)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setFrameShape(QtWidgets.QFrame.Box)
            label.clicked.connect(lambda idx=i: self.on_image_clicked(idx))

            # Add the label to the grid layout
            grid_layout.addWidget(label, i // 4, i % 4)

    def refresh_window_info(self):
        self.images_to_label =  self.get_labeling_images()

        self.update_image_display()
        self.update_checkboxes_selection()

    def get_labeling_images(self):
        return [f for f in os.listdir(self.images_labeling_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    def get_labels_selection(self):
        # Function to get the selection status of checkboxes as a binary array
        selections = []
        for i in range(self.ui.labelList.count()):
            # Get the list widget item
            item = self.ui.labelList.item(i)
            
            # Get the widget associated with the item (which contains the checkbox and label)
            widget = self.ui.labelList.itemWidget(item)
            
            # Extract the checkbox from the widget's layout
            checkbox = widget.findChild(QtWidgets.QCheckBox)
            
            # Append 1 if checked, otherwise 0
            selections.append(1 if checkbox.isChecked() else 0)     
        return selections
