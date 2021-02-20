import glob
from collections import namedtuple
from os.path import isdir, splitext
import yaml
import logging as l
from lxml import etree
from functools import partial
import parser

p = print

slices = lambda sausage: sausage.split("/")
file_xpath = lambda file: splitext(file)[0]

convert_to_text = partial(etree.tostring, method="text", encoding="UTF-8")


def read(filename):
    with open(filename, 'r') as f:
        return f.read()


# CONS
HTMLS = 'html'
OUTPUT = 'output'

PATTERN = HTMLS + "/**/*.html"

# representation of the extracted data
REGISTER = {}


# placeholder for deck data
class ButtonCard:
    def __init__(self, name, category):
        self.buttons = {}
        # fmt: off
        self.info = {
            'name': name,
            'category': " ".join(category)
        }
        # fmt: on

    def _to_dict_(self):
        # fmt: off
        return {
            'buttons': self.buttons,
            'info': self.info
        }
        # fmt: on


def collections_from_files():
    for file in glob.glob(PATTERN, recursive=True):
        if isdir(file):  # we dont do stuff to folders
            continue

        l.info("Working with file: ", file)

        if len(slices(file)) == 2:  # we don't like files in root folder
            l.info("Oh no! I don't like this file! It's in root!")
            continue

        content_tree = parser.load_tree(file)
        del content_tree
        yield file_xpath(file), parser.collection(content_tree)


if __name__ == "__main__":
    l.info("Running main")

    for xpath, collection in collections_from_files():
        collection_folder = xpath.replace("/", "_")
        collection_save_path = SAVE_PATH + "/" + collection_folder

        if path_not_exists(collection_save_path):
            mkdir(collection_save_path)

        id, name, decks, decks_tree = collection
        decks = [
            (deck.id, deck.name, deck.save_as_yaml(collection_save_path))
            for deck in decks
        ]

        REGISTER[xpath] = (id, name, decks_tree, decks)

    """
        Output parsed stuff
    """

    # p(REGISTER)

    dumps = yaml.dump(REGISTER)

    p(dumps)


def test_helpers():
    import pytest

    assert read(".test_target") == "test\n"

    assert 2 == len(slices("0/1"))
    assert 0 == int(slices("0/1")[0])
    assert 1 == int(slices("0/1")[1])
