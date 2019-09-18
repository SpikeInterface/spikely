========
Overview
========

.. _SpikeInterface: https://github.com/SpikeInterface

SpikeInterface_ is a powerful Python based extracellular data processing
framework supporting a broad range of features and functions.  For those well
versed in Python programming and needing full control over the extracellular
data processing process, working directly with SpikeInterface is the way to go.

Spikely, on the other hand, is for users who want to take advantage of some of
SpikeInterface's processing power without having to program in Python. Instead,
Spikely provides a GUI on top of SpikeInterface_ optimized for a particular use
case: pipelining extracelluar data from a source to a sink while enabling one
or more data transformations along the way.

In addition to being familiar with SpikeInterface_, taking full advantage of
spikely requires an understanding of a few key concepts specific to it:

* **Element** - An element in Spikely corresponds to the processing nodes used
  in SpikeInterface such as Extractors, Pre-Processors Sorters, Curators, and
  Exporters.  Elements are selected by users from drop down menus in spikely.
* **Parameter** - Most elements have one or more parameters associated with
  them that can be edited by the user in spikely to customize the behavior of
  that Element.
* **Pipeline** - The user organizes Elements in spikely into a pipeline where
  extracelluar data "flows" from the first Element in the Pipeline to the last
  when the pipeline is run.  Pipelines, and their associated parameterized
  elements, can be saved for future use therby enabling greater efficiency and
  repeatability.

Workflow
--------

With a solid grounding in SpikeInterface_, and a grasp of spikely's Element,
Parameter, and Pipeline abstractions, the last piece of the puzzle to unlocking
spikely's potential is understanding its workflow and associated UI layout.

.. image:: ../images/gui_annotated.png



Related projects
-----------------
