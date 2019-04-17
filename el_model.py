"""Class definition of SpikeElement.

Implements the SpikeInterface elements responsible extracellular data
processing.
"""

import spikely_core as sc


class SpikeElement:
    """TBD."""

    _avail_elements = []

    @classmethod
    def avail_elements(cls, stage_id):
        """TBD."""
        if len(cls._avail_elements) == 0:
            cls._fill_avail_elements()
        return cls._avail_elements[stage_id]

    @classmethod
    def _fill_avail_elements(cls):
        """TBD."""
        cls._avail_elements.append([
            SpikeElement(sc.EXTRACT, "Extractor A"),
            SpikeElement(sc.EXTRACT, "Extractor B"),
            SpikeElement(sc.EXTRACT, "Extractor C"),
            SpikeElement(sc.EXTRACT, "Extractor D")])
        cls._avail_elements.append([
            SpikeElement(sc.PREPROC, "Pre-Processor A"),
            SpikeElement(sc.PREPROC, "Pre-Processor B"),
            SpikeElement(sc.PREPROC, "Pre-Processor C"),
            SpikeElement(sc.PREPROC, "Pre-Processor D")])
        cls._avail_elements.append([
            SpikeElement(sc.SORTING, "Sorter A"),
            SpikeElement(sc.SORTING, "Sorter B"),
            SpikeElement(sc.SORTING, "Sorter C"),
            SpikeElement(sc.SORTING, "Sorter D")])
        cls._avail_elements.append([
            SpikeElement(sc.POSTPROC, "Post-Processor A"),
            SpikeElement(sc.POSTPROC, "Post-Processor B"),
            SpikeElement(sc.POSTPROC, "Post-Processor C"),
            SpikeElement(sc.POSTPROC, "Post-Processor D")])

    def __init__(self):
        """TBD."""
        self._stage_id = None
        self._name = None

    def __init__(self, stage_id, name):
        """TBD."""
        self._stage_id = stage_id
        self._name = name

    def set_name(self, name):
        """TBD."""
        self._name = name

    def name(self):
        """TBD."""
        return self._name

    def set_stage_id(self, stage_id):
        """TBD."""
        self._stage_id = stage_id

    def stage_id(self):
        """TBD."""
        return self._stage_id

    def __repr__(self):
        return self._name

    def __str__(self):
        return self._name
