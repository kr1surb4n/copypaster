#!/usr/bin/env python3
from folders.register import Register as __
from folders import log
from folders.signal_bus import signal_bus


class MouseState:
    pass


class KeyboardState:
    pass


on_key_press():
   mouse_state[key_val] = True

on_key_release():
   mouse_state[key_val] = False

on_button_press():
   mouse_state[button] = True

on_button_release():
   mouse_state[button] = False
