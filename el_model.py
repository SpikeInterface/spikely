"""Class definition of SpikeElement.

Implements the SpikeInterface elements responsible extracellular data
processing.
"""

import spikely_constants as sc


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
            SpikeElement(sc.EXTR, "Extractor A"),
            SpikeElement(sc.EXTR, "Extractor B"),
            SpikeElement(sc.EXTR, "Extractor C"),
            SpikeElement(sc.EXTR, "Extractor D")])
        cls._avail_elements.append([
            SpikeElement(sc.PREP, "Pre-Processor A"),
            SpikeElement(sc.PREP, "Pre-Processor B"),
            SpikeElement(sc.PREP, "Pre-Processor C"),
            SpikeElement(sc.PREP, "Pre-Processor D")])
        cls._avail_elements.append([
            SpikeElement(sc.SORT, "Sorter A"),
            SpikeElement(sc.SORT, "Sorter B"),
            SpikeElement(sc.SORT, "Sorter C"),
            SpikeElement(sc.SORT, "Sorter D")])
        cls._avail_elements.append([
            SpikeElement(sc.POST, "Post-Processor A"),
            SpikeElement(sc.POST, "Post-Processor B"),
            SpikeElement(sc.POST, "Post-Processor C"),
            SpikeElement(sc.POST, "Post-Processor D")])

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
