import os
import random
import sys
from typing import Sequence, Mapping, Any, Union
import torch
import shutil
import subprocess
import socket
import time
import os
import signal

GENERATION = 'GENERATION'
BASE_OUTPUT_PATH = 'BASE_OUTPUT_PATH'
FILES = 'FILES'
GENERATED_DIR = 'GENERATED_DIR'


def get_value_at_index(obj: Union[Sequence, Mapping], index: int) -> Any:
    """Returns the value at the given index of a sequence or mapping.

    If the object is a sequence (like list or string), returns the value at the given index.
    If the object is a mapping (like a dictionary), returns the value at the index-th key.

    Some return a dictionary, in these cases, we look for the "results" key

    Args:
        obj (Union[Sequence, Mapping]): The object to retrieve the value from.
        index (int): The index of the value to retrieve.

    Returns:
        Any: The value at the given index.

    Raises:
        IndexError: If the index is out of bounds for the object and the object is not a mapping.
    """
    try:
        return obj[index]
    except KeyError:
        return obj["result"][index]


def find_path(name: str, path: str = None) -> str:
    """
    Recursively looks at parent folders starting from the given path until it finds the given name.
    Returns the path as a Path object if found, or None otherwise.
    """
    # If no path is given, use the current working directory
    if path is None:
        path = os.getcwd()

    # Check if the current directory contains the name
    if name in os.listdir(path):
        path_name = os.path.join(path, name)
        #print(f"{name} found: {path_name}")
        return path_name

    # Get the parent directory
    parent_directory = os.path.dirname(path)

    # If the parent directory is the same as the current directory, we've reached the root and stop the search
    if parent_directory == path:
        return None

    # Recursively call the function with the parent directory
    return find_path(name, parent_directory)


def add_comfyui_directory_to_sys_path() -> None:
    """
    Add 'ComfyUI' to the sys.path
    """
    comfyui_path = find_path("ComfyUI")
    if comfyui_path is not None and os.path.isdir(comfyui_path):
        sys.path.append(comfyui_path)
        #print(f"'{comfyui_path}' added to sys.path")


def add_extra_model_paths() -> None:
    """
    Parse the optional extra_model_paths.yaml file and add the parsed paths to the sys.path.
    """
    try:
        from main import load_extra_path_config
    except ImportError:
        #print(
        #    "Could not import load_extra_path_config from main.py. Looking in utils.extra_config instead."
        #)
        from utils.extra_config import load_extra_path_config

    extra_model_paths = find_path("extra_model_paths.yaml")

    if extra_model_paths is not None:
        load_extra_path_config(extra_model_paths)
    else:
        #print("Could not find the extra_model_paths config file.")
        pass


add_comfyui_directory_to_sys_path()
add_extra_model_paths()


def import_custom_nodes() -> None:
    """Find all custom nodes in the custom_nodes folder and add those node objects to NODE_CLASS_MAPPINGS

    This function sets up a new asyncio event loop, initializes the PromptServer,
    creates a PromptQueue, and initializes the custom nodes.
    """
    import asyncio
    import execution
    from nodes import init_extra_nodes
    import server

    # Creating a new event loop and setting it as the default loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Creating an instance of PromptServer with the loop
    server_instance = server.PromptServer(loop)
    execution.PromptQueue(server_instance)

    # Initializing custom nodes
    init_extra_nodes()


from nodes import NODE_CLASS_MAPPINGS


