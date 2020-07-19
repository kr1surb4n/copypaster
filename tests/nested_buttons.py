from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import Gtk, GdkPixbuf
import gi
from os.path import basename, dirname, abspath, join as path_join
gi.require_version("Gtk", "3.0")


THIS_FOLDER = dirname(abspath(__file__))

buttons = list(range(10))

class _Button(Gtk.Button):

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', None)
        kwargs['label'] = self.name
        self.id = self.hash()

        super(_Button, self).__init__(*args, **kwargs)

        self.set_tooltip_text(self.name)
        self.connect('clicked', self.on_button_click)

    def on_button_click(self, button):
        print(self.name)


class ParentLink(_Button):
    def __init__(self, parent, container):
        self.parent = parent
        self.container = container

        super(ParentLink, self).__init__(name="Back One")

    def on_bu



class ButtonGrid(Gtk.FlowBox):
    "Main area of user interface content."

    def __init__(self, deck_file):
        Gtk.FlowBox.__init__(self)

        self.set_valign(Gtk.Align.START)
        # self.set_max_children_per_line(4)
        self.set_selection_mode(Gtk.SelectionMode.NONE)

        for button in self.button_deck.get_buttons():
            self.add(button)



class NestedButtons:
    current_display = None

    """Zagnierzdżone guziki

    mam bloki guzików:

    blocks = {root: [], 'blok1': [], 'blok2': [], 'blok3': []}

    każdy z bloków ma guzik powrót, dodaj nowy  i po guziku do każdego z bloku (1 ma 2 i 3, 2 ma 1 i 3 itd.)
    każdy z bloków to po prostu Grid

    kiedyt się wszystko ładuje za pierwszym razem, to
    pierwszy grid jest widoczny. reszta jest niewidoczna.

    klik na guzik powrót: wychodzisz wyżej
    klik na guzik 1, 2, 3 : przechodzisz do bloku


    """




class IconViewWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(200, 200)

        liststore = Gtk.ListStore(Pixbuf, str, str)
        iconview = Gtk.IconView.new()
        iconview.set_model(liststore)
        iconview.set_item_width(10)
        iconview.set_pixbuf_column(0)
        iconview.set_text_column(1)
        iconview.set_tooltip_column(2)

        # for icon in icons:

        for _ in range(200):
            _, icon = next(shooter)
            pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 16, 0)
            # pixbuf = GdkPixbuf.Pixbuf.new_from_file(
            #     "icons/{}.png".format(icon))
            liststore.append([pixbuf, icon, icon])

        self.add(iconview)


win = IconViewWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
