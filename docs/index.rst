.. PyVic2WarAnalyzer documentation master file, created by
   sphinx-quickstart on Tue Jul 20 22:27:01 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyVic2WarAnalyzer's documentation!
=============================================

I created this module because I was bored and because I wanted to make a discord bot with it.

Classes and methods
=========================

Pyvic2waranalyzer.main
-----------------------------

.. autoclass:: pyvic2waranalyzer.GameFile

    :param localisation_folder: Indicates a localisation folder with .csv files.
    :type localisation_folder: :class:`str` or :class:`list` or :class:`None`
    :param lang: Indicates the language to translate.
    :type lang: :class:`str`

.. automethod:: pyvic2waranalyzer.GameFile.scan

Pyvic2waranalyzer.utils
-----------------------------

.. autoclass:: pyvic2waranalyzer.utils.types.Unit

.. autoclass:: pyvic2waranalyzer.utils.types.War

.. autoclass:: pyvic2waranalyzer.utils.types.Battle

.. autoclass:: pyvic2waranalyzer.utils.types.Wargoal

.. autoclass:: pyvic2waranalyzer.utils.types.OriginalWargoal

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
