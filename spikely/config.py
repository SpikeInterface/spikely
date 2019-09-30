# Constants and helper functions used by other spikely modules

import PyQt5.QtWidgets as qw
import sys

# Duration in milliseconds of timeout for temporary status messages
STATUS_MSG_TIMEOUT = 3500

# Identifier to get element object from pipeline model data()
ELEMENT_ROLE = 0x100

# Column IDs used by QTableView to display element parameter data
PARAM_COL, TYPE_COL, VALUE_COL = 0, 1, 2


def find_main_window():
    # Avoids a global. Used to specify parent for qw.QMessageBox popups
    for widget in qw.QApplication.instance().topLevelWidgets():
        if isinstance(widget, qw.QMainWindow):
            return widget

    # It is a dark day if we end up here
    print('<<spikely fatal error: Failed to find QMainWindow.>>',
          file=sys.stderr)
    sys.exit()
