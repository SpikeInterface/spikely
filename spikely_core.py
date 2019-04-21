"""Constants and utilities used by other spikely modules.
"""

import PyQt5.QtWidgets as qw


_main_window = None

# Numeric constants representing pipeline stages
EXTRACT, PREPROC, SORTING, POSTPROC = range(4)

# User friendly names for pipeline stages
STAGE_NAMES = ["Extractors", "Pre-Processors", "Sorters",
               "Post-Processors"]

ELEMENT_ROLE = 0x100


def spikely_msg_box(win, text="The nicest thing about the rain is "
                    "that it always stops.", informative_text="Eventually."):
    msg_box = qw.QMessageBox(win)
    msg_box.setIcon(qw.QMessageBox.Information)
    msg_box.setWindowTitle("Spikely Message")
    msg_box.setText(text)
    msg_box.setInformativeText(informative_text)
    msg_box.setStandardButtons(qw.QMessageBox.Ok)
    msg_box.exec()
