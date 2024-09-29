import os
import subprocess

def convert_all_ui_files(directory):
    """
    Convert all .ui files in the specified directory to .py files using pyuic5.
    :param directory: The directory to search for .ui files.
    """
    # Walk through all files in the specified directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.ui'):
                # Full path of the .ui file
                ui_file_path = os.path.join(root, file)
                # Determine the output .py file path
                py_file_path = os.path.join(root, file.replace('.ui', '.py'))
                
                # Command to convert .ui to .py using pyuic5
                command = ['pyuic5', '-x', ui_file_path, '-o', py_file_path]
                
                try:
                    # Run the conversion command
                    subprocess.run(command, check=True)
                    print(f"Successfully converted: {ui_file_path} -> {py_file_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Error converting {ui_file_path}: {e}")

if __name__ == "__main__":
    # Set the directory where your .ui files are located (e.g., 'frontend')
    ui_directory = os.path.join(os.getcwd(), 'frontend')  # Change 'frontend' to your specific folder
    convert_all_ui_files(ui_directory)