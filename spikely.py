"""
Spikely - an application built on top of SpikeInterface to create and run
extracellular data processing pipelines

The application is designed to allow users to load an extracellular recording,
run preprocessing on the recording, run an installed spike sorter, and then perform
postprocessing on the results. All results are saved into a folder.
"""

__author__ = "Roger Hurwitz"
__credits__ = ["Cole Hurwitz"]
__license__ = "GPL"
__version__ = "0.1.5"
__maintainer__ = "Roger Hurwitz"
__email__ = "rogerhurwitz@gmail.com"
__status__ = "Development"

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget,
    QTreeWidget, QTreeWidgetItem, QHBoxLayout, QGroupBox, QFrame,
    QVBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtGui import QStandardItemModel, QIcon

class Spikely(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        # Set attributes of applicaiton window
        self.setWindowTitle("Spikely " + __version__)
        self.setGeometry(100, 100, 800, 400)
        self.setWindowIcon(QIcon("spikely.png"))

        # Processing pipeline model and view
        self.pipe_tree = QTreeWidget(self)
        self.pipe_tree.setColumnCount(1)
        self.pipe_tree.header().hide()
        # self.pipe_tree.itemClicked.connect(self.clicked)
        # self.pipe_tree.setItemsExpandable(False)

        stagelist = [
            "Stage 1: Recording Extractors", 
            "Stage 2: Pre-Processing",
            "Stage 3: Sorters", 
            "Stage 4: Post-Processing"
        ]
        
        for stage in stagelist:
            an_item = QTreeWidgetItem(self.pipe_tree)
            an_item.setText(0, stage)
            # an_item.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicator)
            an_item.setExpanded(True)
            child = QTreeWidgetItem()
            child.setText(0, "Sample Element")
            an_item.addChild(child)
          

        # Pipeline element commands
        self.up_btn, self.delete_btn, self.down_btn = (QPushButton("Move Up"),
            QPushButton("Delete"), QPushButton("Move Down"))
        pec_box = QFrame()
        hbox = QHBoxLayout()
        hbox.addWidget(self.up_btn)
        hbox.addWidget(self.delete_btn)
        hbox.addWidget(self.down_btn)
        pec_box.setLayout(hbox)

        # Add pipeline elements
        stage_cbx = QComboBox()
        stage_cbx.addItem("Recording")
        stage_cbx.addItem("Pre-Process")
        stage_cbx.addItem("Sorters")
        stage_cbx.addItem("Post-Process")

        ele_cbx = QComboBox()
        ele_cbx.addItem("Element #1")
        ele_cbx.addItem("Element #2")
        ele_cbx.addItem("Element #3")

        ele_box = QFrame()
        hbox = QHBoxLayout()
        hbox.addWidget(stage_cbx)
        hbox.addWidget(ele_cbx)
        hbox.addWidget(QPushButton("Add Element"))
        ele_box.setLayout(hbox)

        # Combine pipeline tree and element commands
        pipe_box = QGroupBox("Pipeline Elements")
        vbox = QVBoxLayout()
        vbox.addWidget(ele_box)
        vbox.addWidget(self.pipe_tree)
        vbox.addWidget(pec_box)
        pipe_box.setLayout(vbox)

        # Pipeline operation commands
        self.run_btn, self.queue_btn, self.clear_btn = (QPushButton("Run"),
            QPushButton("Queue"), QPushButton("Clear"))
        poc_box = QGroupBox("Pipeline Operations")
        hbox = QHBoxLayout()
        hbox.addWidget(self.run_btn)
        hbox.addWidget(self.queue_btn)
        hbox.addWidget(self.clear_btn)
        # hbox.addStretch(1)
        poc_box.setLayout(hbox)

        # Element Properties
        prop_tbl = QTableWidget()
        prop_tbl.setRowCount(10)
        prop_tbl.setColumnCount(2)
        prop_tbl.setHorizontalHeaderLabels(("Property", "Value"))
        prop_tbl.setColumnWidth(0, 200)
        prop_tbl.setColumnWidth(1, 100)
        prop_tbl.verticalHeader().hide()
        prop_tbl.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        prop_box = QGroupBox("Element Properties") 
        hbox = QHBoxLayout()
        hbox.addWidget(prop_tbl)
        prop_box.setLayout(hbox)

        ele_frame = QFrame()
        hbox = QHBoxLayout()
        hbox.addWidget(pipe_box)
        hbox.addWidget(prop_box)
        ele_frame.setLayout(hbox)


        # Layout of main window
        main_box = QVBoxLayout()
        main_box.addStretch(1)
        main_box.addWidget(ele_frame)
        main_box.addWidget(poc_box)

        f = QFrame()
        f.setLayout(main_box)
        self.setCentralWidget(f)


if __name__ == '__main__':
  
    app = QApplication(sys.argv)
    app_win = Spikely()
    app_win.show()
    sys.exit(app.exec_())
