""" UI for SpikeInterface to create and run extracellular data 
processing pipelines.

The application allows users to load an extracellular recording, run 
preprocessing on the recording, run an installed spike sorter, and 
then run postprocessing on the results. All results are saved into a folder.

Loosely based on a hierarchical MVC design pattern, the application is
divided into modules corresponding to the functional screen regions
(the views) and the major data structures (the models)

Modules:
    spikely.py - Main application module
    op_view.py - Operate Pipeline UI region
    cp_view.py - Construct Pipeline UI region 
    pe_view.py - Configure Element UI region 
    pi_model.py - Pipeline Model: multi-stage element execution list
    el_model.py - Element Model: SpikeInterface component wrappers
    qu_model.py - Queue Model: pipeline execution list
"""

import sys

import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg

from op_view import OperatePipelineView
from pi_model import SpikePipeline


__version__ = "0.1.5"

class SpikelyMainWindow(qw.QMainWindow):
    """ Main window of application.

    No public methods other than constructor.
    """

    def __init__(self):
        super().__init__()
        sys.stdout.flush()
        self.spike_pipe = SpikePipeline()
        self._init_ui()


    def _init_ui(self):

        self.setWindowTitle("Spikely")
        self.setGeometry(100, 100, 800, 400)
        self.setWindowIcon(qg.QIcon("spikely.png"))
        self.statusBar().addPermanentWidget(
            qw.QLabel("Version " + __version__))

        self.pipe_tree = qw.QTreeWidget(self)
        self.pipe_tree.setColumnCount(1)
        self.pipe_tree.header().hide()
        # self.pipe_tree.itemClicked.connect(self.clicked)
        # self.pipe_tree.setItemsExpandable(False)

        stagelist = [
            "Stage 1: Extraction", 
            "Stage 2: Pre-Processing",
            "Stage 3: Sorting", 
            "Stage 4: Post-Processing"
        ]
        
        for stage in stagelist:
            an_item = qw.QTreeWidgetItem(self.pipe_tree)
            an_item.setText(0, stage)
            an_item.setForeground(0,qg.QBrush(qg.QColor("gray")))
            an_item.setExpanded(True)
            child = qw.QTreeWidgetItem()
            child.setText(0, "Sample Element")
            an_item.addChild(child)
          

        # Pipeline element commands
        self.up_btn, self.delete_btn, self.down_btn = (qw.QPushButton("Move Up"),
            qw.QPushButton("Delete"), qw.QPushButton("Move Down"))
        pec_box = qw.QFrame()
        hbox = qw.QHBoxLayout()
        hbox.addWidget(self.up_btn)
        hbox.addWidget(self.delete_btn)
        hbox.addWidget(self.down_btn)
        pec_box.setLayout(hbox)

        # Add pipeline elements
        stage_cbx = qw.QComboBox()
        stage_cbx.addItem("Recording")
        stage_cbx.addItem("Pre-Process")
        stage_cbx.addItem("Sorters")
        stage_cbx.addItem("Post-Process")

        ele_cbx = qw.QComboBox()
        ele_cbx.addItem("Element #1")
        ele_cbx.addItem("Element #2")
        ele_cbx.addItem("Element #3")

        ele_box = qw.QFrame()
        hbox = qw.QHBoxLayout()
        hbox.addWidget(stage_cbx)
        hbox.addWidget(ele_cbx)
        hbox.addWidget(qw.QPushButton("Add Element"))
        ele_box.setLayout(hbox)

        # Combine pipeline tree and element commands
        pipe_box = qw.QGroupBox("Construct Pipeline")
        vbox = qw.QVBoxLayout()
        vbox.addWidget(ele_box)
        vbox.addWidget(self.pipe_tree)
        vbox.addWidget(pec_box)
        pipe_box.setLayout(vbox)


        # Element Properties
        prop_tbl = qw.QTableWidget()
        prop_tbl.setRowCount(10)
        prop_tbl.setColumnCount(2)
        prop_tbl.setHorizontalHeaderLabels(("Property", "Value"))
        prop_tbl.setColumnWidth(0, 200)
        prop_tbl.setColumnWidth(1, 100)
        prop_tbl.verticalHeader().hide()
        prop_tbl.horizontalHeader().setSectionResizeMode(1, qw.QHeaderView.Stretch)

        prop_box = qw.QGroupBox("Configure Elements") 
        hbox = qw.QHBoxLayout()
        hbox.addWidget(prop_tbl)
        prop_box.setLayout(hbox)

        ele_frame = qw.QFrame()
        hbox = qw.QHBoxLayout()
        hbox.addWidget(pipe_box)
        hbox.addWidget(prop_box)
        ele_frame.setLayout(hbox)

        # Layout of main window
        main_box = qw.QVBoxLayout()
        main_box.addStretch(1)
        main_box.addWidget(ele_frame)
        main_box.addWidget(OperatePipelineView(self.spike_pipe))

        f = qw.QFrame()
        f.setLayout(main_box)
        self.setCentralWidget(f)


if __name__ == '__main__':
  
    app = qw.QApplication(sys.argv)
    app_win = SpikelyMainWindow()
    app_win.show()
    sys.exit(app.exec_())
