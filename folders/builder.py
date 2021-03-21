# -*- coding: utf-8 -*-
import sys
import os

from folders import log
from folders.widgets.workbench import Workbench
from app.config import Config
from app.register import register_instance, Register as __

""" Initialize services """

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject  # noqa

class GtkBuilder(Gtk.Builder):
    def do_get_type_from_name(self, type_name):
        """
        Looks up a type by name, using the virtual function that Gtk.Builder
        has for that purpose.

        Parameters:  type_name (str) – type name to lookup
        Returns:     the GObject.GType found for type_name
                       or GObject.TYPE_INVALID if no type was found
        Return type: GObject.GType

        """
        
        
        if type_name == 'Workbench':
            return Workbench
            # return MainWindow  - in normal use, Type should be returned

        r = Gtk.Builder.do_get_type_from_name(self, type_name)
        return r


builder = GtkBuilder()
__.builder = builder
