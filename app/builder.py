# -*- coding: utf-8 -*-
import sys
import os
import configparser

from copypaster import log
from app.config import Config
from app.register import register_instance, Register as __

""" Initialize services """

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa


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

        if type_name == 'MainWindow':
            pass
            # return MainWindow  - in normal use, Type should be returned

        r = Gtk.Builder.do_get_type_from_name(self, type_name)
        print('GtkBuilder: => {}\t{}'.format(type_name, r))
        return r


builder = GtkBuilder()
__.builder = builder
