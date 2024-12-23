# IMGEAN - Image Generation and Annotation

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Configuration](#configuration)
4. [Usage](#usage)
   - [Image Generation](#image-generation)
   - [Quality Checking](#quality-checking)
   - [Annotation](#annotation)
5. [Extending the app](#extending-the-app)
   - [Setting up ComfyUI](#setting-up-comfyui)
   - [Setting up your own generation flow](#setting-up-your-own-generation-flow)
   - [Setting up your own automatic-checking functions](#setting-up-your-own-automatic-checking-functions)
   - [Setting up yout own auto-labeling model](#setting-up-your-own-auto-labeling-model)

---

## Introduction

IMGEAN is a tool developed to streamline the generation, management, and annotation of image datasets. It is ideal for creating synthetic datasets from scratch or performing synthetic data augmentation. The tool simplifies image generation while enabling efficient data cleaning and labeling.

---

## Features
- **Multiple Project Management**: Manage multiple datasets simultaneously with flexible import and management tools.
- **Image Generation Module**:
  - Text-to-image (txt2img) generation using a pre-installed ComfyUI server.
  - Configurable parameters such as model selection, number of steps, seed, and image size, ensuring transparent integration with the ComfyUI server.
- **Quality Checker Submodule**:
  - Automatic filtering based on custom user-defined rules.
  - A manual review interface to approve or discard images.
- **Image Annotation Module**:
  - Manual, assisted, and automatic annotation modes.
  - Confidence-level visualization to support assisted annotations.
- **Dynamic System Design**: Provides seamless integration of image generation, quality checking, and annotation workflows.

---

## Getting Started

### Prerequisites
- **Python**: Version 3.11.2 or higher
- **Dependencies**: Listed in `requirements.txt`
- **ComfyUI**: Pre-installed locally with Stable Diffusion 3.

### Installation
1. **Install ComfyUI Locally**  
   Follow the instructions provided in the [ComfyUI repository](https://github.com/comfyanonymous/ComfyUI) to set up the required server.

2. **Clone the IMGEAN Repository**  
   Run the following commands to clone the project repository and navigate into it:
   ```bash
   git clone https://github.com/your-repo/IMGEAN.git
   cd IMGEAN
   ```

3. **Install Dependencies**  
   Use `pip` to install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Using IMGEAN**  
   The setup is complete, and you're ready to begin!

### Configuration
All project-related configurations can be managed directly from the **Settings** tab within the app. If any issues arise, the application settings can be manually edited in the `config.yaml` file.

For advanced customization or using custom models, please refer to the [Extending the App](#extending-the-app) section.

---

## Usage

Start the application with the following command:
```bash
python3 main.py
```

### Base Menu
The base menu provides access to all the functionalities of the application, including image generation, quality checking, and annotation.

### Image Generation
1. Navigate to the **Image Generation** menu.
2. Enter a prompt and define the parameters (e.g., number of images, model, size).
3. Optionally configure quality filters.
4. Start the generation process.

> **Note**: If your model or quality filters are not visible, configure them from the **Settings** tab or refer to the [Extending the App](#extending-the-app) section for further instructions.

### Quality Checking
1. Navigate to the **Quality Checker** menu.
2. In the **"Images to Check"** section:
   - Review images that passed the automatic filters.
   - Approve or discard images using the manual interface.
   - If the image generation results were consistently poor or excellent, you can opt to discard or accept all images at once.

3. In the **"Discarded Images"** section:
   - View all images that were deemed not good enough during the quality check.
   - Check the reasons for rejection. If you no longer agree with the decision, you can re-incorporate the images into the workflow by accepting them.
   - Permanently delete discarded images to free up disk space if they are no longer needed.

> **Note**: Automatic filters configured during image generation are executed before manual checking. If no quality checking is selected, images proceed directly to the annotation stage.

### Annotation
1. Access the **Annotation** module.
2. Select the image you want to label from the menu on the left.
3. Use the panel on the right to:
   - View all available classes.
   - Manually select the appropriate labels for the image.
   - Confirm the labeling to add the annotated image to the dataset.

4. If you have a prediction model enabled:
   - Auto-label images using the model's predictions.
   - Utilize the color-coded confidence indicators (cooler tones for lower confidence, warmer tones for higher confidence) to refine annotations before saving.

---

## Extending the App

IMGEAN is designed to integrate with external generation servers, custom models, and user-defined functions, making it highly adaptable. Below are the steps to customize and extend the application to suit your needs.

### Setting Up ComfyUI
To download and install ComfyUI, you can find numerous tutorials online. Generally, the process involves:
1. Cloning the ComfyUI repository.
2. Downloading the required models and placing them in the appropriate directories.

For optimal integration, it is recommended to install ComfyUI in the same parent directory as IMGEAN. However, this location can be modified in the **Settings** tab.

### Setting Up Your Own Generation Flow
IMGEAN's default generation flow is designed for pedestrian image generation and uses a specific workflow with custom nodes. To set up your own workflow, follow these steps:

1. **Configure Your Workflow**:
   Use the graphical interface of ComfyUI to design your custom workflow.

2. **Install the Custom Node**:
   Install the extension from [ComfyUI-to-Python-Extension](https://github.com/pydn/ComfyUI-to-Python-Extension), which enables a button to export the flow as a Python file. Export the workflow you created earlier.

3. **Replace the Default Workflow**:
   - Navigate to `IMGEAN/backend/image_generator/comfyui_utils.py` to locate the current default flow.
   - Rename the existing flow file and replace it with your exported Python file, ensuring it has the same filename as the original (`comfyui_utils.py`).

4. **Modify the Main Function**:
   Replace the `main()` function in your custom flow with the following signature:
   ```python
   def execute_prompt(prompt_text: str, negative_prompt: str, execution_count: int, model_name: str, steps: int, output_filename: str, seed: int, config=None, progress_callback=None):
   ```

5. **Customize Parameters**:
   Inside your workflow, adjust parameters as needed. All nodes can be freely edited since the workflow is written in Python. For example:
   - Link `prompt_text` to the `text` argument of the `CLIPTextEncode` node.
   - Unused parameters can be omitted.

#### Need Different Parameters? Here's What You Can Do

Currently, the frontend does not support dynamically configurable parameters. However, you can use one of the following options:

##### Option 1: Parse Parameters from the Prompt
Use a string in the prompt to represent multiple parameters. In the `execute_prompt` function, parse the string into the necessary arguments before running the workflow.

##### Option 2: Modify the Application Code
For more complex changes, you can modify the application's source code:
1. **Update the Frontend**:
   - Add the desired inputs in the file `IMGEAN/frontend/generator_window_ui.py`.

2. **Update the Controller**:
   - Adjust the `generate_images()` function in `IMGEAN/frontend/generator_window.py` to handle the new inputs and pass them as arguments to `ImageGenerationThread`.

3. **Update the Backend**:
   - Modify the `ImageGenerationThread` class in `IMGEAN/backend/image_generation_thread.py`. Update its `__init__` method to include the new inputs and pass them to the `execute_prompt()` function in the `run()` method.

### Setting Up Your Own Automatic-Checking Functions

To configure your own automatic-checking functions, the framework is designed to be as transparent as possible. 

- Functions should be added in the directory `IMGEAN/backend/quality_checker` and must follow this template:  
  ```python
  def <function_name>(img, *args) -> bool
  ```
  The function should return `True` if the criterion is met and the image should be discarded.

- Several examples can be found in the same folder for reference.

Once added, the new functions will automatically appear in the **Settings** menu. From there, you can import them into your project and start using them without modifying any application code.

### Setting Up Your Own Auto-Labeling Model

Unfortunately, when loading models with PyTorch, the model’s weights alone are not sufficient; the model's definition is also required. Follow these steps for the simplest configuration:

1. **Modify `custom_models`**:
   - Implement the following functions in `IMGEAN/backend/annotation_manager/custom_models`:
     - A function to **retrieve the model** (e.g., initializing the model and returning it as a variable).
     - A function to **load the model**, which applies its weights and configurations.
     - A function to **retrieve the model’s transformations** (e.g., input resizing, normalization).

   - Additional helper functions or classes might be needed. These should be added under `model_definitions/<MODEL_NAME>`.  

   - In `custom_models`, import all necessary functions with unique identifiers to avoid overwriting, using a naming convention like `<MODEL_NAME>_<FUNCTION_NAME>`.

2. **Update `automatic_labeling.py`**:
   - Add the new model’s loading function to the `model_mapping` dictionary.
   - Ensure the key matches the model name specified in the configuration file.

3. **Update the Configuration File**:
   - Add the new model under the `ANNOTATION->MODELS` section in `config.yaml` using the same format as the existing models.
