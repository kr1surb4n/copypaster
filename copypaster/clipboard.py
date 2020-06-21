import xerox
from copypaster.register import Register, register_instance
from copypaster import logger


@register_instance
class Jimmy:
    """in tribute to Jimmy McGill, a copist"""

    def send(self, text):
        logger.debug("Coping: {}".format(text))
        # copy(text)
        xerox.copy(text)

    def clean_clipboard(self):
        logger.debug("cleaning clipboard")
        self.send("")

    def recieve(self):
        contents = xerox.paste()
        logger.debug("Pasting: {}".format(contents))
        return contents


jimmy = Jimmy()
