#!/usr/bin/env python3

from folders import log
from folders.register import register_instance


import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa

from gaphas import Canvas, GtkView
from gaphas.examples import Box, Text
from gaphas.painter import DefaultPainter
from gaphas.item import Line
from gaphas.util import text_extents


class MyText(Text):
    """
    Text with experimental connection protocol.
    """

    def draw(self, context):
        Text.draw(self, context)
        cr = context.cairo
        w, h = text_extents(cr, self.text, multiline=self.multiline)
        cr.rectangle(-25, -15, w + 50, h + 30)
        cr.stroke()


@register_instance
class Workbench(Gtk.Box):
    "Main area of user interface content."

    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)

        log.info("Loading Workbench")
        canvas = Canvas()
        view = GtkView()
        view.painter = DefaultPainter()
        view.canvas = canvas
        self.pack_start(view, True, True, 0)

        # Draw first gaphas box
        b1 = Box(60, 60)
        b1.matrix = (1.0, 0.0, 0.0, 1, 10, 10)
        canvas.add(b1)

        tx = Text(text="joo")
        tx.matrix.translate(20, 20)
        canvas.add(tx)

        # Draw second gaphas box
        b2 = Box(60, 60)
        b2.min_width = 40
        b2.min_height = 50
        b2.matrix.translate(170, 170)
        canvas.add(b2)

        # Draw gaphas line
        line = Line()
        line.matrix.translate(100, 60)
        canvas.add(line)
        line.handles()[1].pos = (30, 30)

        self.view = view
        self.canvas = canvas
        self.show_all()
        log.info("Workbench loaded")

        view.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        # self.connect('clicked', self.on_field_click)
        # "set-focus-child" container, widget
        self.connect("focus", self.on_field_click)
        self.view.connect("clicked", self.on_field_click_2)

        # musze zrobic swojego toola

        # jest ustawiony DefaultTool teraz,
        # muszę zrobić Toola,
        # działają one tak:
        #    - do view jest ustawiony DefaultTool - ToolChain z Tool'ami
        #    - każdy tool, to taka klasa, przez ktorą przechodzi przez każdą event,
        #      i jak jest obsługiwany to można sobie coś tam zrobić.

        #      no i można złapać sobie event key press, on ustawi flagę co jest naciskane
        #      , w tym samym toolu, zrobić łapanie mouse btton press, oraz główna operacja.
        #      i jak jest w button click i key press (np. CTRL) to wykonaj główną operację.

        #    Tak mogę dodać domyślne dodanie rzeczy, które są w klip boardzie

        #    wydaje mi się że może się

    def on_field_click(self, widget, direction):
        mt = MyText(text="I'm in a box")
        mt.matrix.translate(200, 100)
        self.canvas.add(mt)

        return False

    def on_field_click_2(self, *kwargs, **args):
        self.on_field_click(None, None)
