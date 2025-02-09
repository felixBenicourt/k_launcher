
# regular import
import logging
import subprocess
import k_launcher_utils
import k_launcher_repo
import os

# custom packages import
from k_constants import CONSTANTS


logging.basicConfig(level=logging.INFO)


class k_cmds(k_launcher_repo.k_repo):
    """
    A class that encapsulates commands for generating and managing `rez` environment setup commands.
    
    This class provides functionality to configure and generate the `rez` command, handle packages, 
    and manage configuration settings for DCC software launching. The generated command includes 
    parameters for packages, configuration loading/saving, environment setup, and launching DCC software.
    """
    def __init__(self, json_file_path=None):
        """
        Initializes the k_cmds instance with optional configuration parameters.
        
        Args:
            json_file_path (str, optional): Path to the JSON file used for configuration loading/saving.
        """
        self.json_file_path = json_file_path
        self.config_set = None
        self.set_package = None
        self.save_config = None
        self.load_config = None
        self.grab_commande = None
        self.switch_commande = None
        self.dcc_launch = None
        self.add_package = None


    def generate_rez_command(self):
        """
        Generates the full `rez` command for environment setup.

        This method assembles various parts of the `rez` command based on the instance attributes,
        including environment variables, package handling, configuration loading/saving, and DCC software launch.
        
        Returns:
            str: The generated `rez` command.
        """
        command_parts = []
        launch_config = []
        package_list = []
        switch_prod_local = []
        launch_cmd = []

        self.set_package_to_command(command_parts)
        self.add_package_to_command(command_parts)
        self.handle_grab_command(package_list, switch_prod_local)
        self.handle_switch_command(package_list, switch_prod_local)
        self.add_dcc_launch_to_command(launch_cmd)

        if self.save_config:
            self.save_rez_environment(
                os.path.join(
                    CONSTANTS.root_folder, 
                    CONSTANTS.context_folder, 
                    CONSTANTS.environments, 
                    f"{self.save_config}.rxt"
                ), 
                    f"rez env{' '.join(command_parts)}"
            )

        if self.load_config:
            launch_config.append(
                os.path.join(
                    CONSTANTS.root_folder, 
                    CONSTANTS.context_folder, 
                    CONSTANTS.environments, 
                    f"{self.load_config}.rxt"
                )
            )

        if self.load_config:
            rez_cmd = f"rez-env --input {' '.join(launch_config)} {''.join(launch_cmd)}"
        elif not switch_prod_local:
            rez_cmd = f"rez env{' '.join(command_parts)} {''.join(launch_cmd)}"
        else:
            rez_cmd = (
                f"set REZ_PACKAGES_PATH={switch_prod_local[0]} rez env"
                f"{''.join(package_list)} {''.join(launch_cmd)}"
            )

        logging.info(f"Generated command: {rez_cmd}")
        return rez_cmd


    def set_package_to_command(self, command_parts):
        if self.set_package:
            command_parts.append(f" {self.set_package}")


    def add_package_to_command(self, command_parts):
        """
        Adds the specified package to the `rez` command.
        
        Args:
            command_parts (list): The list to which the package will be added in the command.
        """
        if self.add_package:
            command_parts.append(' '.join(self.add_package))
            

    def handle_grab_command(self, package_list, switch_prod_local):
        """
        Handles the grab command by ensuring packages are grabbed locally.
        
        Args:
            package_list (list): The list to which the grabbed packages will be added in the command.
            switch_prod_local (list): The list that tracks whether packages need to be switched to local.
        """
        if self.grab_commande:
            self.ensure_switch_prod_local(switch_prod_local)
            for package in self.grab_commande:
                try:
                    k_launcher_utils.grab_package_to_local(package)
                    package_list.append(f" {package}")
                except Exception as e:
                    logging.error(f"Failed to grab package {package}: {e}")


    def handle_switch_command(self, package_list, switch_prod_local):
        """
        Handles the switch command by ensuring packages are switched to local versions.
        
        Args:
            package_list (list): The list to which the switched packages will be added in the command.
            switch_prod_local (list): The list that tracks whether packages need to be switched to local.
        """
        if self.switch_commande:
            self.ensure_switch_prod_local(switch_prod_local)
            for package in self.switch_commande:
                package_list.append(f" {package}")


    def ensure_switch_prod_local(self, switch_prod_local):
        """
        Ensures that the switch to the local folder is applied when necessary.
        
        Args:
            switch_prod_local (list): The list that tracks whether packages need to be switched to local.
        """
        if not switch_prod_local:
            switch_prod_local.append(
                f"{CONSTANTS.rootLocalFolder};{CONSTANTS.rootParseFolder} &&"
            )


    def add_dcc_launch_to_command(self, launch_cmd):
        """
        Adds the command to launch the DCC software to the `rez` command.
        
        Args:
            launch_cmd (list): The list to which the launch command will be added.
        """
        if self.dcc_launch:
            launch_cmd.append(f"-- {self.dcc_launch}")
        else:
            logging.warning("DCC launch command is not set.")


    def save_rez_environment(self, config_path, command_parts):
        """
        Saves the current Rez environment to a specified context file.

        Args:
            config_path (str): Full path to save the Rez context file.
            command_parts (list): List of commands for logging or further processing.
        """
        try:
            base_command = f"{command_parts} --output {config_path}"
            subprocess.run(base_command, shell=True, check=True)
            logging.info(f"Environment saved successfully at {config_path}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to save Rez environment: {e}")

