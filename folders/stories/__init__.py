"""Here we load all the stories.

We do that by importing whole file.
The order is probably important.
"""
# from .errors import *  # noqa
# from .load_button_decks import *  # noqa
# from .notebook_stories import *  # noqa
# from .buttons import *  # noqa
# from .of_jimmy_mcgill import *  # noqa
from folders import log
from app.register import Register as __
from app.signal_bus import subscribe, emit, signals
from folders.widgets.workbench import Workbench

@subscribe
def set_location(location):
    __.workbench_location.set_text(location.value)

@subscribe
def start_app():
    print("Starting folders")
    __.main_box.show_all()

    emit('set_location', __.workbench.location)