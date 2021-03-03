import os
import string
from copypaster.widgets.buttons import CopyButton
from copypaster.widgets.buttons import NavigateButton
from copypaster import log

join = os.path.join

rules = str.maketrans('', '', string.punctuation)

name_counter = 1

def placeholder_name():
    _lock = threading.Lock()
    with _lock:
        global name_counter
        name = f"snippet_{name_counter}"
        name_counter += 1

    return name

def clean_name(name):
    name.strip()
    name = name.translate(rules)

    if len(name) > MAX_FILENAME_LENGTH:
        name = name[:MAX_FILENAME_LENGTH]

    if len(name) == 0:
        name = placeholder_name()

    return name

class Snippet:
    """A unit of snippet"""

    def __init__(self):
        self.name = ""
        self.content = ""

    @property
    def file_name(self):
        return self.name.replace(" ", "-")

    def populate(self, button):
        self.content = str(button.get(VALUE, ""))
        self.name = str(button.get(NAME, button.get(VALUE, "")))
        self.name = clean_name(self.name)

        return self

    def load(self, path):
        with open(path, 'r') as f:
            content = f.readlines()

        # f"# name: {self.name}\n"
        self.name = content[0][8:].strip()
        self.content = "".join(content[1:])

        return self

    def save(self, path):
        with open(join(path, self.file_name), 'w') as f:
            f.write(f"# name: {self.name} \n")
            f.write(self.content)

        return self
