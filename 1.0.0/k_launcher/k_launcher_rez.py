

import argparse
import logging
import subprocess
import os
import sys
import k_config.main
import k_launcher_info
import k_launcher_rez_cmds
import k_launcher_utils
import k_launcher_context
import k_launcher_id
from k_constants import CONSTANTS


logging.basicConfig(level=logging.INFO)


class KLauncher_rez(k_launcher_rez_cmds.k_cmds,
                    k_launcher_context.PackageContextManager,
                    ):
    """
    KLauncher_rez class manages the environment setup and execution of DCC software.

    It handles various tasks such as setting and displaying configuration details,
    managing the environment variables using `rez`, and launching DCC software with
    the specified packages and settings.

    Attributes:
        config (str): The configuration set to use.
        package (str): The package to load with the environment.
        add (str): Additional packages to be added to the environment.
        launch (str): The DCC software to launch.
        save (str): The configuration to save.
        load (str): The configuration to load.
        grab (list): List of packages to grab.
        switch (list): List of packages to switch.
    """

    def __init__(self):
        super().__init__()
        """
        Initializes the KLauncher_rez object, setting up the session ID, repository dictionary,
        and loading the context from a saved file.
        """
        self.add_package = None
        self.switch = None
        self.package = None
        self.grab = None
        self.path = None
        
        self.session_id = str(k_launcher_id.get_terminal_pid())
        
        self.load_repo_dict()
        self.load_data_context()

    def set_arguments(self, args):
        """
        Sets command-line arguments as instance variables and updates the context file accordingly.

        Args:
            args (argparse.Namespace): Parsed command-line arguments.
        """
        if args.package:
            self.package = args.package
            self.save_data_context("package", self.package)
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

    def echo_settings(self):
        """
        Logs the current configuration settings for the k_wrapper instance.

        This function logs important settings such as the configuration set,
        the main package, the additional packages, the DCC software to launch, 
        and any other saved settings.

        Example log output:
            Config set: dev
            Package: myPackage
            Additional packages: extraPackage1 extraPackage2
            Launch DCC software: maya
            Save config: devConfig
            Load config: prodConfig
            Grab packages: package1 package2
            Switch packages: package3 package4
        """
        logging.info(f"Config set: {self.config_set}")
        logging.info(f"Package: {self.package}")
        logging.info(f"Additional packages: {self.add_package}")
        logging.info(f"Launch DCC software: {self.dcc_launch}")
        logging.info(f"Save config: {self.save_config}")
        logging.info(f"Load config: {self.load_config}")
        logging.info(f"Grab packages: {self.grab_commande}")
        logging.info(f"Switch packages: {self.switch_commande}")

    def eval_rez_command(self):
        """
        Executes the generated `rez` command to set up the environment.

        This method generates a `rez` command using the instance's settings
        and executes it using the `subprocess` module. If the command fails,
        the error message is logged.

        It handles the environment setup and manages launching the required 
        DCC software with the specified configuration.

        Raises:
            subprocess.CalledProcessError: If the `rez` command fails to execute.
        """
        logging.info(f"Attributes: grab_commande={getattr(self, 'grab_commande', None)}")
        try:
            env = os.environ.copy()
            command = f"{self.generate_rez_command()}"
            logging.info(f"Executing command: {command}")
            subprocess.run(command, shell=True, check=True, capture_output=True, text=True, env=env)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing command: {e}")
            logging.error("Command Output:")
            logging.error(e.stdout)


def main():
    """
    Main entry point for the script.

    Parses command-line arguments and uses the `KLauncher_rez` class to manage 
    the configuration settings, execute the `rez` commands, and launch 
    the appropriate DCC software based on the provided options.
    """

    parser = argparse.ArgumentParser(description="k_launcher_rez - A script to manage packages and env with rez.")
    parser.add_argument("-i", "--info", action="store_true", help="Display information")
    parser.add_argument("-e", "--echo", action="store_true", help="Display current settings")
    parser.add_argument("-co", "--context", action="store_true", help="Display the current context")
    parser.add_argument("-c", "--config", type=str, help="Set config")
    parser.add_argument("-p", "--package", type=str, help="Load package")
    parser.add_argument("-a", "--add", type=str, nargs="+", help="Add package")
    parser.add_argument("-pa", "--path", type=str, help="Folder path argument.")
    parser.add_argument("-lo", "--load", type=str, help="Load config")
    parser.add_argument("-s", "--save", type=str, help="Save config")
    parser.add_argument("-g", "--grab", type=str, nargs="+", help="Grab the package in LOCAL")
    parser.add_argument("-w", "--switch", type=str, nargs="+", help="Switch the packages to local version")
    parser.add_argument("-l", "--launch", type=str, help="Launch the DCC software")
    parser.add_argument("-r", "--release", type=str, help="Chosen LOCAL package to release")
    parser.add_argument("-pr", "--prod_release", type=str, help="Chosen version of the package to release on PROD")
    


    args = parser.parse_args()
    wrapper = KLauncher_rez()
    wrapper.set_arguments(args)

    try:
        if args.info:
            k_launcher_info.print_k_launcher_documentation_rez()

        if args.context:
            wrapper.get_data_context()

        elif args.release and args.prod_release:
            src_path = os.path.join(CONSTANTS.rootLocalFolder, args.release.split("-")[0], args.release.split("-")[-1])
            dest_path = os.path.join(CONSTANTS.rootParseFolder, args.prod_release.split("-")[0], args.prod_release.split("-")[-1])
            if os.path.exists(src_path) and not os.path.exists(dest_path):
                k_launcher_utils.release_package(src_path, dest_path)

        else:
            if args.echo:
                wrapper.echo_settings()
                k_config.main.print_rez_env_variables()

            if args.config:
                wrapper.config_set = args.config

            if args.package:
                wrapper.set_package = args.package

            if args.add:
                wrapper.add_package = " ".join(args.add)

            if args.load:
                wrapper.load_config = args.load

            if args.save:
                wrapper.save_config = args.save

            if args.grab:
                wrapper.grab_commande = args.grab

            if args.switch:
                wrapper.switch_commande = args.switch

            if args.launch:
                wrapper.dcc_launch = args.launch

            wrapper.eval_rez_command()

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

