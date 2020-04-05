from copypaste import copy
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


jimmy = Jimmy()
