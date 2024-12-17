import os
import CONSTANTS
import dcc_packages
import json
import logging

logging.basicConfig(level=logging.INFO)

def parse_packages_files(root_folder, version=None):
    """
    Walks through the directory tree starting from `root_folder` and finds all package files.

    Args:
        root_folder (str): The root directory to start searching for package files.
        version (str, optional): The version string to filter package files by version. Defaults to None.

    Returns:
        list: A list of paths to package files that match the version (if provided).
    """
    package_files = []
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename == CONSTANTS.package:
                if version in foldername:
                    package_files.append(os.path.join(foldername, filename))
    return package_files


def filter_packages_from_dcc(packages_files, dcc):
    """
    Filters the list of package files based on the DCC tool.

    Args:
        packages_files (list): A list of paths to package files.
        dcc (str): The DCC tool (e.g., 'maya', 'houdini') to filter packages for.

    Returns:
        list: A list of filtered package paths that are associated with the given DCC tool.
    """
    packages = dcc_packages.packages_assignation[dcc]
    filter_packages = []
    for path in packages_files:
        for package in packages:
            if package in path:
                filter_packages.append(path.replace(CONSTANTS.package, ""))
    return filter_packages


def get_dcc_packages_paths(dcc):
    """
    Retrieves the paths for the packages associated with a specific DCC tool.

    Args:
        dcc (str): The DCC tool (e.g., 'maya', 'houdini') to get package paths for.

    Returns:
        list: A list of package paths associated with the given DCC tool.
    """
    packages_files = parse_packages_files(CONSTANTS.rootParseFolder)
    filter_packages = filter_packages_from_dcc(packages_files, dcc)
    return filter_packages


def load_json_file(file_path):
    """
    Loads a JSON file from the specified file path.

    Args:
        file_path (str): The path to the JSON file to load.

    Returns:
        dict or None: The loaded data if the file exists and is valid JSON, or None if there was an error (e.g., file not found or invalid JSON).
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        logging.info(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        logging.info(f"Error: Unable to parse JSON in file '{file_path}': {e}")
        return None


def save_json_file(file_path, data):
    """
    Saves data to a JSON file at the specified file path.

    Args:
        file_path (str): The path to save the JSON file.
        data (dict): The data to save, typically in dictionary format.

    Returns:
        None: Logs success or failure messages during the save operation.
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        logging.info(f"Data saved to '{file_path}' successfully.")
    except Exception as e:
        logging.info(f"Error occurred while saving data to '{file_path}': {e}")

