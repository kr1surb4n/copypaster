from copypaster.register import Register as __
from copypaster import logger
from copypaster.signal_bus import signal_bus
from copypaster.widgets.dialogs import DialogAdd, DialogEdit


class ButtonStories:

    def on_edit_button(self, button_to_edit):
        dialog = DialogEdit(
            __['Application'].win, button_to_edit)
        dialog.run()
        dialog.destroy()

    def on_remove_button(self, button):
        parent = button.get_parent()
        del parent.get_parent().button_deck.buttons[button.value]
        parent.remove(button)

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

            __['Jimmy'].send('')
        except IndexError:
            pass  # yes, cause this value exists

    def on_open_add_button_dialog(self):
        dialog = DialogAdd(
            __['Application'].win)
        dialog.run()
        dialog.destroy()

button_stories = ButtonStories()

signal_bus.subscribe('add_button', button_stories)
signal_bus.subscribe('edit_button', button_stories)
signal_bus.subscribe('remove_button', button_stories)
signal_bus.subscribe('open_add_button_dialog', button_stories)
