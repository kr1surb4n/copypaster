import yaml
from copypaster.widgets.buttons import CopyButton
from copypaster.register import Register, register_instance
from copypaster import logger, PROJECT_DIR
from os import path as p


class Deck:
    """Deck of values for buttons"""

    def __init__(self):
        self.buttons = {}
        self.contents = None

    def load(self, path):
        with open(path) as f:
            self.contents = yaml.load(f.read(), Loader=yaml.FullLoader)

    def init_buttons(self):
        for _button in self.contents['buttons']:
            self.add_button(**_button)

    def add_button(self, **kwargs):
        c = CopyButton(**kwargs)
        self.buttons[c.id] = c
        return c

    def save(self, data, path):
        with open(path, 'w') as f:
            f.write(yaml.dump(data, encoding='utf-8'))

    def category(self):
        return self.contents['info']['category']

    def name(self):
        return self.contents['info']['name']

    def get_buttons(self):
        return self.buttons.values()


@register_instance
class Dirty(Deck):
    """Deck of values for buttons"""

    def __init__(self):
        Deck.__init__(self)
        self.load(p.join(PROJECT_DIR, "button_maps/dirty.yml"))
        self.init_buttons()


@register_instance
class Simple(Deck):
    """Deck of values for buttons"""

    def __init__(self):
        Deck.__init__(self)
        self.load(p.join(PROJECT_DIR, "button_maps/simple_buttons.yml"))
        self.init_buttons()


@register_instance
class Python(Deck):
    """Deck of values for buttons"""

    def __init__(self):
        Deck.__init__(self)
        self.load(p.join(PROJECT_DIR, "button_maps/python.yml"))
        self.init_buttons()


@register_instance
class Bash(Deck):
    """Deck of values for buttons"""

    def __init__(self):
        Deck.__init__(self)
        self.load(p.join(PROJECT_DIR, "button_maps/bash.yml"))
        self.init_buttons()


Simple(), Python(), Bash(), Dirty()
