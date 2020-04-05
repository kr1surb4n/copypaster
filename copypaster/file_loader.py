import yaml
from copypaster.register import Register, register_instance
from copypaster import logger, PROJECT_DIR
from os import path


@register_instance
class Deck:
    """Deck of values for buttons"""
    contents = None

    def __init__(self):
        with open(path.join(PROJECT_DIR, "button_maps/simple_buttons.yml")) as f:
            self.contents = yaml.load(f.read(), Loader=yaml.FullLoader)

    def category(self):
        return self.contents['info']['category']

    def name(self):
        return self.contents['info']['name']

    def get_buttons(self):
        return self.contents['buttons']


loader = Deck()
