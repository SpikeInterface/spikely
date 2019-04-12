"""Class definition of SpikePipeline.

Implements the pipeline of SpikeInterface elements responsible
extracellular data processing.
"""

import PyQt5.QtCore as qc
import PyQt5.QtGui as qg

from el_model import SpikeElement


class SpikePipeline():
    """TBD."""

    def __init__(self):
        """TBD."""
        super().__init__()
        self.model = qg.QStandardItemModel()

    def run(self):
        """TBD."""
        print("Pipeline Running")
        pass

    def clear(self):
        """TBD."""
        print("Pipeline Cleared")
        pass

    def get_model():
        return self.model
