from PyQt5 import QtCore
from backend.image_generator.comfyui_utils import execute_prompt

class ImageGenerationThread(QtCore.QThread):
    progress_signal = QtCore.pyqtSignal(int, int)  # Signal with current and total count
    image_signal = QtCore.pyqtSignal(str)  # Signal for sending the image path

    def __init__(self, prompt_text, negative_prompt, execution_count, model_name, steps, output_filename, seed, config):
        super().__init__()
        self.prompt_text = prompt_text
        self.negative_prompt = negative_prompt
        self.execution_count = execution_count
        self.model_name = model_name
        self.steps = steps
        self.output_filename = output_filename
        self.seed = seed
        self.config = config

    def run(self):
        """Run the image generation process."""
        def progress_callback(current_image, image_path=None):
            self.progress_signal.emit(current_image, self.execution_count)
            if image_path:
                self.image_signal.emit(image_path)

        execute_prompt(
            prompt_text=self.prompt_text,
            negative_prompt=self.negative_prompt,
            execution_count=self.execution_count,
            model_name=self.model_name,
            steps=self.steps,
            output_filename=self.output_filename,
            seed=self.seed,
            config=self.config,
            progress_callback=progress_callback
        )