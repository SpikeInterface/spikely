Workflow
========

.. _SpikeInterface: https://github.com/SpikeInterface

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
   *Construct Pipeline* part of the UI that element's parameters are displayed
   in the *Configure Elements* part of the UI.
