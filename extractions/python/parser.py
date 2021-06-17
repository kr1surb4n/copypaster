from lxml import etree, html
from collections import namedtuple
import logging as l
import logging as log
from functools import partial
from os.path import isdir, splitext, join
from os import mkdir
import os
import sys
import glob
import yaml
import threading, queue
import string

tasks = queue.Queue()

rules = str.maketrans('', '', string.punctuation)
join = os.path.join

name_counter = 1

MAX_FILENAME_LENGTH = 20
FILENAME = "stdtypes.html"
THING = "¶"


def placeholder_name():
    _lock = threading.Lock()
    with _lock:
        global name_counter
        name = f"snippet_{name_counter}"
        name_counter += 1

    return name


def clean_folder(name: str):
    if not name:
        name = "no name"

    name = name.translate(rules)
    name = name.strip()
    name = name.rstrip("——")
    return name.strip()


def clean_name(name: str):

    if name is None:
        name = "None"

    name.strip()
    name.strip(THING)

    if len(name) > MAX_FILENAME_LENGTH:
        name = name[:MAX_FILENAME_LENGTH]

    return name


def clean_filename(name: str):

    if name is None:
        name = "None"

    name = name.strip()
    name = name.strip(THING)
    name = name.translate(rules)

    if len(name) > MAX_FILENAME_LENGTH:
        name = name[:MAX_FILENAME_LENGTH]

    if len(name) == 0:
        name = placeholder_name()

    return name.replace(" ", "-")


class Snippet:
    def __init__(self, name="", content="", path=""):
        self.path = ""

        self.name = clean_name(name)
        self.filename = clean_filename(name)

        self.content = content.strip(THING)
        self.prefix_filename_with(path)

    def prefix_filename_with(self, path_to_containing_folder):
        self.path = os.path.join(path_to_containing_folder, self.filename)

    def populate(self, snippet_dictionary: dict):
        self.content = str(snippet_dictionary.get(VALUE, ""))
        self.name = str(snippet_dictionary.get(NAME, clean_name(self.content)))

        return self

    def load(self, path: str):
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

    def delete(self):
        os.unlink(self.path)


slices = lambda sausage: sausage.split("/")


def text_from(tree):
    return etree.tostring(tree, method="text", encoding="UTF-8").strip().decode()


def read(filename):
    with open(filename, 'r') as f:
        return f.read()


def write(filename, content):
    with open(filename, 'w') as f:
        f.write(content)


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
    value = text_from(tree)

    if name:
        return name.strip(), value
    else:
        return value, value


def dd(tree):
    info = text_from(tree)
    return info


def a_refs(tree):
    _code = tree.get('title')

    # name, value, info, tag
    return _code, _code


def code(tree):
    _code = text_from(tree)

    # name, value, info, tag
    return _code, _code


def definition(tree):
    dt_tree = [dt for dt in tree.iter("dt")][0]
    dd_tree = [dd for dd in tree.iter("dd")][0]
    name, value = dt(dt_tree)

    # for future, yes, i know
    info = dd(dd_tree)
    tag = tree.attrib.get('class')

    return name, value


def subdefinition(tree):
    name, value = definition(tree)

    # cause, in subdefinition the id
    # has the full code and the value is
    # only function name
    return name, name


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


def slashes2under(path):
    return path.replace("/", "_")


def work_on_section(section, path):
    # id value is a good dict key
    section_id = section.get('id')

    name = title(section)

    print(f"path: {path}, name: {name}")

    if not path:
        path = ""

    try:
        new_path = os.path.join(path, clean_folder(name))
        os.mkdir(new_path)
    except FileExistsError as e:
        print(e)

    try:
        gists_path = join(new_path, "gists")
        os.mkdir(gists_path)
    except FileExistsError as e:
        print(e)

    try:
        codes_path = join(new_path, "codes")
        os.mkdir(codes_path)
    except FileExistsError as e:
        print(e)

    try:
        refs_path = join(new_path, "refs")
        os.mkdir(codes_path)
    except FileExistsError as e:
        print(e)

    # extract all dl
    definitions = [
        Snippet(*definition(dl), new_path)
        for dl in section.xpath(f"//*[@id='{section_id}']/dl")
    ]
    definitions += [
        Snippet(*subdefinition(dl), new_path)
        for dl in section.xpath(f"//*[@id='{section_id}']/dl//dl")
    ]

    refs = [
        Snippet(*a_refs(ahref), refs_path)
        for ahref in section.xpath(f"//*[@class='{section_id}']/p/a[@class='reference']")
    ]
    refs += [
        Snippet(*a_refs(ahref), refs_path)
        for ahref in section.xpath(
            f"//*[@class='{section_id}']/ol//p/a[@class='reference']"
        )
    ]

    # extract all code
    highlight_classes = [
        'highlight',
        'highlight-default',
        'highlight-c',
        'highlight-python',
        'highlight-python3',
    ]

    pre_sections = []

    for highlight in highlight_classes:
        pre_sections += [
            f"//*[@id='{section_id}']/div[@class='{highlight}']/pre",
            f"//*[@id='{section_id}']/div/div[@class='{highlight}']/pre",
            f"//*[@id='{section_id}']/dl//div[@class='{highlight}']/pre",
        ]

    pres = []
    for pre_section_xpath in pre_sections:
        pres += [
            Snippet(*code(pre), gists_path) for pre in section.xpath(pre_section_xpath)
        ]

    code_sections = [
        f"//*[@id='{section_id}']/table//p/code",
    ]
    for code_sections_xpath in code_sections:
        codes = [
            Snippet(*code(_codes), codes_path)
            for _codes in section.xpath(code_sections_xpath)
        ]

    [snippet.save() for snippet in definitions]
    [snippet.save() for snippet in pres]
    [snippet.save() for snippet in codes]
    [snippet.save() for snippet in refs]

    return section_id, new_path


def walk(section, path):
    global tasks

    section_id, new_path = work_on_section(section, path)

    for section_tree in section.xpath(subsection_of(section_id)):

        tasks.put((section_tree, new_path))


def worker():
    global tasks

    while True:
        section_tree, path = tasks.get()
        log.debug(f'Working on path: {path}')

        walk(section_tree, path)
        log.debug(f'Finished {path}')
        tasks.task_done()


def subsection_of(section):
    return f"//*[@id='{section}']/*[@class='section']"


def parse(filename):
    PATH = filename.replace(".html", '')

    os.mkdir(PATH)

    content_tree = load_tree(filename)

    for top_section_tree in content_tree.xpath("//*[@class='body']/*[@class='section']"):

        top_section = top_section_tree.get('id')  # id value is a good dict key

        work_on_section(top_section_tree, PATH)

        for section_tree in top_section_tree.xpath(subsection_of(top_section)):

            tasks.put((section_tree, PATH))

    # turn-on the worker thread
    threading.Thread(target=worker, daemon=True).start()

    # block until all tasks are done
    tasks.join()

    print("stuff done")


if __name__ == "__main__":

    for filename in sys.stdin.readlines():
        parse(filename.strip())
