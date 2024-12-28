

import logging


logging.basicConfig(level=logging.INFO)


def print_k_launcher_documentation():
    """
    Prints the documentation for k_launcher in a single log statement.
    """
    documentation = """
    This is the documentation for the k_launcher.

    Usage:
        python k_launcher_wrapper.py [args*]

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
        python k_launcher_wrapper.py --info
        python k_launcher_wrapper.py --config dev -launch maya -add myPackage
        python k_launcher_wrapper.py --save devConfig
        python k_launcher_wrapper.py --load prodConfig

    Config Structure:
        config : package : context/path/file.rxt

    Class KWrapper:
        The KWrapper class manages the environment setup and execution of DCC software.
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
            - echo_settings(): Logs the current configuration settings for the KWrapper instance.
            - eval_rez_command(): Executes the generated `rez` command to set up the environment.
    """

    logging.info(documentation)

