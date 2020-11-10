import xerox
from copypaster.register import Register, register_instance
from copypaster import log

# This is an abstraction for the actions
# done to clipboard.
#
# It's called Jimmy so that it's easier
# to talk about it.
# i.e.
# Jimmy failed to copy stuff.
# Jimmy cannot .
#


@register_instance
class Jimmy:
    """in tribute to Jimmy McGill, a copist"""

    def send(self, text):
        log.debug("Coping: {}".format(text))
        xerox.copy(text)

    def clean_clipboard(self):
        log.debug("Cleaning clipboard")
        self.send("")

    def receive(self):
        contents = xerox.paste()
        log.debug("Pasting: {}".format(contents))
        return contents if contents.strip() else ""


_Jimmy = Jimmy()


def test_jimmy():

    # can I send and receive?
    test_message = "One, Two, Three"
    _Jimmy.send(test_message)
    assert _Jimmy.receive() == test_message

    # can I clean clipboard?
    _Jimmy.send(test_message)
    _Jimmy.clean_clipboard()
    assert _Jimmy.receive() != test_message
