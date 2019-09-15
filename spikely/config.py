"""Constants and gloabals used by other spikely modules."""

# Application status bar for user messages.  Set in spikely_main.py
# Usage: config.status_bar.showMessage('message', config.TIMEOUT)
status_bar = None

# Duration in milliseconds of timeout for temporary status messages
STATUS_MSG_TIMEOUT = 3500

# Set in spikely_main, needed as parent to create dialogs in modules
main_window = None

# Symbolic constants for different subclasses of SpikeElement
EXTRACTOR, PRE_PROCESSOR, SORTER, CURATOR, EXPORTER = range(5)

# Identifier to get element object from pipeline model data()
ELEMENT_ROLE = 0x100

# Column IDs used by QTableView to display element parameter data
PARAM_COL, TYPE_COL, VALUE_COL = 0, 1, 2
