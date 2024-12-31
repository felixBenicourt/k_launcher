


import os
import json
import logging
from k_constants import CONSTANTS
import k_launcher_id


PACKAGE_CONTEXT_FILE = os.path.join(CONSTANTS.root_folder,CONSTANTS.context_folder, CONSTANTS.package_context)


class PackageContextManager:
    def __init__(self):
        self.session_id = str(k_launcher_id.get_terminal_pid())
        if not self.session_id:
            raise ValueError("Could not retrieve terminal title")

    def save_data_context(self, dataName, dataValue):
        """
        Saves the current context (e.g., package, branch, or path) to a JSON file using the session ID as the key.

        Args:
            dataName (str): Name of the context variable.
            dataValue (str): Value of the context variable.
        """
        context = {}
        if os.path.exists(PACKAGE_CONTEXT_FILE):
            with open(PACKAGE_CONTEXT_FILE, "r") as file:
                try:
                    context = json.load(file)
                except json.JSONDecodeError:
                    logging.warning("Failed to decode JSON, starting fresh.")

        if self.session_id:
            if self.session_id in context:
                context[self.session_id].update({dataName: dataValue})
            else:
                context[self.session_id] = {dataName: dataValue}

            with open(PACKAGE_CONTEXT_FILE, "w") as file:
                json.dump(context, file, indent=4)
            logging.info(f"{dataName} context saved: {dataValue}")
        else:
            logging.warning("Failed to get the session ID.")

    def load_data_context(self):
        """
        Loads the context (e.g., package, branch, or path) from a JSON file using the session ID as the key.

        Returns:
            dict: The loaded context or an empty dictionary if not found.
        """
        if os.path.exists(PACKAGE_CONTEXT_FILE):
            with open(PACKAGE_CONTEXT_FILE, "r") as file:
                saveValue = json.load(file)
                if self.session_id in saveValue:
                    context = saveValue[self.session_id]
                    self.package = context.get("package")
                    self.branch = context.get("branch")
                    self.path = context.get("path")
                    return context
                else:
                    logging.warning(f"No context found for session {self.session_id}.")
                    return {}
        else:
            logging.warning("Context file not found.")
            return {}

    def get_data_context(self):
        """
        Displays the current context information loaded from the JSON file.
        """
        context = self.load_data_context()
        if context:
            for key, val in context.items():
                logging.info(f"context : {key} value is {val}")


