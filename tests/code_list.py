import gi


import astor
 
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

GLADE_FILE = "list_manipulation_buttons.glade"

CODE_FILE = "code_list.py"

ast_code = astor.code_to_ast.parse_file(CODE_FILE)

print(ast_code)


_R = {}

LISTBOX='listbox'

CLIPBOARD = []


class ListHandlers:
    def switch_selection_mode(self, button):
        
        list_box = _R[LISTBOX]

        if button.get_active():
            list_box.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        else:
            list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        
    def deselect_all(self, button):

        _R[LISTBOX].unselect_all()

        print(button.get_label())

    def copy(self, button):
        print(button.get_label())
        global CLIPBOARD
        
        row = _R[LISTBOX].get_selected_row()
        CLIPBOARD = [row.data]

    def copy_selected(self, button):
        print(button.get_label())
        global CLIPBOARD
        
        rows = _R[LISTBOX].get_selected_rows()

        CLIPBOARD = [row.data for row in rows]
        
        [print(row.get_index()) for row in rows]

    def add_row_before(self, button):
        print(button.get_label())

    def paste_before(self, button):
        print(button.get_label())

        if not CLIPBOARD:
            return

        global _R
        lista = _R[LISTBOX]

        current_row = lista.get_selected_row()

        must_prepend = not current_row and current_row.get_index() == 0

        new_row = ListBoxRowWithData(CLIPBOARD[0])

        if must_prepend:
            lista.prepend(new_row)
        else:
            current_row_index = current_row.get_index()

            before = current_row_index - 1
            print(before)
            lista.insert(new_row, before)

        lista.show_all()

    def add_row_after(self, button):
        print(button.get_label())

    def paste_after(self, button):
        print(button.get_label())
        global _R
        if not CLIPBOARD:
            return

        lista = _R[LISTBOX]

        current_row = lista.get_selected_row()
        
        new_row = ListBoxRowWithData(CLIPBOARD[0])

        must_append = not current_row

        if must_append:
            lista.add(new_row)
        else:
            current_row_index = current_row.get_index()

            after = current_row_index + 1
            print(after)
            lista.insert(new_row, after)

        lista.show_all()
    
    def delete_selected(self, button): 
        print(button.get_label())

        lista = _R[LISTBOX]

        for row in lista.get_selected_rows():
            lista.remove(row)

        lista.show_all()

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(label=data))


class ListBoxWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="ListBox Demo")
        self.set_border_width(10)

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box_outer)

        builder = Gtk.Builder()
        builder.add_from_file(GLADE_FILE)
        builder.connect_signals(ListHandlers())

        listbox = builder.get_object("buttons_grid")
        box_outer.pack_start(listbox, True, True, 0)

        listbox_2 = Gtk.ListBox()
        _R[LISTBOX] = listbox_2

        # `listbox_2.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        items = "This is a sorted ListBox Fail".split()

        for item in items:
            listbox_2.add(ListBoxRowWithData(item))

        def sort_func(row_1, row_2, data, notify_destroy):
            return row_1.data.lower() > row_2.data.lower()

        def filter_func(row, data, notify_destroy):
            return False if row.data == "Fail" else True

        listbox_2.set_sort_func(sort_func, None, False)
        listbox_2.set_filter_func(filter_func, None, False)

        def on_row_activated(listbox_widget, row):
            print(row.data)


        listbox_2.connect("row-activated", on_row_activated)

        box_outer.pack_start(listbox_2, True, True, 0)
        listbox_2.show_all()


win = ListBoxWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

