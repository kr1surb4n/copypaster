from app.config import Config
from app.register import Register as __


class CopyConfig(Config):
    
    def get_dirty_deck(self):
        try:
            main = self.cfg["main"]
            return "Dirty", main["dirty_deck"]
        except IndexError as _e:
            print(_e)
            raise _e

    def get_decks(self):
        try:
            filepaths = self.cfg["decks"]
            return {deck_name: filepaths[deck_name] for deck_name in filepaths}
        except IndexError as _e:  # watch out! snakes
            print(_e)
            raise _e

    def get_collections(self):
        try:
            filepaths = self.cfg["collections"]
            return {
                collection_name: filepaths[collection_name]
                for collection_name in filepaths
            }
        except IndexError as _e:  # well, it's python. what did you exepect?
            print(_e)
            raise _e

__.Config = CopyConfig()