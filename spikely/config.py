"""Constants and gloabals used by other spikely modules."""

from enum import Enum

# Duration in milliseconds of timeout for temporary status messages
STATUS_MSG_TIMEOUT = 3500

# Symbolic constants for different subclasses of SpikeElement
EXTRACTOR, PRE_PROCESSOR, SORTER, CURATOR, EXPORTER = range(5)

# Identifier to get element object from pipeline model data()
ELEMENT_ROLE = 0x100

# Column IDs used by QTableView to display element parameter data
PARAM_COL, TYPE_COL, VALUE_COL = 0, 1, 2


class ElementTypes(Enum):
    EXTRACTOR = 'Extractor'
    PRE_PROCESSOR = 'Pre-Processor'
    SORTER = 'Sorter'
    CURATOR = 'Curator'
    EXPORTER = 'Exporter'
