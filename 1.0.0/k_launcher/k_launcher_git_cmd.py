
# regular import
import logging
import git
import os
import json
import subprocess

# custom packages import
import k_launcher_repo
from k_constants import CONSTANTS


logging.basicConfig(level=logging.INFO)


PACKAGE_CONFIG_FILE = os.path.join(CONSTANTS.root_folder,CONSTANTS.context_folder, CONSTANTS.git_user_config)


class k_git_cmd(k_launcher_repo.k_repo):
    """
    A class for managing Git repositories using subprocess commands.
    Extends the `k_repo` class from `k_launcher_repo`.
    """

    def start_ssh_agent(self):
        """
        Starts the SSH agent if not already running and adds the default SSH key.

        The method ensures that the SSH agent is active and the SSH private key
        located at `~/.ssh/id_rsa` is added to the agent.

        Logs:
            - Info: When the SSH agent is started or the key is added.
            - Error: If adding the key to the agent fails.
        """
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
        """
        Fetches the latest changes from the remote repository.

        Args:
            path_folder (str): Path to the parent folder containing the repository.
            name (str): Name of the repository to fetch changes for.

        Logs:
            - Info: When the fetch operation is successful.
            - Warning: If the repository is not found locally.
            - Error: If fetching fails due to Git errors.
        """
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
        """
        Pulls the latest changes from the remote repository and merges them.

        Args:
            path_folder (str): Path to the parent folder containing the repository.
            name (str): Name of the repository to pull changes for.

        Logs:
            - Info: When the pull operation is successful.
            - Warning: If the repository is not found locally.
            - Error: If pulling fails due to Git errors.
        """
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
        """
        Checks out the specified branch in a Git repository.
        
        Args:
            path_folder (str): Path to the parent folder containing the repository.
            name (str): Name of the repository folder.
            branch_name (str): The branch name to check out or create.
        """
        repo_path = os.path.join(path_folder, name)
        logging.info(f"Repository path: {repo_path}")
        
        if not os.path.exists(repo_path):
            logging.warning(f"Repository '{name}' not found at path '{repo_path}'.")
            return
        
        if not os.path.exists(os.path.join(repo_path, ".git")):
            logging.error(f"'{repo_path}' is not a valid Git repository.")
            return

        try:
            subprocess.run(["git", "fetch", "--all"], cwd=repo_path, check=True)

            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repo_path,
                stdout=subprocess.PIPE,
                text=True,
                check=True
            )

            if status_result.stdout.strip():
                logging.warning("Uncommitted changes detected. Stashing changes before checkout.")
                subprocess.run(["git", "stash"], cwd=repo_path, check=True)

            result = subprocess.run(
                ["git", "branch", "--list", branch_name],
                cwd=repo_path,
                stdout=subprocess.PIPE,
                text=True,
                check=True
            )
            
            if not result.stdout.strip():
                logging.warning(f"Branch '{branch_name}' does not exist. Creating it.")
                subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo_path, check=True)
            else:
                subprocess.run(["git", "checkout", branch_name], cwd=repo_path, check=True)
            
            logging.info(f"Successfully checked out branch '{branch_name}' for repository '{name}'.")
        
        except subprocess.CalledProcessError as e:
            logging.error(
                f"Error managing branch '{branch_name}' for repository '{name}': {e.stderr or e}",
                exc_info=True
            )
        except Exception as e:
            logging.error(
                f"Unexpected error occurred while managing branch '{branch_name}' for repository '{name}': {e}",
                exc_info=True
            )


    def create_branch(self, path_folder, name, branch_name):
        """
        Creates a new branch in the repository and switches to it.

        Args:
            path_folder (str): Path to the parent folder containing the repository.
            name (str): Name of the repository to create the branch.
            branch_name (str): Name of the branch to create and switch to.

        Logs:
            - Info: When the branch is successfully created and checked out.
            - Warning: If the repository is not found locally.
            - Error: If creating or switching branches fails.
        """
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
        """
        Lists all remote branches in the repository.

        Args:
            path_folder (str): Path to the parent folder containing the repository.
            name (str): Name of the repository to list remote branches.

        Logs:
            - Info: When the remote branches are successfully listed.
            - Warning: If the repository is not found locally.
            - Error: If listing remote branches fails.
        """
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
        Clones a repository from a given alias or custom URL.

        Args:
            name (str): Alias of the repository to clone.
            path (str): Local path to clone the repository to.
            custom_url (str): Custom URL for the repository (optional).

        Logs:
            - Info: When the repository is successfully cloned.
            - Error: If cloning fails or the alias/URL is invalid.
        """
        repo_path = os.path.join(path, name)
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

        if not os.path.exists(repo_path):
            logging.info(f"Creating directory: {repo_path}")
            os.makedirs(repo_path)

        try:
            self.start_ssh_agent()

            logging.info(f"Cloning repository '{name}' from {url} to {repo_path}")
            result = subprocess.run(
                ["git", "clone", url, repo_path], 
                check=True, 
                capture_output=True, 
                text=True
            )
            logging.info(result.stdout)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error cloning repository '{name}': {e.stderr}", exc_info=True)
        except Exception as e:
            logging.error(f"Unexpected error occurred: {e}", exc_info=True)


    def commit_repository(self, path_folder, name, message, add_all=False, push=True, remote="origin"):
        """
        Commits changes in the repository.

        Args:
            path_folder (str): Path to the parent folder containing the repository.
            name (str): Name of the repository to commit changes.
            message (str): Commit message.
            add_all (bool): Whether to stage all changes before committing (default: False).

        Logs:
            - Info: When the changes are successfully committed.
            - Warning: If the repository is not found locally.
            - Error: If committing fails.
        """

        if os.path.exists(PACKAGE_CONFIG_FILE):
            with open(PACKAGE_CONFIG_FILE, "r") as file:
                try:
                    configInfo = json.load(file)
                except json.JSONDecodeError:
                    configInfo = None

        repo_path = os.path.join(path_folder, name)

        if os.path.exists(repo_path) and configInfo:
            try:
                subprocess.run(
                    ["git", "config", "user.name", configInfo["user_name"]],
                    cwd=repo_path,
                    check=True
                )
                subprocess.run(
                    ["git", "config", "user.email", configInfo["user_mail"]],
                    cwd=repo_path,
                    check=True
                )

                if add_all:
                    logging.info(f"Staging all changes in repository '{name}'...")
                    subprocess.run(["git", "add", "--all"], cwd=repo_path, check=True)
                else:
                    logging.info(f"Staging modified files in repository '{name}'...")
                    subprocess.run(["git", "add", "."], cwd=repo_path, check=True)

                logging.info(f"Committing changes in repository '{name}' with message: '{message}'...")
                subprocess.run(["git", "commit", "-m", message], cwd=repo_path, check=True)

                if push:
                    logging.info(f"Determining the current branch in repository '{name}'...")
                    branch = subprocess.check_output(
                        ["git", "branch", "--show-current"], cwd=repo_path
                    ).strip().decode()

                    logging.info(f"Pushing branch '{branch}' to remote '{remote}'...")
                    subprocess.run(["git", "push", remote, branch], cwd=repo_path, check=True)
                    logging.info(f"Successfully pushed branch '{branch}' to remote '{remote}' for repository '{name}'")
                else:
                    logging.info(f"Push skipped for repository '{name}' (push=False)")
    
            except subprocess.CalledProcessError as e:
                logging.error(
                    f"Error committing/pushing changes to repository '{name}': {e.stderr or str(e)}",
                    exc_info=True
                )
        else:
            logging.warning(f"Repository '{name}' not found locally.")


    def show_commit_log(self, path_folder, name, n=5):
        """
        Displays the last `n` commits in the repository.

        Args:
            path_folder (str): Path to the parent folder containing the repository.
            name (str): Name of the repository to show the commit log.
            n (int): Number of commits to display (default: 5).

        Logs:
            - Info: When the commit log is successfully fetched.
            - Warning: If the repository is not found locally.
            - Error: If fetching the commit log fails.
        """
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
        """
        Tags the repository with a specified tag.

        Args:
            path_folder (str): Path to the parent folder containing the repository.
            name (str): Name of the repository to tag.
            tag_name (str): Name of the tag to apply.

        Logs:
            - Info: When the repository is successfully tagged.
            - Warning: If the repository is not found locally.
            - Error: If tagging fails.
        """
        repo_path = os.path.join(path_folder, name)
        if os.path.exists(repo_path):
            try:
                subprocess.run(["git", "tag", tag_name], cwd=repo_path, check=True)
                logging.info(f"Tagged repository '{name}' with '{tag_name}'")
            except subprocess.CalledProcessError as e:
                logging.error(f"Error tagging repository '{name}' with '{tag_name}': {e.stderr}", exc_info=True)
        else:
            logging.warning(f"Repository '{name}' not found locally.")


    def list_repository_history(self, path_folder, name):
        """
        Lists the complete history of the repository, including commits and tags.

        Args:
            path_folder (str): Path to the parent folder containing the repository.
            name (str): Name of the repository to list the history.

        Logs:
            - Info: When the commit history and tags are successfully fetched.
            - Warning: If the repository is not found locally.
            - Error: If fetching the history fails.
        """
        repo_path = os.path.join(path_folder, name)
        if os.path.exists(repo_path):
            try:
                commit_log = subprocess.run(
                    ["git", "log", "--oneline", "--decorate"], 
                    cwd=repo_path, 
                    check=True, 
                    capture_output=True, 
                    text=True
                )
                logging.info(f"Commit history for '{name}':\n{commit_log.stdout}")

                tags = subprocess.run(
                    ["git", "tag"], 
                    cwd=repo_path, 
                    check=True, 
                    capture_output=True, 
                    text=True
                )
                if tags.stdout.strip():
                    logging.info(f"Tags for '{name}':\n{tags.stdout}")
                else:
                    logging.info(f"No tags found for repository '{name}'")

            except subprocess.CalledProcessError as e:
                logging.error(f"Error listing history for repository '{name}': {e.stderr}", exc_info=True)
        else:
            logging.warning(f"Repository '{name}' not found locally.")


