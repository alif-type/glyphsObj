glyphsObj
=========

This Python 3.6+ library for reading and manipulating Glyphs source files (.glyphs).

Read and write Glyphs data as Python objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from glyphsObj import GSFont

    font = GSFont(glyphs_file)
    font.save(glyphs_file)

The ``glyphsObj.classes`` module aims to provide an interface similar to
Glyphs.app's `Python Scripting API <https://docu.glyphsapp.com>`__.

Note that currently not all the classes and methods may be fully
implemented. We try to keep up to date, but if you find something that
is missing or does not work as expected, please open a issue.

.. TODO Briefly state how much of the Glyphs.app API is currently covered,
   and what is not supported yet.
