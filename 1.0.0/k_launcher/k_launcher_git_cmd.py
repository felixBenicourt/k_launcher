

import logging
import git
import os
import subprocess
import k_launcher_repo


logging.basicConfig(level=logging.INFO)


class k_git_cmd(k_launcher_repo.k_repo):

    def start_ssh_agent(self):
        """Starts the ssh-agent if not already running and adds the SSH key."""
        if "SSH_AUTH_SOCK" not in os.environ:
            logging.info("Starting ssh-agent...")
            subprocess.run(["ssh-agent", "-s"], check=True)

        ssh_key_path = os.path.expanduser("~/.ssh/id_rsa")
        try:
            subprocess.run(["ssh-add", ssh_key_path], check=True)
            logging.info("SSH key added to agent.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to add SSH key to agent: {e}", exc_info=True)

    def fetch_repository(self, path_folder, name):
        """Fetches the latest changes from the remote repository."""
        repo_path = os.path.join(path_folder, name)
        if os.path.exists(repo_path):
            try:
                subprocess.run(["git", "fetch"], cwd=repo_path, check=True)
                logging.info(f"Fetched latest changes for '{name}'")
            except subprocess.CalledProcessError as e:
                logging.error(f"Error fetching repository '{name}': {e.stderr}", exc_info=True)
        else:
            logging.warning(f"Repository '{name}' not found locally.")

    def pull_repository(self, path_folder, name):
        """Pulls the latest changes from the remote repository."""
        repo_path = os.path.join(path_folder, name)
        if os.path.exists(repo_path):
            try:
                subprocess.run(["git", "pull"], cwd=repo_path, check=True)
                logging.info(f"Pulled latest changes for '{name}'")
            except subprocess.CalledProcessError as e:
                logging.error(f"Error pulling repository '{name}': {e.stderr}", exc_info=True)
        else:
            logging.warning(f"Repository '{name}' not found locally.")

    def checkout_branch(self, path_folder, name, branch_name):
        """Checks out a specific branch for the repository."""
        repo_path = os.path.join(path_folder, name)
        if os.path.exists(repo_path):
            try:
                subprocess.run(["git", "checkout", branch_name], cwd=repo_path, check=True)
                logging.info(f"Checked out branch '{branch_name}' for repository '{name}'")
            except subprocess.CalledProcessError as e:
                logging.error(f"Error checking out branch '{branch_name}' for '{name}': {e.stderr}", exc_info=True)
        else:
            logging.warning(f"Repository '{name}' not found locally.")

    def create_branch(self, path_folder, name, branch_name):
        """Creates a new branch and checks it out."""
        repo_path = os.path.join(path_folder, name)
        if os.path.exists(repo_path):
            try:
                subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo_path, check=True)
                logging.info(f"Created and checked out branch '{branch_name}' for repository '{name}'")
            except subprocess.CalledProcessError as e:
                logging.error(f"Error creating or checking out branch '{branch_name}' for '{name}': {e.stderr}", exc_info=True)
        else:
            logging.warning(f"Repository '{name}' not found locally.")

    def list_remote_branches(self, path_folder, name):
        """Lists all remote branches for the repository."""
        repo_path = os.path.join(path_folder, name)
        if os.path.exists(repo_path):
            try:
                result = subprocess.run(
                    ["git", "branch", "-r"], cwd=repo_path, check=True, capture_output=True, text=True
                )
                logging.info(f"Remote branches for '{name}':\n{result.stdout}")
            except subprocess.CalledProcessError as e:
                logging.error(f"Error listing remote branches for repository '{name}': {e.stderr}", exc_info=True)
        else:
            logging.warning(f"Repository '{name}' not found locally.")


    def clone_repository(self, name="", path=".", custom_url=""):
        """
        Clones a repository using its alias or a custom URL.

        Args:
            name (str): Alias of the repository to clone.
            path (str): Local path to clone the repository to.
            custom_url (str): Custom URL for the repository (optional).
        """
        if not custom_url:
            if not name:
                logging.error("No repository name or custom URL provided.")
                return
            url = self.get_repository_url(name)
        else:
            url = custom_url

        if not url:
            logging.error(f"Repository '{name}' not found or URL is invalid.")
            return

        if not os.path.exists(path):
            logging.info(f"Creating directory: {path}")
            os.makedirs(path)

        try:
            self.start_ssh_agent()

            logging.info(f"Cloning repository '{name}' from {url} to {path}")
            result = subprocess.run(
                ["git", "clone", url, path], 
                check=True, 
                capture_output=True, 
                text=True
            )
            logging.info(result.stdout)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error cloning repository '{name}': {e.stderr}", exc_info=True)
        except Exception as e:
            logging.error(f"Unexpected error occurred: {e}", exc_info=True)

    def show_commit_log(self, path_folder, name, n=5):
        """Shows the last n commits for a repository."""
        repo_path = os.path.join(path_folder, name)
        if os.path.exists(repo_path):
            try:
                result = subprocess.run(
                    ["git", "log", f"-n {n}"], cwd=repo_path, check=True, capture_output=True, text=True
                )
                logging.info(f"Last {n} commits for '{name}':\n{result.stdout}")
            except subprocess.CalledProcessError as e:
                logging.error(f"Error fetching commit log for repository '{name}': {e.stderr}", exc_info=True)
        else:
            logging.warning(f"Repository '{name}' not found locally.")

    def tag_repository(self, path_folder, name, tag_name):
        """Tags a repository with a specific tag."""
        repo_path = os.path.join(path_folder, name)
        if os.path.exists(repo_path):
            try:
                subprocess.run(["git", "tag", tag_name], cwd=repo_path, check=True)
                logging.info(f"Tagged repository '{name}' with '{tag_name}'")
            except subprocess.CalledProcessError as e:
                logging.error(f"Error tagging repository '{name}' with '{tag_name}': {e.stderr}", exc_info=True)
        else:
            logging.warning(f"Repository '{name}' not found locally.")

    def commit_repository(self, path_folder, name, message, add_all=False):
        """
        Commits changes in a repository.

        Args:
            path_folder (str): Path to the folder containing the repository.
            name (str): Alias of the repository.
            message (str): Commit message.
            add_all (bool): Whether to add all changes before committing. Defaults to False.
        """
        repo_path = os.path.join(path_folder, name)
        if os.path.exists(repo_path):
            try:
                if add_all:
                    subprocess.run(["git", "add", "--all"], cwd=repo_path, check=True)
                    logging.info(f"Staged all changes in repository '{name}'")

                subprocess.run(["git", "commit", "-m", message], cwd=repo_path, check=True)
                logging.info(f"Committed changes to repository '{name}' with message: '{message}'")
            except subprocess.CalledProcessError as e:
                logging.error(f"Error committing changes to repository '{name}': {e.stderr}", exc_info=True)
        else:
            logging.warning(f"Repository '{name}' not found locally.")

