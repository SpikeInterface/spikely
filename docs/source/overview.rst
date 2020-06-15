
Overview
========

.. _SpikeInterface: https://github.com/SpikeInterface

SpikeInterface_ is a powerful Python-based extracellular data processing
framework supporting a broad range of features and functions.  Its power and
breadth come at a price, however, and that price is complexity.  But for those
well-versed in Python programming and needing full control over the
extracellular data processing process, working directly with SpikeInterface is
the way to go.

Spikely, on the other hand, is for users who want to take advantage of
SpikeInterface without having to program in Python. Spikely provides a GUI on
top of SpikeInterface optimized for a specific use case: pipelining
extracelluar data from a source to a sink while enabling one or more data
transformations along the way.  In exchange for its ease of use and efficiency,
spikely sacrifices some of SpikeInterface's power and breadth. Spikely
therefore complements, rather than replaces, SpikeInterface.

.. tip::
   One of scenarios we had in mind when making spikely was enabling bulk
   extracelluar data processing in the lab.  After data collection, running a
   standard series of transformations may be the next step prior to a deeper
   dive on the data.  In that case using spikely may improve overall
   throughput.

Because of the close relationship between spikely and SpikeInterface, it is
important for the spikely user to have a grounding in the concepts behind
SpikeInterface.  If you are not already familiar with SpikeInterface, a good
place to get started is its `online documentation
<https://spikeinterface.readthedocs.io/en/latest/overview.html>`_

In addition to being familiar with SpikeInterface, taking full advantage of
spikely requires an understanding of a few key concepts specific to it:

* **Element** - An element in Spikely corresponds to entities exposed by
  the data processing nodes in SpikeInterface.  To be used in spikely, the
  underlying SpikeInterface entity must already be installed on the user's
  system. For information on installing SpikeInterface entities like Spike
  Sorters, check out `this document
  <https://spikeinterface.readthedocs.io/en/latest/sortersinfo.html>`_.

  Elements in spikely consist of:

    * *Extractors* - Extractors read raw extracelluar data
      from files, and make those data available to downstream elements in the
      pipeline. Extractor names correspond to the raw extracellular
      data format they support. Spikely requires one, and only one, Recording
      Extractor per pipeline.

    * *Pre-Processors* - Pre-Processors transform data sourced into the
      pipeline by the Extractor before it is sent to the Sorter.
      Pre-processors are optional. Spikely supports multiple Pre-Preprocessors
      per pipeline between the Extractor and the Sorter.

    * *Sorters* - Spike sorting is a big part of SpikeInterface, and spikely's
      Sorters correspond closely to spike sorters in SpikeInterface. Spikely
      requires the presence of one, and only one, Sorter in the pipeline.
      Sorters write their results out to a file (unless specified not to)
      allowing a Sorter to act as a terminating sink in a spikely pipeline.

    * *Curators* - Curators, also known as post-processors, automatically
      curate sorted data produced by the Sorter and output them downstream to
      either another Curator or to a pipeline terminating Exporter.  Curators
      are optional. Spikely supports multiple Curators per pipeline.

    * *Exporters* - Exporters act as data sinks, transforming
      sorted datasets into different formats. Exporters are optional, and
      spikely only supports a single Exporter per pipeline.

* **Parameter** - Most elements have one or more parameters associated with
  them that can be edited by the user in spikely to customize the behavior of
  that element during the execution of a pipeline. Parameters are element
  specific, and some familiarity with the proxied node in SpikeInterface is
  required to correctly configure an element.

* **Pipeline** - The user organizes elements in spikely in a series where
  extracelluar data "flows" from the first element in the Pipeline to the last
  when the pipeline is run.  Pipelines, and their associated parameterized
  elements, can be saved for future use thereby enabling greater efficiency and
  repeatability.
