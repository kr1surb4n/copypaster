from folders.register import Register as __
from folders import log
from folders.signal_bus import signal_bus
from folders.widgets.dialogs import DialogAdd, DialogEdit

class ButtonStories:


    def __init__(self,):
        [signal_bus.subscribe(event, self)
         for event in
         [
             'add_button',
             'edit_button',
             'remove_button',
             'open_add_button_dialog'
         ]]

    def edit_button(self, button_to_edit):
        dialog = DialogEdit(
            __.Application.win, button_to_edit)
        dialog.run()
        dialog.destroy()


    def remove_button(self, button):
        parent = button.get_parent()
        del parent.get_parent().button_deck.buttons[button.value]
        parent.remove(button)


    def add_button(self, name, value):
        log.debug("Adding button to currently selected deck")
        assert name
        assert value

        try:
            cabinet = __.FileCabinet
            page = cabinet.current_page
            b = page.button_deck.add_button(name=name,
                                                    value=value)
            page.add(b)
            b.show()
            log.debug("A button has been added")

            __.Jimmy.send('')
        except IndexError:
            pass  # yes, cause this value exists


    def open_add_button_dialog(self):
        dialog = DialogAdd(
            __.Application.win)
        dialog.run()
        dialog.destroy()


button_stories = ButtonStories()
