

import logging


logging.basicConfig(level=logging.INFO)


def print_k_launcher_documentation_rez():
    """
    Prints the documentation for k_launcher in a single log statement.
    """
    documentation = """
    This is the documentation for the k_launcher Rez Functionality.

    Usage:
        python k_launcher_rez.py [args*]

    Arguments (args*):
        -c, --config : name of the config you're working on.
        -co, --context : display the current context.
        -p, --package : package to load with the environment.
        -a, --add : additional packages to be added.
        -l, --launch : launch the DCC software by name.
        -s, --save : save the context/configuration.
        -lo, --load : load the saved context/configuration.
        -i, --info : display information about the tool.
        -e, --echo : display the current settings.
        -g, --grab : grab the package in PROD to LOCAL.
        -w, --switch : switch the package to the local version.
        -r, --release : chosen LOCAL package to release.
        -pr, --prod_release : chosen version of the package to release on PROD.

    Example Launch Commands:
        python k_launcher_rez.py --info
        python k_launcher_rez.py --config dev --launch maya --add myPackage
        python k_launcher_rez.py --save devConfig
        python k_launcher_rez.py --load prodConfig

    Config Structure:
        config : package : context/path/file.rxt

    Class KLauncher_rez:
        The KLauncher_rez class manages the environment setup and execution of DCC software.
        It handles various tasks such as setting and displaying configuration details,
        managing the environment variables using `rez`, and launching DCC software with
        the specified packages and settings.

        Attributes:
            - config_set (str): The configuration set to use.
            - package (str): The main package to load with the environment.
            - add_package (str): Additional packages to be added to the environment.
            - dcc_launch (str): The DCC software to launch.
            - save_config (str): The configuration to save.
            - load_config (str): The configuration to load.
            - grab_commande (list): List of packages to grab.
            - switch_commande (list): List of packages to switch.

        Methods:
            - echo_settings(): Logs the current configuration settings for the KLauncher_rez instance.
            - eval_rez_command(): Executes the generated `rez` command to set up the environment.
    """

    logging.info(documentation)


def print_k_launcher_documentation_git():
    """
    Prints the documentation for k_launcher in a single log statement.
    """
    documentation = """
    Documentation for k_launcher Git Functionality:

    Usage:
        python k_launcher_git.py [args*]

    Arguments (args*):
        -i, --info : Display information about the tool.
        -p, --package : Load package.
        -co, --context : Display the current context.
        -gc, --git_clone : Clone a Git repository.
            Parameters:
                - URL of the repository.
                - Local folder to clone into.
                - Optional name for the repository folder.
        -gf, --git_fetch : Fetch the latest changes from the remote repository.
            Parameters:
                - Path to the local folder containing the repository.
                - Name of the repository.
        -gp, --git_pull : Update the repository by pulling the latest changes from the remote.
            Parameters:
                - Path to the local folder containing the repository.
                - Name of the repository.
        -ch, --git_check : Switch to a specific branch in the repository.
            Parameters:
                - Path to the local folder containing the repository.
                - Name of the repository.
                - Name of the branch to checkout.
        -c, --git_commit : Commit changes to the repository.
            Parameters:
                - Path to the local folder containing the repository.
                - Name of the repository.
                - Commit message.
        -cr, --git_create : Create a new branch in the specified repository.
            Parameters:
                - Path to the local folder containing the repository.
                - Name of the repository.
                - Name of the new branch.
        -gl, --git_list : List remote branches of the repository.
            Parameters:
                - Path to the local folder containing the repository.
                - Name of the repository.
        -log, --git_log : Display the commit log for the repository.
            Parameters:
                - Path to the local folder containing the repository.
                - Name of the repository.
        -t, --git_tag : Tag the repository.
            Parameters:
                - Path to the local folder containing the repository.
                - Name of the repository.
        -gh, --history : Display the history of the repository.
            Parameters:
                - Path to the local folder containing the repository.
                - Name of the repository.
        -pa, --path : Folder path argument.
        -gu, --git_url : Git URL for cloning.
        -b, --branch : Branch name.
        -m, --msg : Commit message.

    Description:
        The Git functionality of `k_launcher` is designed to simplify the process of managing Git repositories. 
        It provides commands for common Git operations such as cloning repositories, creating and switching branches, 
        and synchronizing with remote repositories. These commands help streamline version control tasks 
        within the context of a production pipeline.
    """

    logging.info(documentation)

