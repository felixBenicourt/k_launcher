import argparse
import logging
import subprocess
import dcc_packages
import utils
from k_constants import CONSTANTS
import os
import k_config.main


logging.basicConfig(level=logging.INFO)


class k_wrapper:
    """
    This class wraps functionality to handle the environment setup for launching DCC software
    with specified packages. It manages loading and saving configurations, generating the proper
    `rez` commands, and executing them to set up the environment for DCC tools.

    Attributes:
        config_set (str): The configuration set to use.
        package (str): The package to load with the environment.
        launch_dcc (str): The DCC software to launch.
        save (bool): Flag to save the configuration.
        load (str): The specific config to load.
        add_package (list): List of additional packages to add.
        is_dcc_launch (bool): Whether a DCC software is selected for launch.
        json_file_path (str): Path to the JSON configuration file.
        dcc_packages (list): List of DCC packages for the selected software.
        commande (str): The full `rez` command generated for environment setup.
    """
    
    def __init__(self, config, add=None, launch=None, save=None, load=None, pa=None):
        """
        Initializes the k_wrapper class with the provided parameters and sets up the environment.

        Args:
            config (str): The configuration set to use.
            add (list, optional): Additional packages to add.
            launch (str, optional): DCC software to launch.
            save (bool, optional): Flag to save configuration.
            load (str, optional): Config to load.
            pa (str, optional): Package to load with the environment.
        """
        self.config_set = config
        self.package = pa
        self.launch_dcc = launch
        self.save = save
        self.load = load
        self.add_package = add
        self.is_dcc_launch = self.launch_dcc in CONSTANTS.dcc_list
        self.json_file_path = os.path.join(CONSTANTS.root_folder, CONSTANTS.context_folder, 'configs.json')
        self.dcc_packages = self.get_dcc_packages()
        self.commande = self.generate_rez_commande()

    def get_dcc_packages(self):
        """
        Retrieves the list of DCC packages for the selected DCC software.

        Returns:
            list: A list of DCC packages if a DCC software is selected, otherwise None.
        """
        if self.launch_dcc:
            list_pack = dcc_packages.packages_assignation[self.launch_dcc]
            return list_pack
        else:
            return None

    def echo_settings(self):
        """
        Logs the current settings, including the environment, selected DCC software, added packages,
        and generated command.
        """
        logging.info("environement : %s", self.config_set)
        logging.info("launch : %s", self.launch_dcc)
        logging.info("packages added : %s", self.add_package)
        logging.info("is a dcc launched : %s", self.is_dcc_launch)
        logging.info("dcc packages : %s", self.dcc_packages)
        logging.info("save : %s", self.save)
        logging.info("load : %s", self.load)
        logging.info("main package : %s", self.package)
        logging.info("commande : %s", self.commande)

    def load_env_json(self):
        """
        Loads the environment configuration from the JSON file.

        Returns:
            dict: The JSON data loaded from the configuration file.
        """
        json_data = utils.load_json_file(self.json_file_path)
        logging.info("environement context path : %s", self.json_file_path)
        return json_data

    def save_env_json(self, data):
        """
        Saves the provided data to the JSON configuration file.

        Args:
            data (dict): The data to save in the configuration file.
        """
        utils.save_json_file(self.json_file_path, data)

    def generate_rez_commande(self):
        """
        Generates the full `rez` command for environment setup based on the provided settings.

        Returns:
            str: The generated `rez` command.
        """
        packages_cmd = ""
        add_pack_cmd = ""
        dcc_launch_cmd = ""
        package = ""
        save_commande = ""
        load_commande = ""

        if self.package:
            package = f" {self.package}"
        if self.dcc_packages:
            packages_cmd = f" {' '.join(self.dcc_packages)}"
        if self.add_package:
            add_pack_cmd = f" {' '.join(self.add_package)}"
        if self.is_dcc_launch:
            dcc_launch_cmd = f" {self.launch_dcc} -- {self.launch_dcc}"
        if self.load:
            json_data = self.load_env_json()
            load_commande = f" -i {json_data[self.config_set][self.load]}"
        if self.save and self.package:
            json_data = self.load_env_json()
            rxt_name_file = f"{self.config_set}-{self.package}.rxt"
            context_path = os.path.join(CONSTANTS.root_folder, CONSTANTS.context_folder, rxt_name_file)

            if self.package in json_data or self.config_set in json_data:
                json_data[self.config_set][self.package] = context_path
            else:
                json_data[self.config_set] = {self.package: context_path}

            self.save_env_json(json_data)
            save_commande = f" -o {context_path}"

        return f"rez env{package}{packages_cmd}{add_pack_cmd}{dcc_launch_cmd}{save_commande}{load_commande}"

    def eval_rez_commande(self, additional_args):
        """
        Executes the generated `rez` command and logs the output.

        Args:
            additional_args (list): Additional arguments to pass to the command.
        """
        logging.info(additional_args)

        try:
            result = subprocess.run(self.commande, shell=True, check=True, capture_output=True, text=True)
            k_config.main.print_rez_env_variables()

            config_data = utils.load_json_file(self.json_file_path)
            if config_data:
                for key, value in config_data.items():
                    logging.info(f"{key}: {value}")

            logging.info("Rez command executed successfully.")
            logging.info("Output:")
            logging.info(result.stdout)

        except subprocess.CalledProcessError as e:
            logging.info("Error executing Rez command:", e)
            logging.info("Output:")
            logging.info(e.stdout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch DCC software with specified package.")
    parser.add_argument("config", help="Config")
    parser.add_argument("-add", "--add", nargs='+', help="Add package.")
    parser.add_argument("-launch", "--launch", help="Launch DCC software.")
    parser.add_argument("-save", "--save", action="store_true", help="Save config.")
    parser.add_argument("-load", "--load", help="Load config.")
    parser.add_argument("-pa", "--pa", help="Load package.")
    args, additional_args = parser.parse_known_args()

    add = args.add if args.add else []

    wrapper = k_wrapper(args.config, args.add, args.launch, args.save, args.load, args.pa)
    wrapper.echo_settings()
    wrapper.eval_rez_commande(additional_args)



