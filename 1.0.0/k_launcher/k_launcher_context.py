


import os
import json
import logging
from k_constants import CONSTANTS
import psutil


PACKAGE_CONTEXT_FILE = os.path.join(CONSTANTS.root_folder,CONSTANTS.context_folder, CONSTANTS.package_context)


def get_terminal_pid():
    current_process = psutil.Process(os.getpid())
    parent_pid = current_process.ppid()

    while parent_pid:
        parent_process = psutil.Process(parent_pid)
        if 'cmd.exe' in parent_process.name().lower():
            return parent_pid
        parent_pid = parent_process.ppid()

    return None


class PackageContextManager:
    def __init__(self):
        self.session_id = str(get_terminal_pid())
        if not self.session_id:
            raise ValueError("Could not retrieve terminal title")

    def save_data_context(self, dataName, dataValue):
        """
        Save the current package and branch values to a JSON file using terminal window title as the key.
        """
        context = {}
        if os.path.exists(PACKAGE_CONTEXT_FILE):
            with open(PACKAGE_CONTEXT_FILE, "r") as file:
                try:
                    context = json.load(file)
                except json.JSONDecodeError:
                    logging.warning("Failed to decode JSON, starting fresh.")
        if self.session_id:
            context[self.session_id] = {dataName:dataValue}
            with open(PACKAGE_CONTEXT_FILE, "w") as file:
                json.dump(context, file, indent=4)
            logging.info(f"{dataName} context saved: {dataValue}")
        else:
            logging.warning("Failed to get the session ID.")

    def load_data_context(self):
        """
        Load the package value from the JSON file if it exists, using the terminal's window title.
        """
        if os.path.exists(PACKAGE_CONTEXT_FILE):
            with open(PACKAGE_CONTEXT_FILE, "r") as file:
                saveValue = json.load(file)
                if self.session_id in saveValue:
                    context = saveValue[self.session_id]
                    self.package = context.get("package")
                    self.branch = context.get("branch")
                    logging.info(f"Context loaded for session {self.session_id}: package = {self.package}, branch = {self.branch}")
                    return context
                else:
                    logging.warning(f"No context found for session {self.session_id}.")
                    return {}
        else:
            logging.warning("Context file not found.")
            return {}

    def get_data_context(self):
        context = self.load_data_context()
        if context:
            for key, val in context.items():
                logging.info(f"context : {key} value is {val}")


"""
if __name__ == "__main__":
    manager = PackageContextManager()
    manager.save_data_context('package', 'iterCmds')
    context = manager.load_data_context()
    print(context)
"""