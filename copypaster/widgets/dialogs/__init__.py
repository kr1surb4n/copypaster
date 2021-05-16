from .add import DialogAdd, DialogAddFolder
from .edit import DialogEdit
from .error import DialogError



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

__all__ = [
    "DialogAdd",
    "DialogAddFolder",
    "DialogEdit",
    "DialogError",
]
