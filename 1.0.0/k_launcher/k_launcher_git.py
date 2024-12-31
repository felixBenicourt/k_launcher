

import argparse
import logging
import sys
from k_constants import CONSTANTS
import k_launcher_info
import k_launcher_git_cmd
import k_launcher_context
import k_launcher_id


logging.basicConfig(level=logging.INFO)


class KLauncher_git(k_launcher_git_cmd.k_git_cmd,
                    k_launcher_context.PackageContextManager
                    ):
    """
    A class to manage Git operations within the context of a pipeline environment.

    Attributes:
        package (str): The package name to operate on.
        branch (str): The Git branch name.
        path (str): The file path for Git operations.
        session_id (str): Unique identifier for the current terminal session.
    """

    def __init__(self):
        """
        Initializes the KLauncher_git object, setting up the session ID, repository dictionary,
        and loading the context from a saved file.
        """
        self.package = None
        self.branch = None
        self.path = None
        self.session_id = str(k_launcher_id.get_terminal_pid())
        self.load_repo_dict()
        self.load_data_context()

    def parse_args(self):
        """
        Parses command-line arguments for Git operations.

        Returns:
            argparse.Namespace: Parsed arguments object.
        """
        parser = argparse.ArgumentParser(description="k_launcher - A script to manage git in the pipeline context.")

        parser.add_argument("-i", "--info", action="store_true", help="Display information about the tool.")
        parser.add_argument("-p", "--package", type=str, help="Load package")
        parser.add_argument("-co", "--context", action="store_true", help="Display the current context")
        parser.add_argument("-gc", "--git_clone", action="store_true", help="GIT clone command.")
        parser.add_argument("-gf", "--git_fetch", action="store_true", help="GIT fetch command.")
        parser.add_argument("-gp", "--git_pull", action="store_true", help="GIT pull command.")
        parser.add_argument("-ch", "--git_check", action="store_true", help="GIT checkout command.")
        parser.add_argument("-c", "--git_commit", action="store_true", help="GIT commit command.")
        parser.add_argument("-cr", "--git_create", action="store_true", help="GIT create branch command.")
        parser.add_argument("-gl", "--git_list", action="store_true", help="GIT list command.")
        parser.add_argument("-log", "--git_log", action="store_true", help="GIT log command.")
        parser.add_argument("-t", "--git_tag", type=str, help="GIT tag command.")
        parser.add_argument("-gh", "--history", action="store_true", help="GIT history command.")
        parser.add_argument("-pa", "--path", type=str, help="Folder path argument.")
        parser.add_argument("-gu", "--git_url", type=str, help="Git URL for cloning.")
        parser.add_argument("-b", "--branch", type=str, help="Branch name.")
        parser.add_argument("-m", "--msg", type=str, help="Message.")

        return parser.parse_args()

    def set_arguments(self, args):
        """
        Sets command-line arguments as instance variables and updates the context file accordingly.

        Args:
            args (argparse.Namespace): Parsed command-line arguments.
        """
        if args.package:
            self.package = args.package
            self.save_data_context("package", self.package)
        if args.branch:
            self.branch = args.branch
            self.save_data_context("branch", self.branch)
        if "path" in self.load_data_context():
            if args.path:
                self.path = args.path
                self.save_data_context("path", args.path)
            else:
                self.path = self.load_data_context()["path"]
        else:
            if args.path:
                self.save_data_context("path", args.path)
            else:
                self.path = args.path or CONSTANTS.rootLocalFolder
                self.save_data_context("path", self.path)

    def execute_commands(self, args):
        """
        Executes Git operations based on parsed command-line arguments.

        Args:
            args (argparse.Namespace): Parsed command-line arguments.
        """
        try:
            if args.info:
                k_launcher_info.print_k_launcher_documentation_git()

            if args.context:
                self.get_data_context()

            if args.git_clone:
                if args.git_url and args.path:
                    self.clone_repository(custom_url=args.git_url, path=args.path)
                elif self.package and self.path:
                    self.clone_repository(name=self.package, path=self.path)
                else:
                    logging.error("Missing required arguments for git clone: --git_url and --path or a valid context (package/path).")
                    sys.exit(1)

            if args.git_fetch:
                if self.package and self.path:
                    self.fetch_repository(self.package, self.path, self.package)
                else:
                    logging.error("Missing package or path for git fetch.")
                    sys.exit(1)

            if args.git_pull:
                if self.package and self.path:
                    self.pull_repository(self.package, self.path)
                else:
                    logging.error("Missing package or path for git pull.")
                    sys.exit(1)

            if args.git_check:
                if self.package and self.branch:
                    self.checkout_branch(self.path, self.package, self.branch)
                else:
                    logging.error("Missing package or branch for git checkout.")
                    sys.exit(1)

            if args.git_commit and args.msg:
                if self.package and self.path:
                    self.commit_repository(self.path, self.package, args.msg)
                else:
                    logging.error("Missing package or path for git commit.")
                    sys.exit(1)

            if args.git_create:
                if self.package and args.git_tag:
                    self.create_branch(self.package, self.path, self.package, args.git_tag)
                else:
                    logging.error("Missing package or git tag for git branch creation.")
                    sys.exit(1)

            if args.git_list:
                if self.package and self.path:
                    self.list_remote_branches(self.path, self.package)
                else:
                    logging.error("Missing package or path for git list remote branches.")
                    sys.exit(1)

            if args.git_log:
                if self.package and self.path:
                    self.show_commit_log(self.path, self.package)
                else:
                    logging.error("Missing package or path for git log.")
                    sys.exit(1)

            if args.history:
                if self.package and self.path:
                    self.list_repository_history(self.path, self.package)
                else:
                    logging.error("Missing package or path for git history.")
                    sys.exit(1)

            if args.git_tag and args.git_tag:
                if self.package and self.path:
                    self.tag_repository(self.path, self.package, args.git_tag)
                else:
                    logging.error("Missing package or path for git tag.")
                    sys.exit(1)

        except Exception as e:
            logging.error(f"An error occurred: {e}", exc_info=True)
            sys.exit(1)


def main():
    """
    Main function to initialize and run the KLauncher_git.
    """
    launcher = KLauncher_git()
    args = launcher.parse_args()
    launcher.set_arguments(args)
    launcher.execute_commands(args)


if __name__ == "__main__":
    main()

