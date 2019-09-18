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
  that element.
* **Pipeline** - The user organizes elements in spikely into a series where
  extracelluar data "flows" from the first element in the Pipeline to the last
  when the pipeline is run.  Pipelines, and their associated parameterized
  elements, can be saved for future use therby enabling greater efficiency and
  repeatability.

Workflow
--------

With a solid grounding in SpikeInterface_, and a grasp of spikely's element,
parameter, and pipeline abstractions, the last piece of the puzzle to unlocking
spikely's potential is understanding its workflow and associated UI layout.

.. image:: ../images/gui_annotated.png

1. **Constructing the Pipeline** - The user constructs a pipeline in spikely by
choosing the element category (e.g., *Extractors*), choosing one of the
installed elements within that category (e.g., *MdaRecordingExtractor*) and
then adding that element to the pipeline using the "Add Element" button.
Individual elements added to the pipeline can be moved up, moved down, or
deleted as part of pipeline construction process.  Note, there are pipeline
policies enforced by spikely related to ordering and singularity that limit
certain pipeline permutations.

2. **Configuring Element Parameters** - When an element is selected in the
*Construct Pipeline* part of the UI that element's parameters are displayed in
the *Configure Elements* part of the UI.

Related projects
-----------------
