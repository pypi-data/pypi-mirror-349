import configparser
import os
import signal
import sys
from typing import Dict, Any
import json
from vyomcloudbridge.utils.logger_setup import setup_logger

logger = setup_logger(name=__name__, show_terminal=False)


class Configs:
    @staticmethod
    def get_machine_config() -> Dict[str, Any]:
        config = configparser.ConfigParser()
        config_path = "/etc/vyomcloudbridge/machine.conf"
        if os.path.exists(config_path):
            config.read(config_path)
            try:
                return {
                    "machine_id": int(config["MACHINE"]["machine_id"]),  # in use
                    "machine_uid": config["MACHINE"]["machine_uid"],  # in use
                    "machine_name": config["MACHINE"]["machine_name"],
                    "machine_model_id": int(config["MACHINE"]["machine_model_id"]),
                    "machine_model_name": config["MACHINE"]["machine_model_name"],
                    "machine_model_type": config["MACHINE"]["machine_model_type"],
                    "organization_id": int(
                        config["MACHINE"]["organization_id"]
                    ),  # in use
                    "organization_name": config["MACHINE"]["organization_name"],
                    "ssh_port": int(config["MACHINE"]["ssh_port"]),  # in use
                    "access_public_key": config["MACHINE"][
                        "access_public_key"
                    ],  # in use
                    "access_private_key": config["MACHINE"][
                        "access_private_key"
                    ],  # in use
                }
            except (KeyError, ValueError):
                logger.error(f"Failed to parse configuration from {config_path}")
        logger.warning(
            f"Using default values because config file {config_path} was not found or is invalid"
        )
        return {
            "machine_id": None,  # in use
            "machine_uid": "",  # in use
            "machine_name": "",
            "machine_model_id": None,
            "machine_model_name": "",
            "machine_model_type": "",
            "organization_id": None,  # in use
            "organization_name": "",
            "ssh_port": None,  # in use
            "access_public_key": "",  # in use
            "access_private_key": "",  # in use
        }


def main():
    machine_config = Configs.get_machine_config()
    machine_id = machine_config.get("machine_id", "-") or "-"
    machine_uid = machine_config.get("machine_uid", "-") or "-"
    machine_name = machine_config.get("machine_name", "-") or "-"
    machine_model_id = machine_config.get("machine_model_id", "-") or "-"
    machine_model_name = machine_config.get("machine_model_name", "-") or "-"
    machine_model_type = machine_config.get("machine_model_type", "-") or "-"
    organization_id = machine_config.get("organization_id", "-") or "-"
    organization_name = machine_config.get("organization_name", "-") or "-"
    ssh_port = machine_config.get("ssh_port", "-") or "-"
    access_public_key = machine_config.get("access_public_key", "-") or "-"
    access_private_key = machine_config.get("access_private_key", "-") or "-"

    print("machine_id:", machine_id)
    print("machine_uid:", machine_uid)
    print("machine_name:", machine_name)
    print("machine_model_id:", machine_model_id)
    print("machine_model_name:", machine_model_name)
    print("machine_model_type:", machine_model_type)
    print("organization_id:", organization_id)
    print("organization_name:", organization_name)
    print("ssh_port:", ssh_port)
    print("access_public_key:", access_public_key)
    print("access_private_key:", access_private_key)


if __name__ == "__main__":
    main()
