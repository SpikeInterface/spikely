"""
Spikely - an application built on top of SpikeInterface to create and run
extracellular data processing pipelines

The application is designed to allow users to load an extracellular recording,
run preprocessing on the recording, run an installed spike sorter, and then perform
postprocessing on the results. All results are saved into a folder.

Author: Roger Hurwitz
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

SPIKELY_VERSION = "0.2"

class Spikely(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        run_btn, queue_btn, clear_btn = (QPushButton("Run"),
            QPushButton("Queue"), QPushButton("Clear"))
        # buttons = [QPushButton(button) for button in "Run Queue
        # Clear".split()]

        # Pipeline
        list = QListView();
        list.setMinimumSize(200, 200)

        model = QStandardItemModel(list)

        elements = [
            "Recording Extractor",
            "Pre-Sort Filter",
            "Sorter",
            "Post-Sort Filter",
            "Sort Extractor"
            "Recording Extractor",
            "Pre-Sort Filter",
            "Sorter",
            "Post-Sort Filter",
            "Sort Extractor"
        ]

        for element in elements:
            item = QStandardItem(element)
            model.appendRow(item)
        
        list.setModel(model)


        # Buttons at the bottom
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(run_btn)
        hbox.addWidget(queue_btn)
        hbox.addWidget(clear_btn)

        gbox = QGroupBox("Operations")
        gbox.setLayout(hbox)

        # for button in buttons:
        #    hbox.addWidget(button)

        # Overall vertical label
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(list)
        vbox.addWidget(gbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle("Spikely " + SPIKELY_VERSION)
        self.setWindowIcon(QIcon("spikely.png"))

        self.show()

if __name__ == '__main__':
  
    app = QApplication(sys.argv)
    w = Spikely()
    sys.exit(app.exec_())
