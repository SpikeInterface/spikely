========
Overview
========

SpikeInterface is a powerful Python based extracellular data processing
framework supporting a broad array of features and functions.  For those well
versed in Python programming, working directly with SpikeInterface is the way
to go.

Spikely, on the other hand, is intended for users who want to take advantage of
SpikeInterface's data processing capabilities, without directly working in
Python.  Instead, Spikely provides a graphical user interface on top of
SpikeInterface optimized for the pipelining of extracelluar data.

Taking full advantage of Spikely requires the user to understand a handful of
key concepts:

- **Element** - An element in Spikely corresponds to the processing nodes used
  in SpikeInterface such as Extractors, Pre-Processors Sorters, Curators, and
  Exporters.
- **Parameter** - Most elements have one or more parameters
  associated with them that can be edited by the user to customize the
  behavior of the associated Element.
- **Pipeline** - Spikely organizes Elements into a pipeline
  where the extracelluar data "flows" from the first Element in the Pipeline
  to the last.

Organization
------------

Related projects
-----------------
