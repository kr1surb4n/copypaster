from lxml import etree, html
from collections import namedtuple
import logging as l
from functools import partial
from os.path import isdir, splitext
import glob


# placeholder for button data
Button = namedtuple(
    'Button', ['name', 'value', 'info', 'click_count', 'tag'], defaults=["", 0, ""]
)


class Deck:

    @property
    def name(self):
        return self.info['name']

    @property
    def category(self):
        return self.info['category']

    def __init__(self, id, name, buttons):
        self.id = id
        self.buttons = buttons
        self.info = {
            'name': name,
            'category': ''
        }

slices = lambda sausage: sausage.split("/")

def convert_to_text(tree):
    return etree.tostring(tree, method="text", encoding="UTF-8").strip().decode()

FILENAME = "stdtypes.html"

def read(filename):
    with open(filename, 'r') as f:
        return f.read()

def main_title(tree):
    for h in tree.iter('h1'):
        return h.text
    return ""

def title(tree):
    for h in tree.iter('h1', 'h2', 'h3', 'h4'):
        return h.text
    return ""

def dt(tree):
    name = tree.get('id')
    text = convert_to_text(tree)
    del tree
    return name, text

def dd(tree):
    info = convert_to_text(tree)
    del tree
    return info

def code(tree):
    _code = convert_to_text(tree)
    del tree
    return Button(name=_code, 
    value=_code, 
    info="", 
    tag="code")


def definition(tree):
    dt_tree = tree.xpath("//dt")
    dd_tree = tree.xpath("//dd")
    name, text = dt(dt_tree[0])
    return Button(name=name, 
    value=text, 
    info=dd(dd_tree[0]), 
    tag=tree.attrib.get('class'))

def section(tree):
        # id value is a good dict key
        id = tree.get('id')

        #  section_name = find_first_header in section
        name = title(tree)

        # extract all dl
        definitions = [definition(dl) for dl in tree.xpath('//dl')]

        # extract all code
        codes = [code(pre) for pre in tree.xpath("//div[@class='highlight']/pre")]

        del tree
        return Deck(id, name, definitions + codes)


def walk_sections(tree):
    """
    I have a section, that has many more sections,
    """
    decks = {}
    deck_tree = {}

    id = '-----'

    for top_section_tree in tree.xpath("//*[@class='body']/*[@class='section']"):

        id = top_section_tree.get('id')  # id value is a good dict key

        level = {}
        for  section_tree in top_section_tree.xpath("//*[@class='section']"):
            deck = section(section_tree)
            decks[deck.id] = deck
            level[deck.id] = {}

        deck_tree[id] = level
    del tree
    return id, decks, deck_tree

def collection(tree):
    name = main_title(tree)

    id, decks, deck_tree = walk_sections(tree)

    if len(deck_tree) == 1:
        decks[id] = Deck(id, name, [])
 
    del tree
    return id, name, decks, deck_tree


def load_element(file):
    l.info("Reading file to tree")
    try:
        return html.fragment_fromstring(read(file))
    except Exception as e:
        l.debug(e)
        raise e

def load_tree(file):
    l.info("Reading file to tree")
    try:
        return etree.HTML(read(file))
    except Exception as e:
        l.debug(e)
        raise e

def test_dt():
    dt_tree = load_element('.dt')
    assert ("int.bit_length", "int.bit_length()¶") == dt(dt_tree)

def test_dd():
    dd_tree = load_element('.dd')
    info = dd(dd_tree)
    assert info.find("Return the number") == 0

def test_dl():
    dl_tree = load_element('.dl')
    for dl in dl_tree.xpath("//dl"):
        button = definition(dl)

    assert isinstance(button, Button)
    assert button.tag == "method"
    assert button.info.find("Return an array") == 0 
    assert button.value.find("int.to_bytes") == 0
    assert button.name == "int.to_bytes"

def test_code():
    code_tree = load_element('.code')
    for pre in code_tree.xpath("//div[@class='highlight']/pre"):
        button = code(pre)

    assert isinstance(button, Button)
    assert button.tag == "code"
    assert button.info == ""

    assert button.value.find(">>> int.from_bytes") == 0
    assert button.name.find(">>> int.from_bytes") == 0

def test_section():
    section_tree = load_element('.section')
    
    for tree in section_tree.xpath("//*[@class='section']"):
        deck = section(tree)

    assert isinstance(deck, Deck)
    assert deck.id == "mapping-types-dict"
    assert deck.name == "Mapping Types — "
    assert deck.category == ""
    assert len(deck.buttons) == 28

def test_title():
    content_tree = load_tree(FILENAME)
    assert content_tree is not None

    # h3
    assert "Navigation" == title(content_tree)
    
    # h1
    h1 = content_tree.xpath("//*[@id='built-in-types']")
    assert "Built-in Types" == title(h1[0])
    assert "Built-in Types" == main_title(content_tree)

    # h2
    h2 = content_tree.xpath('//*[@id="truth-value-testing"]')
    assert "Truth Value Testing" == title(h2[0])

def test_collection():
    content_tree = load_tree(FILENAME)
    assert content_tree is not None

    id, name, decks, decks_tree = collection(content_tree)
    assert id == "built-in-types"
    assert name == "Built-in Types"
    assert decks[id].name == name
    assert len(decks.keys()) == 49
    assert 'built-in-types' in decks_tree
    assert len(decks_tree) == 1
    assert len(decks_tree['built-in-types']) == 49


def useless_code():

    decks = {}
    tree = {}

    for file in folder:
        file_tree = load_tree(file)

        _, folder, filename = slices(file)
        name = splitext(filename)[0]

        _, file_decks, file_decks_tree = collection(file_tree)

        decks.update(file_decks)
        tree.update({name: file_decks_tree})



