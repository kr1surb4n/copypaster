# -*- coding: utf-8 -*-
import os
import configparser

from app import log
from app.register import register_instance


@register_instance
class Config:
    def __init__(self, config_file=None):
        """Load the config file.

        Order of resoliving the path of config file:

        1. Path in env variable KR15_APP_CONFIG
        2. From ~/.config/app.conf file by default
        3. From provided config file path
        4. It will load without conifg
        """
        self.cfg = None

        log.info("Initializing config...")
        config_env = os.environ.get("KR15_APP_CONFIG", None)

        if config_env is not None:
            log.info("loading with config_env")
            config = config_env
        elif config_file is not None:
            log.info("loading with config file")
            config = config_file
        else:
            log.info("load without config")
            config = "i_am_non_existent"

        self.cfg = configparser.ConfigParser()
        self.cfg.read(config)

    def load_config_file(self, filename):
        self.cfg.read(filename)

