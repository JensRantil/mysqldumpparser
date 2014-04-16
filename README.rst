MySQL SQL dump parser
=====================
This is a small Python application that parses a MySQL dump taken using
`mysqldump` and outputs the content of the dump in CSV format.

The application relies on the excellent pyparsing_ library to do the actual
parsing.

.. _pyparsing: http://pyparsing.wikispaces.com

The implementation is slow and was more like a proof of concept to see if
parsing the dump was a viable alternative to convert to CSV. For a faster
alternative, have a look at http://www.github.com/JensRantil/mysqlcsvdump.

Running tests
-------------
Basic tests can be executed using Python's doctest::

    python -m doctest sqlparser.py

Who made this?
--------------
I'm Jens Rantil. Have a look at `my blog`_ for more info on what I'm working
on.

.. _my blog: http://jensrantil.github.io/pages/about-jens.html
