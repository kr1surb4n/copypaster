from app.register import Register as __
from copypaster import log
from app.signal_bus import subscribe, emit
from copypaster.file_loader import Folder, GoTo
from copypaster.file_loader import Copy, Snippet, Folder
from copypaster.widgets.containers import ButtonGrid

"""
ErrorDialog:
error_dialog 
    error_message
    error_ok
        signal:
            click: error_ok_pressed

folder_dialog:
    folder_name
            enter_save_folder
    folder_submit
        signal:
            click: save_folder
            emit   save_folder

snippet_dialog
        snippet_title
            enter_save_snippet
        snippet_content
            enter_save_snippet    
        snippet_submifft:
            click:  save_snippet
            emit    save_snippet
"""


@subscribe
def preview_content(message):
    __.PreviewLabel.set_text(message)


@subscribe
def remove_button(button):
    __.Snippets.remove_button_from_current_grid(button)


@subscribe
def remove_folder(button):
    __.Snippets.remove_grid(button)


@subscribe
def edit_snippet_button(button_to_edit):
    dialog = __.snippet_dialog
    
    snippet_title = __.Builder.get_object('snippet_title')
    snippet_content = __.Builder.get_object('snippet_content').get_buffer()
    
    snippet_title.set_text(button_to_edit.name)
    snippet_content.set_text(button_to_edit.content)
    
    dialog.run()
    dialog.hide()


@subscribe
def save_snippet(*args, **kwargs):
    """
    a form is submited in snippet_dialog

    You have to:
    - get from Builder:
        - snippet_title
        - snippet_content
    - get title from snippet_title, strip
    - get content from snippet_content
    - clean snippet_title
    - clean snippet_content
    - if no content, stop
    - if no title, set content as title
    - emit add_button, send Copy button made from title and content

    """
    snippet_title = __.Builder.get_object('snippet_title')
    snippet_content = __.Builder.get_object('snippet_content').get_buffer()

    title = snippet_title.get_text().strip()
    content = snippet_content.get_text(
        snippet_content.get_start_iter(), snippet_content.get_end_iter(), False
    ).strip()

    snippet_title.set_text("")
    snippet_content.set_text("")

    if not content:
        log.error("No content to save - aborting")
        emit("error_show_dialog", "Soo, the content is missing, it's required.")
        return False

    if not title:
        title = content

    log.debug("Adding new button to grid ...")
    emit("add_button", title, content)
    __.snippet_dialog.hide()


@subscribe
def add_button(title, content):
    log.debug(f"Adding copy {title}, {content} button to current button grid")
    copy_button = Copy(Snippet(title, content))
    __.Snippets.add_to_current_grid(copy_button)

    copy_button.show()

    log.debug("A button has been added")

    __.Jimmy.clean_clipboard()


@subscribe
def save_folder(*args, **kwargs):
    """
    a form is submited in folder_dialog

    You have to:
    - get from Builder:
        - folder_name
    - get name from folder_name, strip
    - clean name
    - if no name, stop
    - emit add_folder, send name

    """
    folder_name = __.Builder.get_object('folder_name')

    name = folder_name.get_text().strip()

    folder_name.set_text("")

    if not name:
        log.error("No name to use - aborting folder creation")
        emit("error_show_dialog", "Soo, the name is missing, it's required.")
        return False

    log.debug("Adding new GoTo button to grid ...")
    emit("add_folder", name)
    __.folder_dialog.hide()


@subscribe
def add_folder(folder_name):
    log.debug(f"Adding folder")
    folder = Folder(folder_name)
    folder.suffix_path(__.Snippets.current_level)
    folder.save()

    grid = ButtonGrid(path=folder.path)

    folder_button = GoTo(folder_name, __.Snippets.current_level, folder.path)

    __.Snippets.tree[folder.path] = grid
    __.Snippets.add_named(grid, folder.path)

    __.Snippets.current_grid.append(folder_button)
    folder_button.show()


@subscribe
def open_add_button_dialog(*args):
    snippet_title = __.Builder.get_object('snippet_title')
    snippet_content = __.Builder.get_object('snippet_content').get_buffer()

    clipboard_content = __.Jimmy.receive()

    snippet_content.set_text(clipboard_content)

    __.snippet_dialog = __.Builder.get_object('snippet_dialog')
    __.snippet_dialog.run()
    __.snippet_dialog.hide()


@subscribe
def open_add_folder_dialog(*args):
    """
    Set folder name entry with clipboard contents,
    Start dialog,
    when done hide it.
    """
    folder_name = __.Builder.get_object('folder_name')

    clipboard_content = __.Jimmy.receive()

    folder_name.set_text(clipboard_content)

    __.folder_dialog = __.Builder.get_object('folder_dialog')
    __.folder_dialog.run()
    __.folder_dialog.hide()


@subscribe
def error_show_dialog(message):
    __.error_message = __.Builder.get_object('error_dialog')
    label = __.Builder.get_object('error_message')
    label.set_text(message)
    __.error_message.run()
    __.error_message.hide()


@subscribe
def close_error_dialog(*args):
    __.error_message.hide()
