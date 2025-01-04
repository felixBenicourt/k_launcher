

# regular import
import logging
import git
import json
import os

# custom packages import
from k_constants import CONSTANTS


logging.basicConfig(level=logging.INFO)


class k_repo:

    def __init__(self):
        self.repo_dict = {}

    def load_repo_dict(self):
        """
        Loads the repository dictionary from the specified JSON file.
        """
        jsonPath = os.path.join(CONSTANTS.root_folder, CONSTANTS.context_folder, CONSTANTS.package_repos)
        if os.path.exists(jsonPath):
            with open(jsonPath, 'r') as file:
                data = json.load(file)
            self.repo_dict = data

    def save_repo_dict(self):
        """
        Saves the repository dictionary to the JSON file.
        """
        jsonPath = os.path.join(CONSTANTS.root_folder, CONSTANTS.context_folder, CONSTANTS.package_repos)
        with open(jsonPath, 'w') as file:
            json.dump(self.repo_dict, file, indent=4)
        logging.info("Repository dictionary saved to repos.json")

    def add_repository(self, name, url):
        """
        Adds a new repository to the dictionary.

        Args:
            name (str): Alias for the repository.
            url (str): URL of the repository.
        """
        self.repo_dict[name] = url
        logging.info(f"Repository '{name}' added with URL: {url}")
        self.save_repo_dict()

    def update_repository(self, name, new_url):
        """
        Update repository to the dictionary.

        Args:
            name (str): Alias for the repository.
            url (str): URL of the repository.
        """
        if name in self.repo_dict:
            self.repo_dict[name] = new_url
            logging.info(f"Repository '{name}' URL updated to {new_url}")
            self.save_repo_dict()
        else:
            logging.warning(f"Repository '{name}' not found.")

    def remove_repository(self, name):
        """
        Removes a repository from the dictionary.

        Args:
            name (str): Alias for the repository to remove.
        """
        if name in self.repo_dict:
            del self.repo_dict[name]
            logging.info(f"Repository '{name}' removed.")
            self.save_repo_dict()
        else:
            logging.warning(f"Repository '{name}' not found.")

    def get_repository_url(self, name):
        """
        Fetches the URL of a repository by its alias.

        Args:
            name (str): Alias of the repository.

        Returns:
            str: URL of the repository, or None if not found.
        """
        return self.repo_dict.get(name)

    def list_repositories(self):
        """
        Lists all repositories in the dictionary.
        """
        if self.repo_dict:
            for name, url in self.repo_dict.items():
                logging.info(f"{name}: {url}")
        else:
            logging.info("No repositories found.")
