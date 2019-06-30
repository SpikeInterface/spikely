"""Constants and gloabals used by other spikely modules."""

# Application status bar for user messages.  Set in spikely.py
# Usage: config.status_bar.showMessage('message', config.TIMEOUT)
status_bar = None

# Duration in milliseconds of timeout for temporary status messages
STATUS_MSG_TIMEOUT = 3500

# Application main window used to anchor dialog boxes.  Set in spikely.py
main_window = None

# Used to represent types of elements
EXTRACTOR, PRE_PROCESSOR, SORTER, CURATOR = range(4)

# Identifier to get element object from pipeline model data()
ELEMENT_ROLE = 0x100

# Column IDs used by QTableView to display element parameter data
PARAM_COL = 0
VTYPE_COL = 1
VALUE_COL = 2
