"""Constants and gloabals used by other spikely modules."""

# Application status bar for user messages
# Usage: config.status_bar.showMessage('message', config.TIMEOUT)
status_bar = None

# Used to represent types of elements
EXTRACTOR, PRE_PROCESSOR, SORTER, POST_PROCESSOR = range(4)

# Identifier to get element object from pipeline model data()
ELEMENT_ROLE = 0x100

# Duration in milliseconds of timeout for temporary status messages
STATUS_MSG_TIMEOUT = 5500
