from app.register import Register as __
from copypaster import log
from app.signal_bus import subscribe
from copypaster.file_loader import Folder, GoTo
from copypaster.widgets.dialogs import DialogAdd, DialogEdit, DialogAddFolder
from copypaster.widgets.containers import ButtonGrid

@subscribe
def edit_button(button_to_edit):
    dialog = DialogEdit(__.Application.win, button_to_edit)
    dialog.run()
    dialog.destroy()

@subscribe
def preview_content(message):
    __.PreviewLabel.set_text(message)

@subscribe
def remove_button(button):
    __.Snippets.remove_button_from_current_grid(button)

@subscribe
def add_button(copy_button):
    log.debug(f"Adding copy {copy_button} button to current button grid")
    
    copy_button.set_path(__.Snippets.level)
    copy_button.save()

    __.Snippets.add_to_current_grid(copy_button)
    
    copy_button.show()
    log.debug("A button has been added")

    __.Jimmy.clean_clipboard()

@subscribe
def add_folder(folder_name):
    log.debug(f"Adding folder")
    folder = Folder(folder_name)
    folder.set_path(__.Snippets.level)
    folder.save()

    goto = GoTo(
        name=folder.name, 
        position=__.Snippets.level,
        destination=folder.path)
    __.Snippets.add_to_current_grid(goto)


    grid = ButtonGrid()
    up_to_parent = GoTo(
                name="..",
                position=folder.path,
                destination=__.Snippets.level
    )
    up_to_parent.show()
    
    grid.append(up_to_parent)
    grid.show()

    __.Snippets.tree[folder.path] = grid
    __.Snippets.add_named(grid, folder.path)

    goto.show()

@subscribe
def open_add_button_dialog():
    dialog = DialogAdd(__.main_window)
    dialog.run()
    dialog.destroy()


@subscribe
def open_add_folder_dialog():
    dialog = DialogAddFolder(__.main_window)
    dialog.run()
    dialog.destroy()