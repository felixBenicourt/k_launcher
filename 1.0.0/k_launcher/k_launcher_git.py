

import argparse
import logging
import os
import sys
from k_constants import CONSTANTS
import k_launcher_info
import k_launcher_git_cmd


logging.basicConfig(level=logging.INFO)


def parse_args():
    """
    Parses command-line arguments.

    This function uses argparse to define and parse the command-line arguments,
    providing the user with options for environment setup, Git repository management,
    configuration handling, and DCC software launching.

    Returns:
        argparse.Namespace: Parsed arguments and their values.
    """
    parser = argparse.ArgumentParser(description="scene_runner - A script to open scenes and run nodes.")
    
    parser.add_argument("-i", "--info", action="store_true", help="Display information about the tool.")

    parser.add_argument("-p", "--package", type=str, help="Load package")

    parser.add_argument("-gc", "--git_clone", action="store_true", help="GIT clone command.")
    parser.add_argument("-gf", "--git_fetch", action="store_true", help="GIT fetch command.")
    parser.add_argument("-gp", "--git_pull", action="store_true", help="GIT pull command.")
    parser.add_argument("-ch", "--git_check", action="store_true", help="GIT checkout command.")
    parser.add_argument("-co", "--git_commit", action="store_true", help="GIT checkout command.")
    parser.add_argument("-cr", "--git_create", action="store_true", help="GIT create command.")
    parser.add_argument("-gl", "--git_list", action="store_true", help="GIT list command.")
    parser.add_argument("-log", "--git_log", action="store_true", help="GIT log command.")
    parser.add_argument("-tag", "--git_tag", type=str, help="GIT tag command.")
    
    parser.add_argument("-pa", "--path", type=str, help="Folder path argument.")
    parser.add_argument("-gu", "--git_url", type=str, help="Git URL for cloning.")
    parser.add_argument("-b", "--branch", type=str, help="Branch name for checkout.")
    parser.add_argument("-m", "--msg", type=str, help="Message.")

    return parser.parse_args()


def main():
    """
    Main entry point for the script.

    This function parses command-line arguments, sets up the necessary environment, 
    handles Git operations, and manages the configuration and launch of DCC software. 
    Depending on the user's input, it either clones repositories, fetches updates, 
    or launches specific DCC software with the configured environment.
    """
    args = parse_args()
    wrapper = k_launcher_git_cmd.k_git_cmd()
    wrapper.load_repo_dict()

    try:
        if args.info:
            k_launcher_info.print_k_launcher_documentation_git()

        if args.git_clone:
            if args.git_url and args.path:
                wrapper.clone_repository(custom_url=args.git_url, path=args.path)
            else:
                logging.error("Missing required arguments for git clone: --git_url and --path.")

        if args.git_fetch:
            if args.package:
                wrapper.fetch_repository(
                    args.package,
                    os.path.join(args.path or CONSTANTS.rootLocalFolder, args.package),
                )
            else:
                logging.error("Missing required argument for git fetch: --package.")

        if args.git_pull:
            if args.package:
                wrapper.pull_repository(
                    args.package,
                    os.path.join(args.path or CONSTANTS.rootLocalFolder, args.package),
                )
            else:
                logging.error("Missing required argument for git pull: --package.")

        if args.git_check:
            if args.package and args.branch:
                wrapper.checkout_branch(
                    args.package,
                    os.path.join(args.path or CONSTANTS.rootLocalFolder, args.package),
                    args.branch,
                )
            else:
                logging.error("Missing required arguments for git checkout: --package and --branch.")

        if args.git_commit:
            if args.package and args.branch and args.msg:
                wrapper.commit_repository(
                    os.path.join(args.path or CONSTANTS.rootLocalFolder, args.package),
                    args.package,
                    args.msg,
                )
            else:
                logging.error("Missing required arguments for git commit: --package, --branch, and --msg.")

        if args.git_create:
            if args.package and args.git_tag:
                wrapper.create_branch(
                    args.package,
                    os.path.join(args.path or CONSTANTS.rootLocalFolder, args.package),
                    args.git_tag,
                )
            else:
                logging.error("Missing required arguments for git create branch: --package and --git_tag.")

        if args.git_list:
            if args.package:
                wrapper.list_remote_branches(
                    args.package,
                    os.path.join(args.path or CONSTANTS.rootLocalFolder, args.package),
                )
            else:
                logging.error("Missing required argument for git list: --package.")

        if args.git_log:
            if args.package:
                wrapper.show_commit_log(
                    args.package,
                    os.path.join(args.path or CONSTANTS.rootLocalFolder, args.package),
                )
            else:
                logging.error("Missing required argument for git log: --package.")

        if args.git_tag:
            if args.package and args.git_tag:
                wrapper.tag_repository(
                    args.package,
                    os.path.join(args.path or CONSTANTS.rootLocalFolder, args.package),
                    args.git_tag,
                )
            else:
                logging.error("Missing required arguments for git tag: --package and --git_tag.")

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
