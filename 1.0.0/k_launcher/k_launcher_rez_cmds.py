

import argparse
import logging
import subprocess
import os
import sys
import k_config.main
import k_launcher_info
import k_launcher_rez_cmds
import k_launcher_utils


logging.basicConfig(level=logging.INFO)


class KLauncher_rez(k_launcher_rez_cmds.k_cmds):
    """
    KLauncher_rez class manages the environment setup and execution of DCC software.

    It handles various tasks such as setting and displaying configuration details,
    managing the environment variables using `rez`, and launching DCC software with
    the specified packages and settings.

    Attributes:
        config_set (str): The configuration set to use.
        package (str): The package to load with the environment.
        add_package (str): Additional packages to be added to the environment.
        dcc_launch (str): The DCC software to launch.
        save_config (str): The configuration to save.
        load_config (str): The configuration to load.
        grab_commande (list): List of packages to grab.
        switch_commande (list): List of packages to switch.
    """

    def echo_settings(self):
        """
        Logs the current configuration settings for the KLauncher_rez instance.

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
    parser.add_argument("-c", "--config", type=str, help="Set config")
    parser.add_argument("-p", "--package", type=str, help="Load package")
    parser.add_argument("-a", "--add", type=str, nargs="+", help="Add package")
    parser.add_argument("-lo", "--load", type=str, help="Load config")
    parser.add_argument("-s", "--save", type=str, help="Save config")
    parser.add_argument("-g", "--grab", type=str, nargs="+", help="Grab the package in LOCAL")
    parser.add_argument("-w", "--switch", type=str, nargs="+", help="Switch the packages to local version")
    parser.add_argument("-l", "--launch", type=str, help="Launch the DCC software")
    parser.add_argument("-r", "--release", type=str, help="Release the package on the PROD with the choosen version")
    parser.add_argument("-pr", "--package_release", type=str, help="Release the package on the PROD with the choosen version")

    args = parser.parse_args()
    wrapper = KLauncher_rez()

    try:
        if args.info:
            k_launcher_info.print_k_launcher_documentation_rez()

        elif args.release and args.prod_package:
            k_launcher_utils.release_package(args.release, args.prod_package)

        else:
            if args.echo:
                wrapper.echo_settings()
                k_config.main.print_rez_env_variables()

            if args.config:
                wrapper.config_set = args.config

            if args.package:
                wrapper.package = args.package

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