def execute_prompt(prompt_text: str, negative_prompt: str, execution_count: int, model_name: str, steps: int, output_filename: str, seed: int, config=None, progress_callback=None):
    import_custom_nodes()
    with torch.inference_mode():
        checkpointloadersimple = NODE_CLASS_MAPPINGS["CheckpointLoaderSimple"]()
        checkpointloadersimple_4 = checkpointloadersimple.load_checkpoint(
            ckpt_name=model_name
        )

        emptylatentimage = NODE_CLASS_MAPPINGS["EmptyLatentImage"]()
        emptylatentimage_5 = emptylatentimage.generate(
            width=1024, height=1024, batch_size=1
        )

        cliptextencode = NODE_CLASS_MAPPINGS["CLIPTextEncode"]()
        cliptextencode_6 = cliptextencode.encode(
            text=prompt_text,
            clip=get_value_at_index(checkpointloadersimple_4, 1),
        )

        cliptextencode_7 = cliptextencode.encode(
            text=negative_prompt,
            clip=get_value_at_index(checkpointloadersimple_4, 1),
        )

        ksampler = NODE_CLASS_MAPPINGS["KSampler"]()
        vaedecode = NODE_CLASS_MAPPINGS["VAEDecode"]()
        toolyolocropper = NODE_CLASS_MAPPINGS["ToolYoloCropper"]()
        saveimage = NODE_CLASS_MAPPINGS["SaveImage"]()

        for q in range(execution_count):
            if seed == None: 
                seed = random.randint(1, 2**64) 
            else:
                seed = seed+q
            ksampler_3 = ksampler.sample(
                seed=seed,
                steps=steps,
                cfg=8,
                sampler_name="euler",
                scheduler="normal",
                denoise=1,
                model=get_value_at_index(checkpointloadersimple_4, 0),
                positive=get_value_at_index(cliptextencode_6, 0),
                negative=get_value_at_index(cliptextencode_7, 0),
                latent_image=get_value_at_index(emptylatentimage_5, 0),
            )

            vaedecode_8 = vaedecode.decode(
                samples=get_value_at_index(ksampler_3, 0),
                vae=get_value_at_index(checkpointloadersimple_4, 2),
            )

            toolyolocropper_10 = toolyolocropper.detect(
                object="person", padding=0, image=get_value_at_index(vaedecode_8, 0)
            )
            

            saveimage_9 = saveimage.save_images(
                filename_prefix=output_filename,
                images=get_value_at_index(toolyolocropper_10, 2),
            )
            source_dir = config[GENERATION][BASE_OUTPUT_PATH]

            image_info = saveimage_9.get('ui', {}).get('images', [])
            if len(image_info) > 0:
                image_filename = image_info[0].get('filename')
                if image_filename:
                    image_path = os.path.join(source_dir, image_filename)  # Assuming './output' is your image directory
                    print(image_path)
                    progress_callback(q + 1, image_path)
            else:
                progress_callback(q + 1, None)
             # Update progress bar if provided
            # Update progress if a callback is provided
            progress_callback(q+1,image_path)

    if config is not None:
        source_dir = config[GENERATION][BASE_OUTPUT_PATH]
        dest_dir = config[FILES][GENERATED_DIR]

        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"Output directory of ComfyUI not found on: {source_dir}")

        files = os.listdir(source_dir)
        if not files:
            raise FileNotFoundError(f"Generated files not found")

        for filename in files:
            source_path = os.path.join(source_dir, filename)
            dest_path = os.path.join(dest_dir, filename)

            if os.path.isfile(source_path):
                shutil.move(source_path, dest_path)

def is_port_in_use(port, host="127.0.0.1"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def terminate_process_on_port(port):
    try:
        # Use lsof to find the process using the port, omitting the host IP
        for proc in subprocess.check_output(["lsof", "-i", f":{port}"]).splitlines():
            if b"LISTEN" in proc:
                pid = int(proc.split()[1])  # Extract the process ID
                os.kill(pid, signal.SIGTERM)
                time.sleep(1)  # Give it a moment to close
                return True
    except subprocess.CalledProcessError:
        # lsof will return a non-zero exit code if nothing is using the port
        return False

def start_comfyui_server(retries=5):
    port = 8188  # Specify the ComfyUI server port

    for attempt in range(1, retries + 1):
        if is_port_in_use(port):
            print(f"Port {port} is already in use. Attempting to terminate existing process...")
            process_terminated = terminate_process_on_port(port)
            if not process_terminated and attempt == retries + 1:
                raise RuntimeError(f"Failed to terminate process on port {port}.")
            elif not process_terminated:
                print(f"Failed on terminate process on port {port}. Retrying ({attempt}/{retries})...")
            else:
                print(f"Terminated process on port {port}.")


    # Try to start the ComfyUI server
    print("Starting ComfyUI server...")
    process = subprocess.Popen(["python3", "main.py"], cwd="../ComfyUI")

    """
    It can be added
    process = subprocess.Popen(
        ["python3", "main.py"],
        cwd="path/to/comfyui",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True  # Ensures the output is captured as strings, not bytes
    )

    And then in another part of the code

    output = process.stdout.readline()
    And just check the output for getting the percentages

    But we need an extra subprocess for that probably
    """

    return process

        

    raise RuntimeError("Failed to start ComfyUI server after multiple attempts.")


def start_comfyui_server_old():

    print("Starting ComfyUI server...")
    process = subprocess.Popen(["python3", "main.py"], cwd="../ComfyUI")

    """
    It can be added
    process = subprocess.Popen(
        ["python3", "main.py"],
        cwd="path/to/comfyui",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True  # Ensures the output is captured as strings, not bytes
    )

    And then in another part of the code

    output = process.stdout.readline()
    And just check the output for getting the percentages

    But we need an extra subprocess for that probably
    """

    return process

def stop_comfyui_server(process):
    print("Closing ComfyUI server...")
    process.terminate()
    process.wait()
    print("Server closed")

if __name__ == "__main__":
    # Example usage

    positive_prompt = "A highly detailed, ultra high definition image of a single pedestrian on an airport, with the pedestrian fully visible and centered in the frame. The pedestrian is visible from head to toe and is the primary focus, and the scene features realistic, natural colors.​"
    negative_prompt = "Partial figures, cropped bodies, low-resolution images, blurred backgrounds, no low-angle or ground-level shots, no side views, no back views, avoid any obscured faces, dull or muted colors, overly zoomed-in perspectives, and no non-airport settings."

    execute_prompt(
        prompt_text=positive_prompt,
        negative_prompt=negative_prompt,
        execution_count=3,
        model_name="sd3_medium_incl_clips.safetensors",
        steps=20,
        output_filename="ComfyUI_custom_output",
        seed=None,
        config=None
    )