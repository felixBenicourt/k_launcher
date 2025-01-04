
# regular import
import os
import json
import logging
import shutil
import os
import re
import subprocess

# custom packages import
from k_constants import CONSTANTS


logging.basicConfig(level=logging.INFO)


def parse_packages_files(root_folder, version=None):
    """
    Walks through the directory tree starting from `root_folder` and finds all package files.

    Args:
        root_folder (str): The root directory to start searching for package files.
        version (str, optional): The version string to filter package files by version. 
        Defaults to None.

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


def load_json_file(file_path):
    """
    Loads a JSON file from the specified file path.

    Args:
        file_path (str): The path to the JSON file to load.

    Returns:
        dict or None: The loaded data if the file exists and is valid JSON, 
        or None if there was an error (e.g., file not found or invalid JSON).
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


def grab_package_to_local(package_name):
    """
    Copies the specified package from PROD to LOCAL, including all versions.

    Args:
        package_name (str): The name of the package to grab.
    """
    src_path = os.path.join(CONSTANTS.rootParseFolder, package_name)
    dest_path = os.path.join(CONSTANTS.rootLocalFolder, package_name)

    if not os.path.exists(src_path):
        logging.error(f"Source package '{src_path}' not found in PROD.")
        return

    try:
        if os.path.exists(dest_path):
            logging.warning(f"Package '{package_name}' already exists in LOCAL. Overwriting...")
            shutil.rmtree(dest_path)
        shutil.copytree(src_path, dest_path)
        logging.info(f"Package '{package_name}' successfully copied from PROD to LOCAL.")
    except Exception as e:
        logging.error(f"Failed to copy package '{package_name}': {e}")


def switch_rez_package_path(package_name, use_local=True):
    """
    Updates the search path for a specific Rez package.

    Args:
        package_name (str): The name of the package to switch.
        use_local (bool): If True, use LOCAL path; otherwise, use PROD path.
    """
    package_path = os.path.join(
        CONSTANTS.rootLocalFolder if use_local else CONSTANTS.rootParseFolder, 
        package_name
    )

    if not os.path.exists(package_path):
        logging.error(f"Package path does not exist: {package_path}")
        return

    try:
        os.environ[f"REZ_{package_name.upper()}_PACKAGE_PATH"] = package_path
        logging.info(f"Path for package '{package_name}' switched to: {package_path}")
    except Exception as e:
        logging.error(f"Failed to switch path for package '{package_name}': {e}")


def update_version(file_path, new_version):
    """
    Updates the version in a given file by replacing the current version with the new version.

    Args:
        file_path (str): The path to the file containing the version.
        new_version (str): The new version to replace the current version.

    Raises:
        Exception: If an error occurs during the file read/write operation.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        match = re.search(r'version\s*=\s*["\']?([^"\']+)["\']?', content)

        if match:
            old_version = match.group(1)  # Extract the found version string
            content_rewrite = content.replace(old_version, new_version)
            logging.info(f"Version updated from {old_version} to {new_version}")

            with open(file_path, 'w') as file:
                file.write(content_rewrite)
        else:
            logging.error("Version not found in the file.")

    except Exception as e:
        logging.error(f"Error occurred: {e}")


def release_package(package_local, package_prod):
    """
    Copies a package from the local directory to the production directory and updates its version.

    Args:
        package_local (str): The name of the package in the local directory (e.g., 'iter-1.1.0').
        package_prod (str): The name of the package in the production directory (e.g., 'iter-1.1.1').

    Raises:
        Exception: If the source package is not found or the copy operation fails.
    """

    if not os.path.exists(package_local):
        logging.error(f"Source package '{package_local}' not found in LOCAL.")
        return

    try:
        shutil.copytree(package_local, package_prod)
        update_version(f"{package_prod}\\package.py", package_prod.split("-")[-1])
        logging.info(f"Package '{package_local}' successfully copied from LOCAL to PROD as {package_prod}.")

    except Exception as e:
        logging.error(f"Failed to copy package '{package_local}': {e}")


def launch_vs_with_package(folder_path):
    command = f"code {folder_path}"
    logging.info(f"Launch Vs Code with the package path : {command}")
    subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

