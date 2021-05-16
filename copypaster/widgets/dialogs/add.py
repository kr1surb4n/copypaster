from app.widgets.utility import wrap
from copypaster import log
from app.register import Register as __
from app.signal_bus import emit
from copypaster.file_loader import Copy, Snippet, Folder

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio  # noqa


class DialogAdd(Gtk.Dialog):
    def __init__(self, parent):
        log.debug("Adding a new button...")
        Gtk.Dialog.__init__(self)
        self.parent = parent

        self.set_modal(True)
        self.add_button(button_text="OK", response_id=Gtk.ResponseType.OK)
        self.add_button(button_text="CANCEL", response_id=Gtk.ResponseType.CANCEL)
        self.set_transient_for(parent)
        self.set_default_size(450, 350)

        box = self.get_content_area()
        grid = Gtk.Grid(
            orientation=Gtk.Orientation.VERTICAL,
            hexpand=True,
            column_spacing=10,
            row_spacing=10,
        )
        clipboard_contents = __.Jimmy.receive()

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Put name here or value will be used")
        self.entry.set_text(clipboard_contents)
        # self.entry.connect("key_press_event", self.on_key_press_event)

        self.textview = Gtk.TextView()
        self.textview.set_cursor_visible(True)
        self.textview.set_hexpand(True)
        self.textview.set_vexpand(True)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)

        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(clipboard_contents)

        self.wrapped_textview = wrap(self.textview)

        self.save_button = Gtk.Button(label="Save")
        self.save_button.connect("clicked", self.on_save)

        grid.add(self.entry)
        grid.add(self.wrapped_textview)
        grid.add(self.save_button)

        box.add(grid)

        self.show()

    def on_key_press_event(self, button):  # TODO check if that works
        self.save(button)

    def on_save(self, button):
        name = self.entry.get_text().strip()

        value = self.textbuffer.get_text(
            self.textbuffer.get_start_iter(), self.textbuffer.get_end_iter(), False
        ).strip()

        if not value:
            log.error("No value to save - aborting")
            emit("error_show_dialog", "Soo, the value is missing, it's required.")
            return False

        if not name:
            name = value

        log.debug("Adding new button to a file cabinet...")
        emit("add_button", Copy(Snippet(name, value)))

        self.destroy()


class DialogAddFolder(Gtk.Dialog):
    def __init__(self, parent):
        log.debug("Adding a new button...")
        Gtk.Dialog.__init__(self)
        self.parent = parent

        self.set_modal(True)
        self.add_button(button_text="OK", response_id=Gtk.ResponseType.OK)
        self.add_button(button_text="CANCEL", response_id=Gtk.ResponseType.CANCEL)
        self.set_transient_for(parent)
        self.set_default_size(450, 350)

        box = self.get_content_area()
        grid = Gtk.Grid(
            orientation=Gtk.Orientation.VERTICAL,
            hexpand=True,
            column_spacing=10,
            row_spacing=10,
        )

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Folder name")
        self.entry.set_text("")

        self.save_button = Gtk.Button(label="Save")
        self.save_button.connect("clicked", self.on_save)

        grid.add(self.entry)
        grid.add(self.save_button)

        box.add(grid)

        self.show_all()

    def on_key_press_event(self, button):  # TODO check if that works
        self.save(button)

    def on_save(self, button):
        name = self.entry.get_text().strip()

        if not name:
            log.error("No folder name to save - aborting")
            emit("error_show_dialog", "Soo, the value is missing, it's required.")
            return False


        log.debug("Adding new folder to snippets...")
        emit("add_folder", name)
        self.destroy()