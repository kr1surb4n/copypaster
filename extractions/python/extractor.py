import glob
from collections import namedtuple
from os.path import isdir, splitext
import yaml
import logging as l
from lxml import etree
from functools import partial

p = print

slices = lambda sausage: sausage.split("/")

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


# placeholder for button data
Button = namedtuple(
    'Button', ['name', 'value', 'info', 'click_count', 'tag'], defaults=["", 0, ""]
)

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


def extract_content(file):
    """

    catgory = [name, filename]


    for each dt
        extract text
        use text as (value, name) for button


    for each code
        extract text
        use code as (value, name) for button

    yield section_name, ButtonCard(buttons = dt + code)
    """

    _, _, filename = slices(file)

    l.info("Reading file to tree")
    try:
        content_tree = etree.HTML(read(file))
    except Exception as e:
        l.debug(e)
        raise e

    # for each section
    for deck in content_tree.xpath("//*[@class='section']"):

        #  section_name = find_first_header in section
        title = ""
        for h in deck.iter('h1', 'h2', 'h3', 'h4'):
            title = h.text
            break

        # extract all dt
        definitions = [convert_to_text(dt) for dt in deck.xpath('//dt')]

        # extract all code
        codes = [
            convert_to_text(code) for code in deck.xpath("//div[@class='highlight']/pre")
        ]

    return [Button(filename, filename)._asdict()]


def add_to_register(file):
    l.info("Begining content extraction")

    _, folder, filename = slices(file)

    name = splitext(filename)[0]

    if folder not in REGISTER:
        REGISTER[folder] = {}

    if name not in REGISTER[folder]:
        REGISTER[folder][name] = {}

    content = extract_content(file)

    # TODO this will go somewhere else soon
    card = ButtonCard(name, [name])
    card.buttons = content

    # TODO this also will go away
    REGISTER[folder][name] = card._to_dict_()


if __name__ == "__main__":
    l.info("Running main")

    for file in glob.glob(PATTERN, recursive=True):
        if isdir(file):  # we dont do stuff to folders
            continue

        l.info("Working with file: ", file)

        if len(slices(file)) == 2:  # we don't like files in root folder
            l.info("Oh no! I don't like this file! It's in root!")
            continue

        add_to_register(file)

    """
        Output parsed stuff
    """

    # p(REGISTER)

    dumps = yaml.dump(REGISTER)

    # p(dumps)
