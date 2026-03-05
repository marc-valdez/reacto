"""
Configuration Module

Handles loading and accessing application configuration from configuration.ini
"""

from pathlib import Path
import configparser

class Config:
    def __init__(self, base_path: Path, config_file=Path('configuration.ini')):
        self.config = configparser.ConfigParser()
        config_path = base_path / config_file
        self.config.read(config_path)

    def get_boolean(self, section, key, fallback=False):
        return self.config.getboolean(section, key, fallback=fallback)

    def get_int(self, section, key, fallback=0):
        return self.config.getint(section, key, fallback=fallback)

    def get_float(self, section, key, fallback=0.0):
        return self.config.getfloat(section, key, fallback=fallback)

    def get_string(self, section, key, fallback=''):
        return self.config.get(section, key, fallback=fallback)

    def get_list(self, section, key, fallback=[], separator=','):
        value = self.get_string(section, key, '')
        if value:
            return [item.strip() for item in value.split(separator)]
        return fallback

    def get_int_list(self, section, key, fallback=[], separator=','):
        str_list = self.get_list(section, key, [], separator)
        return [int(item) for item in str_list] if str_list else fallback
