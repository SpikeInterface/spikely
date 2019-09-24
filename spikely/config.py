"""Constants and helper functions used by other spikely modules."""
import PyQt5.QtWidgets as qw

# Duration in milliseconds of timeout for temporary status messages
STATUS_MSG_TIMEOUT = 3500

# Identifier to get element object from pipeline model data()
ELEMENT_ROLE = 0x100

# Column IDs used by QTableView to display element parameter data
PARAM_COL, TYPE_COL, VALUE_COL = 0, 1, 2


def find_main_window():
    # Global function to find the (open) QMainWindow in application
    app = qw.QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, qw.QMainWindow):
            return widget
    return None
