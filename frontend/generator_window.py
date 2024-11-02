from PyQt5 import QtWidgets
from frontend.generator_window_ui import Ui_genrate_images  # Import the UI class
from backend.image_generator.comfyui_utils import execute_prompt

class GeneratorWindow(QtWidgets.QMainWindow, Ui_genrate_images):
    def __init__(self, stacked_widget, config):
        super(GeneratorWindow, self).__init__()
        self.setupUi(self)  # Set up the UI
        self.stacked_widget = stacked_widget

        self.config = config

        # Connect the return button to go back to the main screen
        self.return_button.clicked.connect(self.go_back)

        # Connect the generate and cancel buttons
        self.generate_button.clicked.connect(self.generate_images)
        self.cancel_button.clicked.connect(self.cancel_generation)

    def go_back(self):
        """Navigate back to the main screen"""
        self.stacked_widget.setCurrentIndex(0)  # Assuming index 0 is the main screen

    def generate_images(self):
        """Handle image generation logic"""
        print("Generating images...")
        # Add your logic for generating images here

        # Example on the generation of images

        positive_prompt = "A highly detailed, ultra high definition image of a single pedestrian on an airport, with the pedestrian fully visible and centered in the frame. The pedestrian is visible from head to toe and is the primary focus, and the scene features realistic, natural colors.​"
        negative_prompt = "Partial figures, cropped bodies, low-resolution images, blurred backgrounds, no low-angle or ground-level shots, no side views, no back views, avoid any obscured faces, dull or muted colors, overly zoomed-in perspectives, and no non-airport settings."
        num_images = 1

        execute_prompt(
            prompt_text=positive_prompt,
            negative_prompt=negative_prompt,
            execution_count=num_images,
            model_name="sd3_medium_incl_clips.safetensors",
            steps=20,
            output_filename="ComfyUI_custom_output",
            seed=None,
            config=self.config
        )

    def cancel_generation(self):
        """Cancel the current image generation process"""
        print("Generation canceled")