#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `copypaster` package."""
from copypaster.copypaster import main_function


def test_applications():
    import os

    default_config_path = os.path.join("example.conf")

    assert main_function(default_config_path) == 1
    assert True
