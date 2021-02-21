import sys
import pytest
import unittest
from unittest import mock
from unittest.mock import patch
from gaphas.item import Item
from gaphas.geometry import Rectangle

from folders.widgets.workbench.rift import (
    get_files_in_folder,
    INITIAL_FOLDER,
)

def test_get_files_in_folder():
    files = get_files_in_folder(INITIAL_FOLDER)

    with open("debug", 'w') as f:
        f.write(repr(list(files)))

    assert files is not []



