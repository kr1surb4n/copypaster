import yaml
import os
import threading, queue
from pathlib import Path
import configparser
import yaml
import string

from copypaster.widgets.buttons import Copy, GoTo
from copypaster.widgets.containers import ButtonTree, ButtonGrid
from copypaster import log

line = queue.Queue()
Decks = {}

BACKUP_FOLDER = "/home/kris/workshops/tools/copypaster/file_decks"

PATH_TO_SNIPPETS_FOLDER = os.environ.get('SNIPPETS_FOLDER', BACKUP_FOLDER)

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


class Snippet:
    def __init__(self):
        self.name = ""
        self.path = ""
        self.content = ""

    @property
    def file_name(self):
        return self.name.replace(" ", "-")

    def populate(self, snippet_dictionary):
        self.content = str(snippet_dictionary.get(VALUE, ""))
        self.name = str(snippet_dictionary.get(NAME, clean_name(self.content)))
        
        return self

    def load(self, path):
        self.path = path

        with open(path, 'r') as f:
            content = f.readlines()

        # f"# name: {self.name}\n"
        self.name = content[0][8:].strip()
        self.content = "".join(content[1:])

        return self

    def save(self):
        with open(self.path, 'w') as f:
            f.write(f"# name: {self.name} \n")
            f.write(self.content)

        return self


def button_made_from(entry):
    if entry.is_file():
        return Copy(Snippet().load(entry.path))

    if entry.is_dir():
        return GoTo(
                name=entry.name,
                position=os.path.dirname(entry.path),
                destination=entry.path,
            )
        
def walk(folder):
    global Decks
    global Decks_Data
    global line

    deck = ButtonGrid()

    parent_folder = os.path.dirname(folder)

    if folder != PATH_TO_SNIPPETS_FOLDER:
        up_to_parent = GoTo(
                    name="..",
                    position=folder,
                    destination=parent_folder
        )
        deck.append(up_to_parent)

    # TODO: here i can read a file with metadata

    with os.scandir(folder) as it:
        for entry in it:
            if entry.name.startswith('.'):
                continue

            if entry.is_dir():
                line.put(entry.path)

            deck.append(button_made_from(entry))

    deck.show()
    Decks[folder] = deck

def worker():
    global line

    while True:
        folder = line.get()
        log.debug(f'Working on folder: {folder}')

        walk(folder)
        log.debug(f'Finished {folder}')
        line.task_done()


def load_snippets():
    log.info('Loading snippets')
    global line
    global Decks

    # turn-on the worker thread
    threading.Thread(target=worker, daemon=True).start()

    line.put(PATH_TO_SNIPPETS_FOLDER)

    # block until all tasks are done
    line.join()

    return Decks, PATH_TO_SNIPPETS_FOLDER

    log.info('All snippets loaded')
