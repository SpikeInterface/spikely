===================================
spikely
===================================

A simple extracellur data processing application based on SpikeInterface
========================================================================

SpikeInterface is a powerful Python based extracellular data processing
framework supporting a broad array of features and functions.  For those well
versed in Python programming, working directly with SpikeInterface is the way
to go.

Spikely, on the other hand, is intended for users who want to take advantage of
SpikeInterface's data processing capabilities, without the need of directly
working in Python.  Instead, Spikely provides a graphical user interface on top
of SpikeInterface optimized for the pipelining of extracelluar data.

Taking full advantage of Spikely requires the user to understand a handful of
key concepts:

  - **Element** - An element in Spikely corresponds to the
    processing nodes used in SpikeInterface such as Extractors, Pre-Processors
    Sorters, Curators, and Exporters.
  - **Parameter** - Most elements have one or more parameters
    associated with them that can be edited by the user to customize the
    behavior of the associated Element.
  - **Pipeline** - Spikely organizes Elements into a pipeline
    where the extracelluar data "flows" from the first Element in the Pipeline
    to the last.

Spikely is an application built on top of SpikeInterface designed to create and
run extracellular data processing pipelines within a GUI. Spikely currently
supports loading, preprocessing, sorting, and curating extracellular datasets
that are stored in SpikeInterface compatible file formats.

.. image:: ../images/gui.png

- read many file formats
- pre-process extracellular recordings
- run several popular spike sorters
- curate the spike sorting output

.. toctree::
  :maxdepth: 1
  :caption: Contents:

  overview

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
