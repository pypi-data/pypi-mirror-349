import json
import os
import logging
from dataclasses import fields, is_dataclass, MISSING
from typing import Type, TypeVar
from pathlib import Path

import yaml
from cryptography.fernet import Fernet

from mqtt_presence.app_data import Configuration
from mqtt_presence.app_config import AppConfiguration
from mqtt_presence.utils import Tools
from mqtt_presence.version import NAME


logger = logging.getLogger(__name__)

DEFAULT_PASSWORD = "h7F$kP2!mA93X@vL"
SECRET_KEY_FILE = "secret.key"
CONFIG_DATA_FILE = "config.json"
CONFIG_YAML_FILE = "config.yaml"


class ConfigHandler:
    def __init__(self, data_path: str = None):
        self.data_path = Path(data_path or Tools.get_data_path(NAME))
        self._secret_file = str(self.data_path / SECRET_KEY_FILE)
        self._config_file = str(self.data_path / CONFIG_DATA_FILE)
        self._yaml_file = str(self.data_path / CONFIG_YAML_FILE)
        self._fernet = Fernet(self._load_key())

        logger.info("ℹ️  Data initialized in path: %s", self.data_path)

    def _load_key(self):
        if not os.path.exists(self._secret_file):
            return self._generate_key()
        with open(self._secret_file, "rb") as file_secret:
            return file_secret.read()

    def _generate_key(self):
        dir_path = os.path.dirname(self._secret_file)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        key = Fernet.generate_key()
        with open(self._secret_file, "wb") as file_secret:
            file_secret.write(key)
        return key


    def check_yaml_config(self, config: AppConfiguration):
        if Tools.is_none_or_empty(config.app.mqtt.client_id):
            config.app.mqtt.client_id =  f"mqtt-presence_{Tools.get_pc_name()}"
        config.app.mqtt.client_id = Tools.sanitize_mqtt_topic(config.app.mqtt.client_id)


    # Load YAML file as AppConfiguration
    def load_config_yaml(self) -> AppConfiguration:
        config = None
        if os.path.exists(self._yaml_file):
            with open(self._yaml_file, "r", encoding="utf-8") as file_yaml:
                config = self._from_dict(AppConfiguration, yaml.safe_load(file_yaml))
            self.check_yaml_config(config)
            logger.info("✅ Configuration loaded from: %s", self._yaml_file)
        else:
            logger.warning("⚠️ No configuration file found in: %s. Create default.", self._yaml_file)
            config = AppConfiguration()
            self.check_yaml_config(config)
            with open(self._yaml_file, "w", encoding="utf-8") as f_out:
                yaml.dump(self._to_dict(config), f_out)
            logger.info("📝 Default configuration written to: %s", self._yaml_file)
        return config


    def check_config(self, config: Configuration):
        if Tools.is_none_or_empty(config.mqtt.homeassistant.device_name):
            config.mqtt.homeassistant.device_name = Tools.get_pc_name()
        if Tools.is_none_or_empty(config.mqtt.broker.prefix):
            config.mqtt.broker.prefix = Tools.sanitize_mqtt_topic(f"mqtt-presence/{config.mqtt.homeassistant.device_name}")


    # Load config file as Configuration
    def load_config(self) -> Configuration:
        config = None
        try:
            with open(self._config_file, "r", encoding="utf-8") as file_config:
                raw_data = json.load(file_config)
                config = self._from_dict(Configuration, raw_data)
        except FileNotFoundError:
            logger.warning("⚠️ File '%s' not found – use defaults.", {self._config_file})
            config = self._from_dict(Configuration, {})
            config.mqtt.broker.encrypted_password = self.get_encrypt_password(DEFAULT_PASSWORD)

        # check cofig
        self.check_config(config)
        return config



    def save_config(self, config: Configuration):
        def to_diff_dict(obj, default_obj):
            if is_dataclass(obj):
                result = {}
                for field in fields(obj):
                    value = getattr(obj, field.name)
                    default_value = getattr(default_obj, field.name)

                    # check recursiv for nested data
                    diff = to_diff_dict(value, default_value)
                    if diff != {}:
                        result[field.name] = diff
                return result
            if isinstance(obj, list):
                return obj if obj != default_obj else {}
            if isinstance(obj, dict):
                return obj if obj != default_obj else {}

            return obj if obj != default_obj else {}

        # create default instance to compare
        default_config = Configuration()

        #create a dictionary, with differences
        diff_dict = to_diff_dict(config, default_config)

        with open(self._config_file, "w", encoding="utf-8") as file:
            json.dump(diff_dict, file, indent=2)


    def get_encrypt_password(self, plain_password):
        return self._encrypt(plain_password)

    def get_decrypt_password(self, encrypted_password):
        return DEFAULT_PASSWORD if encrypted_password is None else self._decrypt(encrypted_password)

    def _encrypt(self, value):
        return self._fernet.encrypt(value.encode()).decode()

    def _decrypt(self, value):
        return self._fernet.decrypt(value.encode()).decode()


    # Typehelper for generic load
    T = TypeVar("T")
    def _from_dict(self, data_class: Type[T], data: dict) -> T:
        """
        Recursive conversion of a dictionary into a dataclass instance,
        with support for default values and nested classes.
        """
        kwargs = {}
        for field in fields(data_class):
            value = data.get(field.name, MISSING)
            if value is MISSING:
                # Field not found in yaml
                if field.default is not MISSING:
                    kwargs[field.name] = field.default
                elif field.default_factory is not MISSING:  # type: ignore
                    kwargs[field.name] = field.default_factory()  # type: ignore
                else:
                    raise ValueError(f"Feld '{field.name}' fehlt in Daten und hat keinen Defaultwert.")
            else:
                # Value not set → check if nested dataclass
                if is_dataclass(field.type) and isinstance(value, dict):
                    kwargs[field.name] = self._from_dict(field.type, value)
                else:
                    kwargs[field.name] = value

        return data_class(**kwargs)

    def _to_dict(self, obj):
        if is_dataclass(obj):
            return {field.name: self._to_dict(getattr(obj, field.name)) for field in fields(obj)}
        if isinstance(obj, list):
            return [self._to_dict(value) for value in obj]
        if isinstance(obj, dict):
            return {k: self._to_dict(value) for k, value in obj.items()}

        return obj
