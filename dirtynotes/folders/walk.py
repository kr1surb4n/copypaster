"""The Walking Thread"""
import os
import threading, queue

kolejka_folder = queue.Queue()

CODE_PATH = "/home/kris/workshops/tools/copypaster"
DECKS = "decks"

Decks = {}
Decks_Data = {}

join = os.path.join


def read(entry):

    if entry.is_file():
        return ('file', f"name: {entry.name}", f"path: {entry.path}")

    if entry.is_dir():
        return ('dir', f"name: {entry.name}", f"path: {entry.path}")


def walk(folder):
    global Decks
    deck = []
    # folders = []

    # TODO: here i can read a file with metadata

    with os.scandir(folder) as it:
        for entry in it:
            if entry.name.startswith('.'):
                continue

            if entry.is_dir():
                kolejka_folder.put(entry.path)

            deck.append(read(entry))

    Decks[folder] = deck
    Decks_Data[folder] = {'name': os.path.basename(folder)}


def worker():
    while True:
        folder = kolejka_folder.get()
        print(f'Working on folder: {folder}')

        walk(folder)
        print(f'Finished {folder}')
        kolejka_folder.task_done()


# turn-on the worker thread
threading.Thread(target=worker, daemon=True).start()

kolejka_folder.put(CODE_PATH)

# block until all tasks are done
kolejka_folder.join()
print('All work completed')


print()
print("Files")
for path, deck in Decks.items():
    print(deck)
