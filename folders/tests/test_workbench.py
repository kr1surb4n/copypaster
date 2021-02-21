import pytest
import unittest
from unittest import mock
from unittest.mock import patch
from gaphas.item import Item
from gaphas.geometry import Rectangle

from folders.widgets.workbench import (
    build_elements,
    object_register,
    Container,
    Box,
)


def test_build_elements():

    assert isinstance(build_elements(Box, Rectangle(1, 1, 60, 60)), Item)


def test_object_register():
    container_one = Container(
        key="one", value="puma", box=Rectangle(0, 0, 20, 20), element=Box
    )
    container_two = Container(
        key="two", value="bunny", box=Rectangle(0, 5, 10, 10), element=Box
    )
    container_three = Container(
        key="three", value="bear", box=Rectangle(5, 5, 10, 2), element=Box
    )
    container_far = Container(
        key="far", value="bat", box=Rectangle(100, 100, 20, 20), element=Box
    )

    viewport = Rectangle(-5, -5, 40, 40)

    index = object_register()

    index.register(container_one)
    index.register(container_two)
    index.register(container_three)
    index.register(container_far)

    assert index[id(container_one)] == container_one
    assert index[id(container_two)] == container_two
    assert index[id(container_three)] == container_three
    assert index[id(container_far)] == container_far

    assert index[id(container_one)] != container_two
    assert index[id(container_one)] != container_three
    assert index[id(container_one)] != container_far

    visible_object = index.get_visible_objects(viewport)

    assert container_one in visible_object
    assert container_two in visible_object
    assert container_three in visible_object

    assert container_far not in visible_object
