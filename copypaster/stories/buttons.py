from app.register import Register as __
from copypaster import log
from app.signal_bus import subscribe
from copypaster.widgets.dialogs import DialogAdd, DialogEdit


@subscribe
def edit_button(button_to_edit):
    dialog = DialogEdit(__.Application.win, button_to_edit)
    dialog.run()
    dialog.destroy()


@subscribe
def remove_button(button):
    parent = button.get_parent()
    del parent.get_parent().button_deck.buttons[button.value]
    parent.remove(button)


@subscribe
def add_button(name, value):
    log.debug("Adding button to currently selected deck")
    assert name
    assert value

    try:
        cabinet = __.FileCabinet
        current_grid = cabinet.pages[cabinet.get_current_page()]
        b = current_grid.button_deck.add_button(name=name, value=value)
        current_grid.add(b)
        b.show()
        log.debug("A button has been added")

        __.Jimmy.send("")
    except IndexError:
        pass  # yes, cause this value exists


@subscribe
def open_add_button_dialog():
    dialog = DialogAdd(__.Application.win)
    dialog.run()
    dialog.destroy()
