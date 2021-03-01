from deyaml import (
    rules,
    YamlFile,
    CONTENT,
    INFO,
    NAME,
    VALUE,
    CODE_PATH,
    CLICK_COUNT,
    BUTTONS,
    CATEGORY,
    MAX_FILENAME_LENGTH,
    SNIPPET,
    Snippet,
)
import pytest
import logging as log
import configparser

TEST_FIXTURE = "fixture.yml"

FIRST = "First"
TWO = "Two"
THREE = "Three"
EXCEPTION = "Exceptions"
PITU = "pitu"
TEST = "test"
FIXTURE = "fixture"


def test_helpers():
    successes = [
        # '',
        # ' ',
        "_",
        "[",
        "#",
        "@",
        "!",
        ",",
        ".",
        "-",
    ]

    fails = ["a", "1", "Z", "A"]

    for fixture in successes:
        assert "" == fixture.translate(rules)

    for fixture in fails:
        assert "" != fixture.translate(rules)


def test_yaml_file():

    yaml_file = YamlFile(TEST_FIXTURE)

    assert yaml_file
    assert yaml_file.contents
    assert INFO in yaml_file.contents
    assert BUTTONS in yaml_file.contents
    assert NAME in yaml_file.contents[INFO][0]
    assert CATEGORY in yaml_file.contents[INFO][1]

    assert TEST == yaml_file.contents[INFO][0][NAME]
    assert FIXTURE in yaml_file.contents[INFO][1][CATEGORY]

    buttons = yaml_file.contents[BUTTONS]
    assert 6 == len(buttons)
    assert all(isinstance(button, dict) for button in buttons)

    one, two, three, four, five, six = buttons

    assert FIRST == one.get(VALUE)
    assert False == two.get(VALUE, False)
    assert THREE == three.get(NAME)
    assert PITU == five.get(VALUE)
    assert False == five.get(NAME, False)


def test_snippet():
    snippet = Snippet()
    assert snippet

    with pytest.raises(AttributeError):
        x = snippet.dupa

    snippet.test = None

    snippet.content = TEST
    assert snippet.content
    assert snippet.content == TEST

    snippet.name = FIXTURE
    assert snippet.file_name == FIXTURE


def test_snippets():

    yaml_file = YamlFile(TEST_FIXTURE)

    assert yaml_file

    snippets = list(yaml_file.transform_into_snippets())
    assert snippets

    assert len(snippets) == 6

    one, two, three, four, five, six = snippets

    assert one.content == FIRST
    assert two.content == ""
    assert three.content == ""

    assert four.file_name.startswith("snippet")

    assert five.content == PITU
    assert five.name == PITU

    assert len(six.file_name) == MAX_FILENAME_LENGTH
    assert six.file_name == "ogor-ryba--liscie-"


def test_reverse():
    snippet_path = CODE_PATH + "/python/try-exec-else-fina"

    snippet = Snippet()
    snippet.load(snippet_path)

    assert snippet.content
    assert snippet.name == "try exec else fina"
    assert snippet.file_name == "try-exec-else-fina"
