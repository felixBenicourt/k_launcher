

import argparse
import logging
import subprocess
import os
import sys
import k_config.main
import k_launcher_info
import k_launcher_cmds


logging.basicConfig(level=logging.INFO)


class KWrapper(k_launcher_cmds.k_cmds):

    def echo_settings(self):
        """Log the current settings for the wrapper."""
        logging.info(f"Config set: {self.config_set}")
        logging.info(f"Package: {self.package}")
        logging.info(f"Additional packages: {self.add_package}")
        logging.info(f"Launch DCC software: {self.dcc_launch}")
        logging.info(f"Save config: {self.save_config}")
        logging.info(f"Load config: {self.load_config}")
        logging.info(f"Grab packages: {self.grab_commande}")
        logging.info(f"Switch packages: {self.switch_commande}")


    def eval_rez_command(self):
        """Executes the generated `rez` command."""
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
    parser = argparse.ArgumentParser(description="scene_runner - A script to open scenes and run nodes.")
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

    args = parser.parse_args()
    wrapper = KWrapper()

    try:
        if args.info:
            k_launcher_info.print_k_launcher_documentation()
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

