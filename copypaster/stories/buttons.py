from copypaster.register import Register as __, register_instance
from copypaster import logger, State, AppState
from copypaster.signal_bus import signal_bus


class AddButton:
    def on_add_button(self, name, value):
        logger.debug("Adding button to currently selected deck")
        assert name
        assert value

        try:
            cabinet = __['FileCabinet']
            current_deck = cabinet.pages[cabinet.get_current_page()]
            b = current_deck.button_deck.add_button(name=name,
                                                    value=value)
            current_deck.add(b)
            b.show()
            logger.debug("A button has been added")
        except IndexError:
            pass  # yes, cause this value exists

class OpenAddButtonDialog:
    def on_

signal_bus.subscribe('add_button', AddButton())
