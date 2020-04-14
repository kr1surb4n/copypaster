import yaml
from copypaster.widgets.buttons import CopyButton
from copypaster.register import Register, register_instance
from copypaster import logger, PROJECT_DIR
from os import path as p


class Deck:
    """Deck of values for buttons"""

    def __init__(self, deck_file):
        self.buttons = {}
        self.contents = None
        self.path = deck_file
        self.load(self.path)
        self.init_buttons()

    def load(self, path):
        """Load file"""
        with open(path) as f:
            self.contents = yaml.load(f.read(), Loader=yaml.FullLoader)

    def save(self, data, path):
        """Save file"""
        with open(path, 'w') as f:
            f.write(yaml.dump(data))

    def init_buttons(self):
        """Initialize buttons"""
        for _button in self.contents.get('buttons', []):
            try:
                self.add_button(**_button)
            except IndexError:
                pass  # yes, cause this value exists
            except AssertionError:
                logger.error("No-value entry in deck {}".format(self.path))
                exit(1)

    def add_button(self, **kwargs):
        """Create button, add it to table and return it"""
        c = self.buttons.get(str(kwargs.get('value', None)), None)
        if c:
            raise IndexError('There is such value')

        c = CopyButton(**kwargs)

        self.buttons[c.value] = c
        return c

    def update_contents(self):
        """Update button IR"""
        self.contents['buttons'] = []
        for button in self.buttons.values():
            self.contents['buttons'] += [button.serialize()]

    def save_buttons(self):
        """Save buttons to file"""
        self.update_contents()
        self.save(self.contents, self.path)

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
        Deck.__init__(self, p.join(PROJECT_DIR, "button_maps/dirty.yml"))


Dirty()
