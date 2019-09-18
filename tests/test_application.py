#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `copypaster` package."""

import pytest

from copypaster.copypaster import main_function

def test_applications():
    assert main_function() == 1
    assert True

