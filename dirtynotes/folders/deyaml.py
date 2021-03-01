"""The Walking Thread"""
import os
import threading, queue
from pathlib import Path
import configparser
from dataclasses import dataclass, asdict, astuple
import yaml
import string

kolejka_folder = queue.Queue()

CODE_PATH = "/home/kris/workshops/tools/copypaster/dirtynotes/folders/maps"
DECKS = "decks"

YAML_FILES = (
    '.yaml',
    '.yml',
)

CLICK_COUNT = "click_count"
INFO = "info"
NAME = "name"
VALUE = "value"
BUTTONS = "buttons"
CATEGORY = "category"
SNIPPET = "snippet"

CONTENT = "content"
INFO = "info"

MAX_FILENAME_LENGTH = 18

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


def read(entry):
    if entry.is_file():
        return ('file', f"name: {entry.name}", f"path: {entry.path}")

    if entry.is_dir():
        return ('dir', f"name: {entry.name}", f"path: {entry.path}")


class Snippet:
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


class YamlFile:
    def __init__(self, file_path):
        self.contents = None
        self.load(file_path)

    def load(self, path):
        """Load file"""
        with open(path) as f:
            self.contents = yaml.load(f.read(), Loader=yaml.FullLoader)

    def transform_into_snippets(self):
        for button in self.contents[BUTTONS]:
            yield Snippet().populate(button)


def extract_values(entry):
    """
    open file with yaml,

    walk over every element of `buttons`, translate it to configparser object

    every element has this:
      - click_count: 1
        info: 'First value'
        name: First
        value: "First"

    next, create folder with the name of the file,

    and under that folimport configparserder, write down all config parser objects
    """

    path = Path(entry.path)

    yaml_snippets = YamlFile(entry.path)

    snippet_folder = path.with_suffix('')
    snippet_folder.mkdir(parents=True, exist_ok=True)
    snippet_folder = str(snippet_folder)

    [snippet.save(snippet_folder) for snippet in yaml_snippets.transform_into_snippets()]


def deyaml(folder):
    # TODO: here i selfcan read a file with metadata

    with os.scandir(folder) as it:
        for entry in it:
            if entry.name.startswith('.'):
                continue

            if entry.is_dir():
                kolejka_folder.put(entry.path)

            if Path(entry.path).suffix not in YAML_FILES:
                continue

            extract_values(entry)


def worker():
    while True:
        folder = kolejka_folder.get()
        print(f'Working on folder: {folder}')

        deyaml(folder)
        print(f'Finished {folder}')
        kolejka_folder.task_done()


if __name__ == "__main__":
    # turn-on the worker thread
    threading.Thread(target=worker, daemon=True).start()

    kolejka_folder.put(CODE_PATH)

    # block until all tasks are done
    kolejka_folder.join()
    print('All work completed')
