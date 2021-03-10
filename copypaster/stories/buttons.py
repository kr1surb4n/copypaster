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
    __.Snippets.remove_button_from_current_grid(button)

@subscribe
def add_button(copy_button):
    log.debug(f"Adding copy {copy_button} button to current button grid")
    
    __.Snippets.add_to_current_grid(copy_button)
    
    copy_button.show()
    log.debug("A button has been added")

    __.Jimmy.clean_clipboard()


@subscribe
def open_add_button_dialog():
    dialog = DialogAdd(__.Application.win)
    dialog.run()
    dialog.destroy()
