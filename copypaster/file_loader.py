import yaml
from copypaster.widgets.buttons import CopyButton
from copypaster.widgets.buttons import NavigateButton
from copypaster import log


# This handles loading an dumping yaml files
class YamlFile:
    def __init__(self):
        self.contents = None

    def load(self, path):
        """Load file"""
        with open(path) as f:
            self.contents = yaml.load(f.read(), Loader=yaml.FullLoader)

    def save(self, data, path):
        """Save file"""
        log.debug("Saving file {}".format(path))
        with open(path, "w") as f:
            f.write(yaml.dump(data))


"""Deck of values for buttons"""


class Deck(YamlFile):

    _buttons = "buttons"
    _info = "info"
    _category = "category"
    _name = "name"

    def __init__(self, deck_file):
        super(Deck, self).__init__()
        self.buttons = {}
        self.path = deck_file
        self.load(self.path)
        self.init_buttons()

    def init_buttons(self):
        """Initialize buttons"""
        for _button in self.contents.get(self._buttons, []):
            try:
                self.add_button(**_button)
            except IndexError:
                pass  # yes, cause this value exists
            except AssertionError:
                log.error("No-value entry in deck {}".format(self.path))
                exit(1)

    def add_button(self, **kwargs):
        """Create button, add it to table and return it"""
        # log.debug(
        #     "Adding button {}  {}".format(kwargs.get("name", ""), kwargs.get("value", ""))
        # )
        c = self.buttons.get(str(kwargs.get("value", None)), None)
        if c:
            raise IndexError("There is such a value")

        c = CopyButton(**kwargs)

        self.buttons[c.value] = c
        return c

    def update_contents(self):
        """Update button IR"""
        self.contents["buttons"] = []
        for button in self.buttons.values():
            self.contents["buttons"] += [button.serialize()]

    def save_buttons(self):
        """Save buttons to file"""
        self.update_contents()
        self.save(self.contents, self.path)

    def category(self):
        return self.contents["info"]["category"]

    def name(self):
        return self.contents["info"]["name"]

    def get_buttons(self):
        return self.buttons.values()


# Deck that is on the branch of a collection
class BranchDeck(Deck):
    def __init__(self, name, deck_file):
        super(BranchDeck, self).__init__(deck_file)
        self.name = name

        # add NavigationButton(current=self, target=parent)
        # where target and current are BranchDeck
        self.one_up_button = None
        self.links_buttons = []

    def get_buttons(self):
        return [self.one_up_button] + self.links_buttons + list(self.buttons.values())


# Root collection deck
class NavigationDeck:
    def __init__(self, name, collection_name, link_names):
        self.name = name
        self.collection_name = collection_name

        self.buttons = {
            target_name: NavigateButton(  # is what we will display
                label=target_name,
                report_to=collection_name,
                current=name,
                target=target_name,
            )  # we take button grid
            for target_name in link_names
        }

    def get_buttons(self):
        return self.buttons.values()


def walk_branches(parent, parents, levels, tree_branch):  # and build tree representation

    if parent not in levels.keys():
        levels[parent] = []

    if tree_branch is None:
        log.debug("End of branch. Parent: %s" % parent)
        return None

    for branch_name, lower_branches in tree_branch.items():
        levels[parent] += [branch_name]
        parents[branch_name] = parent

        # here we go deeper
        walk_branches(branch_name, parents, levels, lower_branches)

    return None


# Collection
class DeckCollection(YamlFile):
    def __init__(self, name, collection_file):
        super(DeckCollection, self).__init__()
        self.name = name
        self.branch_decks = {}
        self.levels = {}
        self.parents = {}

        self.path = collection_file
        self.load(self.path)

        self.build_tree()

    def branches(self):
        return self.branch_decks.items()

    def build_tree(self):
        deck_list = self.contents.get("decks")

        tree = self.contents.get("tree")

        branch_decks = {}
        parents = {}
        levels = {}

        walk_branches("root", parents, levels, tree)  # and build branches list

        branch_decks["root"] = None
        parents["root"] = None

        for name, info in deck_list.items():
            deck_file = info["url"]
            deck = BranchDeck(name, deck_file)
            branch_decks[name] = deck

        self.branch_decks = branch_decks
        self.levels = levels
        self.parents = parents
