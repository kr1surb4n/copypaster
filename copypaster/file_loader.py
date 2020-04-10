import yaml
from copypaster.widgets.buttons import CopyButton
from copypaster.register import Register, register_instance
from copypaster import logger, PROJECT_DIR
from os import path as p


class Deck:
    """Deck of values for buttons"""

    def __init__(self):
        self.buttons = {}
        self.path = ""
        self.contents = None

    def load(self, path):
        with open(path) as f:
            self.contents = yaml.load(f.read(), Loader=yaml.FullLoader)

    def init_buttons(self):
        try:
            for _button in self.contents.get('buttons', []):
                self.add_button(**_button)
        except IndexError:
            pass  # yes, cause this value exists

    def add_button(self, **kwargs):
        c = self.buttons.get(str(kwargs.get('value', None)), None)
        if c:
            raise IndexError('There is such value')

        c = CopyButton(**kwargs)
        self.buttons[c.value] = c
        return c

    def update_contents(self):
        self.contents['buttons'] = []
        for button in self.buttons.values():
            self.contents['buttons'] += [button.serialize()]

    def save_buttons(self):
        self.update_contents()
        self.save(self.contents, self.path)

    def save(self, data, path):
        with open(path, 'w') as f:
            f.write(yaml.dump(data))

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
        self.path = p.join(PROJECT_DIR, "button_maps/dirty.yml")
        self.load(self.path)
        self.init_buttons()


@register_instance
class Simple(Deck):
    """Deck of values for buttons"""

    def __init__(self):
        Deck.__init__(self)
        self.path = p.join(PROJECT_DIR, "button_maps/simple_buttons.yml")
        self.load(self.path)
        self.init_buttons()


@register_instance
class Python(Deck):
    """Deck of values for buttons"""

    def __init__(self):
        Deck.__init__(self)
        self.path = p.join(PROJECT_DIR, "button_maps/python.yml")
        self.load(self.path)
        self.init_buttons()


@register_instance
class Bash(Deck):
    """Deck of values for buttons"""

    def __init__(self):
        Deck.__init__(self)
        self.path = p.join(PROJECT_DIR, "button_maps/bash.yml")
        self.load(self.path)
        self.init_buttons()


Simple(), Python(), Bash(), Dirty()
