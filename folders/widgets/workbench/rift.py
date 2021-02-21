"""
Rift is the object, that takes
some entity and display's its internals
on a plain.

i takes some (in our case) path to folder,
and displays the contents of that folder.

"""
import os

INITIAL_FOLDER = "/home/kris/workshops/tools/copypaster"


def get_files_in_folder(path):
    return os.scandir(path)


def obtain_values():
    return list(get_files_in_folder(INITIAL_FOLDER))
