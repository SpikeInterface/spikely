"""
Spikely - an application built on top of SpikeInterface to create and run
extracellular data processing pipelines

The application is designed to allow users to load an extracellular recording,
run preprocessing on the recording, run an installed spike sorter, and then perform
postprocessing on the results. All results are saved into a folder.

Author: Roger Hurwitz
"""

import sys
from PyQt5.QtWidgets import (QApplication, QPushButton, QWidget, 
    QTreeWidget, QTreeWidgetItem, QHBoxLayout, QGroupBox,
    QVBoxLayout)
from PyQt5.QtGui import QStandardItemModel, QIcon

SPIKELY_VERSION = "0.2"

class Spikely(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()


    def clicked(self, item, column):
        print("Clicked")


    def initUI(self):
        # Actions that will apply to the processing pipeline
        self.run_btn, self.queue_btn, self.clear_btn = (QPushButton("Run"),
            QPushButton("Queue"), QPushButton("Clear"))

        # Create the processing pipeline model and view
        self.pipe_tree = QTreeWidget(self)
        self.pipe_tree.setColumnCount(1)
        self.pipe_tree.setHeaderLabels(["Processing Elements"])
        self.pipe_tree.header().hide()
        self.pipe_tree.itemClicked.connect(self.clicked)

        rec_ext = QTreeWidgetItem(self.pipe_tree)
        rec_ext.setText(0, "Stage 1: Recording Extractors")
        item = QTreeWidgetItem()
        item.setText(0, "Sample Recording Extractor #1")
        rec_ext.addChild(item)
        item = QTreeWidgetItem()
        item.setText(0, "Sample Recording Extractor #2")
        rec_ext.addChild(item)


        # Buttons at the bottom
        hbox = QHBoxLayout()
        hbox.addWidget(self.run_btn)
        hbox.addWidget(self.queue_btn)
        hbox.addWidget(self.clear_btn)
        hbox.addStretch(1)

        gbox = QGroupBox("Operations")
        gbox.setLayout(hbox)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.pipe_tree)
        vbox.addWidget(gbox)
        self.setLayout(vbox)

    


if __name__ == '__main__':
  
    app = QApplication(sys.argv)
    
    w = Spikely()
    w.setGeometry(300, 300, 300, 220)
    w.setWindowTitle("Spikely " + SPIKELY_VERSION)
    # w.setWindowIcon(QIcon("spikely.png"))
    w.show()

    sys.exit(app.exec_())
