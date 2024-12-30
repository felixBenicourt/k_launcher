

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
        -config : name of the config you're working on.
        -package : package to load with the environment.
        -add : additional packages to be added.
        -launch : launch the DCC software by name.
        -save : save the context/configuration.
        -load : load the saved context/configuration.
        -info : display information about the tool.
        -echo : display the current settings.
        -grab : grab the package in PROD to LOCAL.
        -switch : switch the package to the local version.
        -release : release the package in PROD with a specific version.
        -package_release : specify the version of the package to release in PROD.

    Example Launch Commands:
        python k_launcher_rez.py --info
        python k_launcher_rez.py --config dev -launch maya -add myPackage
        python k_launcher_rez.py --save devConfig
        python k_launcher_rez.py --load prodConfig

    Config Structure:
        config : package : context/path/file.rxt

    Class k_wrapper:
        The k_wrapper class manages the environment setup and execution of DCC software.
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
            - echo_settings(): Logs the current configuration settings for the k_wrapper instance.
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
        -clone_repo : Clone a Git repository.
            Parameters:
                - URL of the repository.
                - Local folder to clone into.
                - Optional name for the repository folder.

        -create_branch : Create a new branch in the specified repository.
            Parameters:
                - Path to the local folder containing the repository.
                - Name of the repository.
                - Name of the new branch.

        -checkout_branch : Switch to a specific branch in the repository.
            Parameters:
                - Path to the local folder containing the repository.
                - Name of the repository.
                - Name of the branch to checkout.

        -status : Show the status of the local repository.
            Parameters:
                - Path to the local folder containing the repository.
                - Name of the repository.

        -pull : Update the repository by pulling the latest changes from the remote.
            Parameters:
                - Path to the local folder containing the repository.
                - Name of the repository.

        -push : Push local commits to the remote repository.
            Parameters:
                - Path to the local folder containing the repository.
                - Name of the repository.

        -log : Display the commit log for the repository.
            Parameters:
                - Path to the local folder containing the repository.
                - Name of the repository.

        -tag : Tag the repository.
            Parameters:
                - Path to the local folder containing the repository.
                - Name of the repository.

        -history : Display the history of the repository.
            Parameters:
                - Path to the local folder containing the repository.
                - Name of the repository.

        -path : Folder path argument.

        -git_url : Git URL for cloning.
                
        -branch : Branch name.
                
        -msg : Message.

    Example Git Commands:
        python k_launcher_git.py -clone_repo https://example.com/repo.git /path/to/folder my-repo
        python k_launcher_git.py -create_branch /path/to/folder my-repo new-feature-branch
        python k_launcher_git.py -checkout_branch /path/to/folder my-repo main
        python k_launcher_git.py -status /path/to/folder my-repo
        python k_launcher_git.py -pull /path/to/folder my-repo
        python k_launcher_git.py -push /path/to/folder my-repo
        python k_launcher_git.py -log /path/to/folder my-repo

    Description:
        The Git functionality of `k_launcher` is designed to simplify the process of managing Git repositories. 
        It provides commands for common Git operations such as cloning repositories, creating and switching branches, 
        and synchronizing with remote repositories. These commands help streamline version control tasks 
        within the context of a production pipeline.
    """

    logging.info(documentation)

