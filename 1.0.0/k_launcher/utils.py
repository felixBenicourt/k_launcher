

import os
import CONSTANTS
import dcc_packages
import json
import logging


logging.basicConfig(level=logging.INFO)



def parse_packages_files(root_folder, version = None):
    package_files = []
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename == CONSTANTS.package:
                if version in foldername:
                    package_files.append(os.path.join(foldername, filename))
    return package_files


def filter_packages_from_dcc(packages_files, dcc):
    packages = dcc_packages.packages_assignation[dcc]
    filter_packages = []
    for path in packages_files:
        for package in packages:
            if package in path:
                filter_packages.append(path.replace(CONSTANTS.package, ""))
    return filter_packages


def get_dcc_packages_paths(dcc):
    packages_files = parse_packages_files(CONSTANTS.rootParseFolder)
    filter_packages = filter_packages_from_dcc(packages_files, dcc)
    return filter_packages


def load_json_file(file_path):
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
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        logging.info(f"Data saved to '{file_path}' successfully.")
    except Exception as e:
        logging.info(f"Error occurred while saving data to '{file_path}': {e}")


