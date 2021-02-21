#!/usr/bin/env python3

from math import ceil, sqrt
from folders import log
from app.register import register_instance, Register as __
import collections

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa

from gaphas import Canvas, GtkView
from gaphas.geometry import Rectangle, rectangle_intersects
from gaphas.examples import Box as Gaphas_Box, Text as Gaphas_Text
from gaphas.painter import DefaultPainter
from gaphas.item import Line, Item
from gaphas.util import text_extents

from folders.widgets.workbench.rift import obtain_values

Point = collections.namedtuple('Point', ['x', 'y'])
Size = collections.namedtuple('Size', ['width', 'height'])


class ElementManipulator:
    def set_position(self, box: Rectangle):
        log.info("Setting position")
        x, y = box.x, box.y
        self.box.x = x
        self.box.y = y

        self.element.matrix.translate(x, y)


class Container(ElementManipulator):
    def __init__(self, key: str, value: object, box: Rectangle, element: type):
        log.info(f"Made element {key}")
        self.key = key
        self.value = value
        self.box = box
        self.element = build_elements(element, box)


class Text(Gaphas_Text):
    """
    Text with experimental connection protocol.
    """

    def draw(self, context):
        Gaphas_Text.draw(self, context)
        cr = context.cairo
        w, h = text_extents(cr, self.text, multiline=self.multiline)
        cr.rectangle(-25, -15, w + 50, h + 30)
        cr.stroke()


class Box(Gaphas_Box):
    def __init__(self, box: Rectangle):
        super(Gaphas_Box, self).__init__(box.width, box.height)
        self.matrix.translate(box.x, box.y)


def build_elements(Type: Container, rectangle: Rectangle):
    return Type(rectangle)


class object_register(dict):
    """
    Dictionary with elements:

    key: tuple(obj.Rectangle)
    value: obj

    in other words, a key is tuple with pos/size rectangle
    value is the object
    """

    def register(self, object: Container) -> None:
        self[id(object)] = object

    def get_visible_objects(self, viewport: Rectangle) -> list:
        return [
            element
            for key, element in self.items()
            if rectangle_intersects(tuple(viewport), tuple(element.box))
        ]

    def add_to_canvas(self, canvas):
        for container in self.values():
            canvas.add(container.element)


viewport = Rectangle(0, 0, 800, 600)


def build_rows_cols(iterable):
    count = len(iterable)
    row_width = ceil(sqrt(count))

    horizontal_space, vertical_space = 50, 25

    return [(x, y) for x in range(row_width) for y in range(row_width)]


def organize_elements(index: object_register):
    log.info("Organizing elements")
    containers = index.values()

    count = len(containers)
    row_width = ceil(sqrt(count))

    horizontal_space, vertical_space = 120, 60
    offset_x, offset_y = 100, 100

    rows_cols = [(x, y) for x in range(row_width) for y in range(row_width)]

    for position, container in enumerate(index.values()):
        log.debug(f"Moving element to {rows_cols[position]}")
        print(rows_cols[position])
        row, col = rows_cols[position]
        box = Rectangle(
            offset_x + row * horizontal_space, offset_y + col * vertical_space, 40, 15
        )
        container.set_position(box)


def interpreter():
    log.info("Interpreting folders")
    index = object_register()

    files = obtain_values()

    for i, value in enumerate(files):
        container = Container(
            key=value.path, value=value, box=Rectangle(0, 0, 40, 15), element=Text
        )
        container.element.text = value.name
        index.register(container)

    organize_elements(index)

    return index


@register_instance
class Workbench(Gtk.Box):
    "Main area of user interface content."

    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)

        log.info("Loading Workbench")
        canvas = Canvas()
        view = GtkView()
        __.canvas = canvas
        __.view = view
        view.painter = DefaultPainter()
        view.canvas = canvas
        self.pack_start(view, True, True, 20)
        self.index = interpreter()

        self.index.add_to_canvas(canvas)
        # # Draw first gaphas box
        # b1 = Box(Rectangle(1, 0, 60, 60))
        # canvas.add(b1)

        # tx = Text(text="joo")
        # tx.matrix.translate(20, 20)
        # canvas.add(tx)

        # # Draw second gaphas box
        # b2 = Box(Rectangle(170, 170, 60, 60))
        # canvas.add(b2)

        # # Draw gaphas line
        # line = Line()
        # line.matrix.translate(100, 60)
        # canvas.add(line)
        # line.handles()[1].pos = (30, 30)

        self.view = view
        self.canvas = canvas
        self.show_all()
        log.info("Workbench loaded")

        view.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        # self.connect('clicked', self.on_field_click)
        # "set-focus-child" container, widget
        self.connect("focus", self.on_field_click)
        # view.connect("clicked", self.on_field_click_2)

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
        mt = Text(text="I'm in a box")
        mt.matrix.translate(200, 100)
        self.canvas.add(mt)

        return False

    def on_field_click_2(self, *kwargs, **args):
        self.on_field_click(None, None)
