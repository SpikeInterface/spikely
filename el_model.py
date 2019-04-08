"""Class definition of SpikeElement.

Implements the SpikeInterface elements responsible extracellular data processing.
"""

# from pi_model import SpikePipeline

class SpikeElement:
    """TBD."""

    def __init__(self):
        """TBD."""
        self.stage = None
        self.name = None
    
    def __init__(self, stage, name):
        """TBD."""
        self.stage = stage
        self.name = name

    def set_name(self, name):
        """TBD."""
        self.name = name

    def get_name(self):
        """TBD."""
        return self.name
    
    def set_stage(self, stage):
        """TBD."""
        self.stage = stage

    def get_stage(self):
        """TBD."""
        return self_stage