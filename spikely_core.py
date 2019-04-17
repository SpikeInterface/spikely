"""Initializes constants for use within Spikely
"""

import PyQt5.QtWidgets as qw


_main_window = None

# Stage ID constants
EXTR, PREP, SORT, POST = range(4)

# Stage name constants
STAGE_NAMES = [
    "Extraction",
    "Pre-Processing",
    "Sorting",
    "Post-Processing"
]


def spikely_msg_box(win, pri_text="The nicest thing about the rain is "
                    "that it always stops.", sec_text="Eventually."):
    msg_box = qw.QMessageBox(win)
    msg_box.setIcon(qw.QMessageBox.Warning)
    msg_box.setWindowTitle("Spikely")
    msg_box.setText(pri_text)
    msg_box.setInformativeText(sec_text)
    msg_box.setStandardButtons(qw.QMessageBox.Ok)
    msg_box.exec()
