
import gi
import pytest
import threading
from time import sleep
import logging as log
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject  # noqa

import folders
from folders import PROJECT_DIR
from folders.main import GLADE_FILE
from folders.builder import builder
from folders.widgets.workbench import (
    Workbench, Canvas, 
    build_elements, 
    object_register, 
    viewport, 
    organize_elements, 
    interpreter)  
from folders.widgets.workbench.rift import Location


"""
Folders

a view/prespective is a set of
inforamtions and function represented
in python code, that are used to display
and manipulate folders and files,
the items on the file system.
"""
@pytest.mark.skip()
def test_folders_works():
    from folders.main import main_function
    folders = threading.Thread(target=main_function, args=(1,))
    folders.start()

    sleep(1)
    assert folders.is_alive()

def test_add_workbench_to_glade():
    WORKBENCH='Workbench'

    # builder returns Workbench class on name
    instance = builder.get_type_from_name(WORKBENCH)
    assert instance == GObject.GType(Workbench)

    builder.add_from_file(GLADE_FILE)
    workbench = builder.get_object(WORKBENCH.lower())
    
    assert isinstance(workbench, type(Workbench()))
    

def test_display_workbench():
    """
    Workbench is the floor on which you
    stand the blocks(elements).
    The background.

    Display it."""
    
    workbench = Workbench()
    assert workbench.canvas
    assert workbench.index
    assert workbench.view
    assert workbench.location

    assert workbench.diagram

    assert isinstance(workbench.canvas, type(Canvas()))

def test_definition_of_elements():
    """Elements needs to be defined,

    the folders view has:
    - files
    - folders

    editor view (default) has:
    - text
    - box

    every element has label.

    definitions have defined values.
    folder and files have paths and 
    (maybe) attributes.
join
    text has content.

    box has other elements.

    a loadable definition is needed.
    Start from python code.
    """
    pass

def test_use_diagram_on_workbench():
    """Try using diagram from Gaphor
    (/home/kris/workshops/tools/copypaster/lib/gaphor/gaphor/core/modeling/diagram.py)
        the goal is to use the elements of the gaphor to get the diagrams styled
        by css"""

    """Create your own diagram class that you use as the diagram
    without the all the extra things """
    pass


    """Take elements from gaphor"""
    """Use Item and StyledItem for the styles"""

def test_styles_of_elements():
    """
    Having definitions, the elements
    need their distinct styles.

    Editor also needs default styles.
    
    a loadable definition is needed.
    Start from python code.
    """
    pass

    """
    Gaphor has an ItemPainter,
    (gaphor/gaphor/diagram/painter.py)
    that, takes a selection, then (diagram has a style something)
    there is StyledItem, 
    that generates some "style" and that is painted

    Gaphas has almost the same Painter (i need to take it)
    
    """


def test_elements_organiser():
    """Views have organiser that
    is responsible for organising elements on
    the workbench.

    Folders have a simple organizer:
    - first folders, later files
    - hidden folders and files are shown after normal
    - names sort (maybe other attributes)
    - organized in rows and columns

    from top left to right down, to max window width.
    stable padding.
    """
    pass

def test_actions_on_elements():
    """
    Every type of element should have
    actions menu, that displays default
    actions defined with 
    types(elements) definitions.

    action menu can also load functions defined
    by user from outside. 

    actions for view.
    actions for elements.

    (hooks on actions?)
    """
    pass


def test_rift():
    """A rift is the users window. The frames
    through he looks onto the infinite workbench.

    Rift sets the position and defines location.
    A clean rift is opened on Lat 0 Lng 0.
    With elevetion.(or zoom)

    Folders open rift at 0,0,0
    Plateu open at saved position.
    
    Rift can display elements at a given
    location(workbench address) at 
    the displayed rift coordinates.
    (adding stuff above the area
    you are looking at)
    """
    pass

def test_rift():
    """Rift saves position in coordinates,
    """
    pass

def test_move_rift_with_wsad():
    """Change the possitio of the rift
    by pressing W,S,A,D keys, like in a game.
    """
    pass

def test_go_up_down_with_right_using_mouse_scroll():
    """And pageup and pagedown.

        change elevation of the rift (zoom in/out) using
        scroll and pageup/down buttons
    """
    pass


def test_provide_button_to_go_to_center_of_rift():
    """Provide a button that will change possition
    to 0,0,0"""
    pass

def test_view_interpreter():
    """
    Interpreter is the mechanism that
    translates a given workbench addres,
    and according to the view
    represents the elements
    
    folders is a view that displays
    folders and files.

    interpreter translates given
    entities to their corresponding
    representations. 
    """
    pass

def test_view_mainpulator():
    """
    Manipulator is the mechanism that
    allows the manipulation
    of represented entities by
    actions triggered on workbench elements
    """
    pass


def test_workbench_has_and_address():
    """
    A workbench has an address.
    Its a path, an url, folder, file,
    database, network - any fucking thing.
    
    workbench displays that location
    with an interpreter. 

    elements that are displayed on the
    workbench are related to the view.

    folders is a view that displays files
    and folders. the address is the
    path to folder. (curren folder)
    
    display elements of project folder.
    """

    workbench = Workbench()
    assert workbench.location
    assert isinstance(workbench.location, Location)
    assert workbench.location.value == PROJECT_DIR
    
def test_left_click_on_workbench():
    """When clicked on workbench with
        left mouse button
       everything is deselected. """
    pass

def test_right_click_on_workbench():
    """
    When clicking on workbench with 
        right mouse button
       an workbenchs actions right-mouse-click menu
       is displayed"""
    pass

def test_double_left_click_on_workbench():
    """When clicking on workbench with
        double left click
        an empty element of type "set as default"
        is created under the cursor"""
    pass

# tools are needed to operate and define
# the default left/right click(and drag)

def test_right_click_on_element():
    """When you click on element with right mouse button,
    an element actions right-mouse-click menu is
    displayed"""
    pass

def test_double_left_click_on_element():
    """
    When you double click stuff on element,
    you either
    open a program
    open a defined action
    open a defined action in view
    open insides of that element in a new window.
    
    probably some abstract of that"""
    pass