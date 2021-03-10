# -*- coding: utf-8 -*-
from copypaster import log
from app.register import Register as __

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
        from copypaster.widgets.containers import ButtonTree  # noqa

        if type_name == 'MainWindow':
            pass
            # return MainWindow  - in normal use, Type should be returned

        if type_name == 'ButtonTree':
            return ButtonTree

        r = Gtk.Builder.do_get_type_from_name(self, type_name)
        log.debug('GtkBuilder: => {}\t{}'.format(type_name, r))
        return r


log.info("Starting builder")
builder = GtkBuilder()
__.Builder = builder
