

# regular import
import os
import json
import logging

# custom packages import
from k_constants import CONSTANTS
import k_launcher_id


PACKAGE_CONTEXT_FILE = os.path.join(CONSTANTS.root_folder, CONSTANTS.context_folder, CONSTANTS.package_context)


class PackageContextManager:
    """
    Manages the context for the current session by saving and loading 
    information (e.g., package, branch, or path) using a session ID as the key.

    Attributes:
        session_id (str): The unique identifier for the current session, 
                          retrieved from the terminal process ID.

    Raises:
        ValueError: If the session ID cannot be retrieved.
    """
    def __init__(self):
        """
        Initializes the PackageContextManager by setting the session ID.
        
        Raises:
            ValueError: If the terminal title cannot be retrieved, 
                        indicating a problem obtaining the session ID.
        """
        self.session_id = str(k_launcher_id.get_terminal_pid())
        if not self.session_id:
            raise ValueError("Could not retrieve terminal title")

    def save_data_context(self, dataName, dataValue):
        """
        Saves the current context (e.g., package, branch, or path) to a JSON file 
        using the session ID as the key.

        Args:
            dataName (str): The name of the context variable to save.
            dataValue (str): The value of the context variable to save.

        Behavior:
            - Reads the existing context from the JSON file, if it exists.
            - Updates or adds the context information for the current session.
            - Writes the updated context back to the JSON file.

        Logs:
            - Logs a success message when the context is saved.
            - Logs a warning if the session ID is unavailable.

        Warnings:
            If the JSON file cannot be decoded, starts with a fresh context.

        Raises:
            None.
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
        Loads the context (e.g., package, branch, or path) from a JSON file 
        using the session ID as the key.

        Returns:
            dict: The loaded context for the current session, or an empty 
                  dictionary if the context is not found.

        Behavior:
            - Reads the JSON file for saved context data.
            - Checks if the current session ID exists in the loaded context.
            - Retrieves context values (e.g., package, branch, or path) 
              if available.

        Logs:
            - Logs a warning if the session ID is not found in the file.
            - Logs a warning if the file does not exist.

        Raises:
            None.
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

        Behavior:
            - Calls `load_data_context` to retrieve the saved context.
            - Logs each key-value pair in the loaded context.

        Logs:
            - Logs the key-value pairs of the context.
            - Logs a warning if the context is not found or the file is missing.

        Raises:
            None.
        """
        context = self.load_data_context()
        if context:
            for key, val in context.items():
                logging.info(f"context : {key} value is {val}")
