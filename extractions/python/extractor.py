import glob
from collections import namedtuple
from os.path import dirname, splitext, isdir
import yaml

p = print

HTMLS = 'html'
OUTPUT = 'output'


PATTERN = HTMLS + "/**/*.html"

REGISTER = {}

from copy import copy

Button = namedtuple('Button', ['name', 'value', 'info', 'click_count'], defaults=["", 0])

class ButtonCard:
    def __init__(self, name, category):
        self.buttons = {}
        self.info = {
            'name': name,
            'category': " ".join(category)
        }
    
    def _to_dict_(self):
        return {
            'buttons': self.buttons,
            'info': self.info
        }


def extract_content(filename):
    """ 
        open file.
        find all objects with class: section
        
        for each section
            section_name = find_first_header in section
            catgory = [name, filename]

            extract all dt
            for each dt
                extract text
                use text as (value, name) for button

            extract all code
            for each code
                extract text
                use code as (value, name) for button

            yield section_name, ButtonCard(buttons = dt + code)
    """


    buttons = [Button(filename, filename)._asdict()]

    return buttons

def add_to_register(file, entry):

    _, folder, filename = entry


    name = splitext(filename)[0]

    if folder not in REGISTER:
        REGISTER[folder] = {}

    if name not in REGISTER[folder]:
        REGISTER[folder][name] = {}

    content = extract_content(filename)

    card = ButtonCard(name, [name])
    card.buttons = content

    REGISTER[folder][name] = card._to_dict_()

for file in glob.glob(PATTERN, recursive=True):
    if isdir(file):     # we dont do stuff to folders
        continue
    
    entry = file.split("/")

    if len(entry) == 2: # we don't like files in root folder
        continue

    add_to_register(file, entry)



"""
    Output parsed stuff
"""

#p(REGISTER)

dumps = yaml.dump(REGISTER)

p(dumps)