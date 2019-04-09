"""Class definition of SpikePipeline.

Implements the pipeline of SpikeInterface elements responsible
extracellular data processing.
"""

import PyQt5.QtCore as qc

from el_model import SpikeElement


class SpikePipeline(qc.QAbstractItemModel):
    """TBD."""

    STAGE_NAMES = ["Extraction", "Pre-Processing", "Sorting",
                   "Post-Processing"]
    element_dict = {}

    @classmethod
    def get_elements(cls, stage_name):
        """TBD."""
        if len(cls.element_dict) == 0:
            cls._fill_element_dict()
        return cls.element_dict[stage_name]
        
    @classmethod
    def _fill_element_dict(cls):
        """TBD."""
        cls.element_dict[cls.STAGE_NAMES[0]] = [SpikeElement(
            stage=cls.STAGE_NAMES[0], name="Sample Extractor"), 
            SpikeElement("Extraction", "Cole Extractor")]
        
    def __init__(self):
        """TBD."""
        super().__init__()

    def index(row, col, parent):
        """TBD."""
        pass

    def parent(child):
        """TBD."""
        pass
    
    def rowCount():
        """TBD."""
        pass

    def columnCount():
        """TBD."""
        pass

    def data():
        """TBD."""
        pass


    def run(self):
        """TBD."""
        print("Pipeline Running")
        pass

    def clear(self):
        """TBD."""
        print("Pipeline Cleared")
        pass