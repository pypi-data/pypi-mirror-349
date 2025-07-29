# filetools.py
# Import packages
import json, shutil, os

# Load a JSON file into a dictionary
def json_to_dict(path: str) -> dict:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        raise Exception(f"Error loading JSON file: {e}")

def dict_to_json(path: str, data: dict) -> None:
    try:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        raise Exception(f"Error saving JSON file: {e}")

def copy_file(src: str, dst: str, overwrite: bool = False) -> None:
    try:
        if os.path.exists(dst) and not overwrite:
            raise Exception("Destination file exists and overwrite is False")
        shutil.copy2(src, dst)
    except Exception as e:
        raise Exception(f"Error copying file: {e}")

# Read a directory structure
def os_to_dict(path: str, content: bool = False, show_nr_files: bool = True) -> dict:
    result = {}
    
    # Check if the path exists and is a directory
    if not os.path.exists(path) or not os.path.isdir(path):
        raise OSError(f"Invalid or inaccessible directory: {path}")
    
    # Get the directory name from the path
    dirname = os.path.basename(path)
    result[dirname] = {}
    
    # Iterate through all items in the directory
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        
        if os.path.isdir(item_path):
            # Recursively process subdirectories with the same parameters
            subdir_structure = os_to_dict(item_path, content, show_nr_files)
            result[dirname].update(subdir_structure)
        else:
            # Handle files
            if content:
                try:
                    with open(item_path, 'r', encoding='utf-8') as file:
                        result[dirname][item] = file.read()
                except (IOError, UnicodeDecodeError):
                    if show_nr_files:
                        result[dirname][item] = "<non-readable content>"
            else:
                if show_nr_files:
                    # Include all files
                    result[dirname][item] = {}
                else:
                    # Include only text-readable files
                    try:
                        with open(item_path, 'r', encoding='utf-8') as file:
                            file.read(1024)  # Read first 1024 bytes to check
                        result[dirname][item] = {}
                    except (IOError, UnicodeDecodeError):
                        # Skip non-readable files
                        continue
    
    return result