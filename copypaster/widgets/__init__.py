from app.register import Register as __, register_instance
from copypaster import log, CURRENT_DIR, State, AppState
import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio  # noqa
