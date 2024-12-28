

import logging
import os
import utils
from k_constants import CONSTANTS


logging.basicConfig(level=logging.INFO)


class k_cmds:
    def __init__(self, json_file_path=None):
        self.json_file_path = json_file_path
        self.config_set = None
        self.package = None
        self.save_config = None
        self.load_config = None
        self.grab_commande = None
        self.switch_commande = None
        self.dcc_launch = None

    def generate_rez_command(self):
        """
        Generates the full `rez` command for environment setup.

        Returns:
            str: The generated `rez` command.
        """
        command_parts = []
        package_list = []
        switch_prod_local = []
        launch_cmd = []

        self.add_package_to_command(command_parts)
        self.handle_grab_command(package_list, switch_prod_local)
        self.handle_switch_command(package_list, switch_prod_local)
        self.add_dcc_launch_to_command(launch_cmd)
        self.handle_load_config(command_parts)
        self.handle_save_config(command_parts)

        if not switch_prod_local:
            return f"rez env{''.join(command_parts)} {''.join(launch_cmd)}"
        else:
            rez_cmd = (
                f"set REZ_PACKAGES_PATH={switch_prod_local[0]} rez env"
                f"{''.join(package_list)} {''.join(launch_cmd)}"
            )
            return rez_cmd

    def add_package_to_command(self, command_parts):
        if self.package:
            command_parts.append(f" {self.package}")

    def handle_grab_command(self, package_list, switch_prod_local):
        if self.grab_commande:
            self.ensure_switch_prod_local(switch_prod_local)
            for package in self.grab_commande:
                try:
                    utils.grab_package_to_local(package)
                    package_list.append(f" {package}")
                except Exception as e:
                    logging.error(f"Failed to grab package {package}: {e}")

    def handle_switch_command(self, package_list, switch_prod_local):
        if self.switch_commande:
            self.ensure_switch_prod_local(switch_prod_local)
            for package in self.switch_commande:
                package_list.append(f" {package}")

    def ensure_switch_prod_local(self, switch_prod_local):
        if not switch_prod_local:
            switch_prod_local.append(
                f"{CONSTANTS.rootLocalFolder};{CONSTANTS.rootParseFolder} &&"
            )

    def add_dcc_launch_to_command(self, launch_cmd):
        if self.dcc_launch:
            launch_cmd.append(f"-- {self.dcc_launch}")

    def handle_load_config(self, command_parts):
        if self.load_config and self.json_file_path:
            try:
                json_data = utils.load_json_file(self.json_file_path)
                load_command = f" -i {json_data[self.config_set][self.load_config]}"
                command_parts.append(load_command)
            except KeyError:
                logging.error(f"Load config '{self.load_config}' not found in '{self.config_set}'.")
            except Exception as e:
                logging.error(f"Error loading config from {self.json_file_path}: {e}")

    def handle_save_config(self, command_parts):
        if self.save_config and self.package and self.json_file_path:
            try:
                json_data = utils.load_json_file(self.json_file_path)
                rxt_name_file = f"{self.config_set}-{self.package}.rxt"
                context_path = os.path.join(
                    CONSTANTS.root_folder, CONSTANTS.context_folder, rxt_name_file
                )

                if self.config_set in json_data:
                    json_data[self.config_set][self.package] = context_path
                else:
                    json_data[self.config_set] = {self.package: context_path}

                utils.save_json_file(self.json_file_path, json_data)
                save_command = f" -o {context_path}"
                command_parts.append(save_command)
            except Exception as e:
                logging.error(f"Error saving config to {self.json_file_path}: {e}")
