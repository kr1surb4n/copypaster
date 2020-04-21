from gi.repository import Gtk, Gdk
import gi

gi.require_version("Gtk", "3.0")


class LabelWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Label Example")
        self.set_default_size(500, 500)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_homogeneous(False)

        label = Gtk.Label("This is a normal label")
        self.label = label
        vbox.pack_start(label, True, True, 0)

        self.add(vbox)
        self.connect("key-press-event", self.on_key_press_event)

    def on_key_press_event(self, widget, event):

        print("Key press on widget: ", widget)
        print("          Modifiers: ", event.state)
        print("      Key val, name: ", event.keyval,
              Gdk.keyval_name(event.keyval))

        self.label.set_text(Gdk.keyval_name(event.keyval))

        # check the event modifiers (can also use SHIFTMASK, etc)
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)

        # see if we recognise a keypress
        if ctrl and event.keyval == Gdk.KEY_h:
            self.shortcut_hits += 1
            self.update_label_text()


style_provider = Gtk.CssProvider()
style_provider.load_from_path("app.css")
Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

window = LabelWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
