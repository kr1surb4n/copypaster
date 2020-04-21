from copypaster.widgets.utility import wrap

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio  # noqa


class DialogError(Gtk.Dialog):

    def __init__(self, parent, massage):  # lol
        Gtk.Dialog.__init__(self)
        self.set_modal(True)
        self.add_button(button_text="OK", response_id=Gtk.ResponseType.OK)
        self.set_transient_for(parent)
        self.set_default_size(150, 100)

        label = Gtk.Label(massage)

        box = self.get_content_area()
        box.add(label)
        self.show_all()


class DialogEdit(Gtk.Dialog):

    def __init__(self, parent, button_to_edit):  # lol
        Gtk.Dialog.__init__(self)

        self.edited = button_to_edit

        self.set_modal(True)
        self.add_button(button_text="OK", response_id=Gtk.ResponseType.OK)
        self.add_button(button_text="CANCEL",
                        response_id=Gtk.ResponseType.CANCEL)
        self.set_transient_for(parent)
        self.set_default_size(450, 350)

        box = self.get_content_area()
        grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL,
                        hexpand=True, column_spacing=10, row_spacing=10)

        self.entry = Gtk.Entry()
        self.entry.set_text(self.edited.name)
        self.entry.connect("key_press_event", self.on_key_press_event)

        self.textview = Gtk.TextView()
        self.textview.set_cursor_visible(True)
        self.textview.set_hexpand(True)
        self.textview.set_vexpand(True)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)

        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(self.edited.value)

        self.wrapped_textview = wrap(self.textview)

        self.save_button = Gtk.Button(label="Save")
        self.save_button.connect('clicked', self.on_save)

        grid.add(self.entry)
        grid.add(self.wrapped_textview)
        grid.add(self.save_button)

        box.add(grid)

        self.show_all()

    def on_key_press_event(self, button):
        self.save(button)

    def on_save(self, button):
        text_view_content = self.textbuffer.get_text(self.textbuffer.get_start_iter(
        ), self.textbuffer.get_end_iter(), False)

        self.edited.name, self.edited.value = self.entry.get_text(), text_view_content
        self.edited.set_label(self.edited.name)
        self.destroy()
