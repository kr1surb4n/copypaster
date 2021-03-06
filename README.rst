==================
Copypaster
==================


.. image:: https://img.shields.io/pypi/v/copypaster.svg
        :target: https://pypi.python.org/pypi/copypaster

.. image:: https://img.shields.io/travis/audreyr/copypaster.svg
        :target: https://travis-ci.org/audreyr/copypaster

.. image:: https://readthedocs.org/projects/copypaster/badge/?version=latest
        :target: https://copypaster.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/audreyr/copypaster/shield.svg
     :target: https://pyup.io/repos/github/audreyr/copypaster/
     :alt: Updates

Copypaster - a copy/paste tool that aims to change your
work into simple copy-pasting actions by displaying snippets as a list. I want to code like I play Starcraft - by choosing what to build from a list and not check in documentation all the time, before I remember.


It creates rows of buttons, which when pressed, write
to your clipboard some value that you stored earlier.

Inspired by my private method of coding - copy/pasting.
Where most of my code is copied from other parts of the software I'm working on. Not remember all the functions, but choose from a list and have no worries if I typed anything wrong.

Also, working in a corporate environment tool like clipboard manager proved itself usefull - you have a lot
of problems daily that require the same message.


Written using Python and GTK3

* Free software: MIT license

Running
-----------

Run `git submodule update --init` to download the snippets from `https://github.com/kr1surb4n/copypaster_filedecks`

Run `pip install -r requirements.txt && pip install -e . && copypaster`  (after this you can use only `copypaster`)



Features
--------

* Autosave mode - what you copy is saved in Copypaster
* Quick add, remove and edit snippet. Add folders.
* Snippets are kept in files, inside folders.
* With folders you can have a tree structure, that allows to store many objects, and use them with ease. 
* TODO Images on buttons

TODO
----
1. File loader should check if the file is a text file (do not load binary)
2. Snippets are loading slow. (logging is a drag)
   a) Do performance checks.
        - add vprof and profiler output
   b) Add some info for user that stuff is loading (splash)
4. Load CTAGS files as functions and variable names in different tabs (add notebook)
   - choose file to use
   - check if changes
6. implement test for copypaster components
7. extract app as stand alone project

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
