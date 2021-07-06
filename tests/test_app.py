#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from click.testing import CliRunner

def test_app_start():
    import os

    from app import cli

    from app.signal_bus import subscribe, emit, event

    # we subscribe to the signal bus and trigger the quit.
    @subscribe
    def activate_app():
        
        emit(event.quit)


    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ["--debug"])

    assert result.exit_code == 0

    assert "DEBUG" not in result.output
    assert "WARNING" not in result.output
    assert "CRITICAL" not in result.output

    elements = ["Started Kr15 Gtk App",
    "Initializing services...",
    "Initializing config...",
    "load without config",
    "State object initialized",
    "Loading Widgets usig GtkBuilder...",
    "Builder: Resolving object for type GtkApplicationWindow",
    "Builder: Resolving object for type GtkBox",
    "Builder: Resolving object for type GtkMenuBar",
    "Builder: Resolving object for type GtkMenuItem",
    "Builder: Resolving object for type GtkMenu",
    "Builder: Resolving object for type GtkImageMenuItem",
    "Builder: Resolving object for type GtkImageMenuItem",
    "Builder: Resolving object for type GtkImageMenuItem",
    "Builder: Resolving object for type GtkImageMenuItem",
    "Builder: Resolving object for type GtkSeparatorMenuItem",
    "Builder: Resolving object for type GtkImageMenuItem",
    "Builder: Resolving object for type GtkMenuItem",
    "Builder: Resolving object for type GtkMenu",
    "Builder: Resolving object for type GtkImageMenuItem",
    "Builder: Resolving object for type GtkImageMenuItem",
    "Builder: Resolving object for type GtkImageMenuItem",
    "Builder: Resolving object for type GtkImageMenuItem",
    "Builder: Resolving object for type GtkMenuItem",
    "Builder: Resolving object for type GtkMenuItem",
    "Builder: Resolving object for type GtkMenu",
    "Builder: Resolving object for type GtkImageMenuItem",
    "Builder: Resolving object for type GtkMenuItem",
    "Builder: Resolving object for type GtkMenu",
    "Builder: Resolving object for type GtkImageMenuItem",
    "Builder: Resolving object for type GtkLabel",
    "Routing event: about_button",
    "Routing event: reset_styles",
    "Routing event: quit",
    "Importing stories...",
    "Subscribed error_show_dialog for event error_show_dialog",
    "Subscribed about_button for event about_button",
    "Subscribed activate_app for event activate_app",
    "Subscribed start_app for event start_app",
    "Subscribed quit for event quit",
    "Subscribed load_styles for event load_styles",
    "Subscribed reset_styles for event reset_styles",
    "Starting the Application...",
    "Startup...",
    "Emited start_app",
    "Switching to state NORMAL",
    "Emited load_styles",
    "Loading styles",
    "Loading css files",
    "Activation...",
    "Emited activate_app",
    "State is NORMAL",
    "All green. Welcome to application.",
    "Returning exit status value..."]

    for element in elements:
        assert element in result.output
