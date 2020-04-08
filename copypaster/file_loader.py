import yaml
from copypaster.register import Register, register_instance
from copypaster import logger, PROJECT_DIR
from os import path as p


class Deck:
    """Deck of values for buttons"""
    contents = None

    def __init__(self):
        pass

    def load(self, path):
        with open(path) as f:
            self.contents = yaml.load(f.read(), Loader=yaml.FullLoader)

    def category(self):
        return self.contents['info']['category']

    def name(self):
        return self.contents['info']['name']

    def get_buttons(self):
        return self.contents['buttons']


@register_instance
class Simple(Deck):
    """Deck of values for buttons"""

    def __init__(self):
        self.load(p.join(PROJECT_DIR, "button_maps/simple_buttons.yml"))


@register_instance
class Python(Deck):
    """Deck of values for buttons"""

    def __init__(self):
        self.load(p.join(PROJECT_DIR, "button_maps/python.yml"))


@register_instance
class Bash(Deck):
    """Deck of values for buttons"""

    def __init__(self):
        self.load(p.join(PROJECT_DIR, "button_maps/bash.yml"))


Simple(), Python(), Bash()
