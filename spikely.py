""" UI for SpikeInterface to create and run extracellular data 
processing pipelines.

The application allows users to load an extracellular recording, run 
preprocessing on the recording, run an installed spike sorter, and 
then run postprocessing on the results. All results are saved into a folder.
"""

import sys

import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

from op_view import OperatePipelineView

__version__ = "0.1.5"

class SpikelyMainWindow(qtw.QMainWindow):
    """ Main window of application.

    No public methods other than constructor.
    """

    def __init__(self):
        super().__init__()
        self._init_ui()


    def _init_ui(self):

        self.setWindowTitle("Spikely")
        self.setGeometry(100, 100, 800, 400)
        self.setWindowIcon(qtg.QIcon("spikely.png"))
        self.statusBar().addPermanentWidget(
            qtw.QLabel("Version " + __version__))

        self.pipe_tree = qtw.QTreeWidget(self)
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
            an_item = qtw.QTreeWidgetItem(self.pipe_tree)
            an_item.setText(0, stage)
            an_item.setForeground(0,qtg.QBrush(qtg.QColor("gray")))
            an_item.setExpanded(True)
            child = qtw.QTreeWidgetItem()
            child.setText(0, "Sample Element")
            an_item.addChild(child)
          

        # Pipeline element commands
        self.up_btn, self.delete_btn, self.down_btn = (qtw.QPushButton("Move Up"),
            qtw.QPushButton("Delete"), qtw.QPushButton("Move Down"))
        pec_box = qtw.QFrame()
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.up_btn)
        hbox.addWidget(self.delete_btn)
        hbox.addWidget(self.down_btn)
        pec_box.setLayout(hbox)

        # Add pipeline elements
        stage_cbx = qtw.QComboBox()
        stage_cbx.addItem("Recording")
        stage_cbx.addItem("Pre-Process")
        stage_cbx.addItem("Sorters")
        stage_cbx.addItem("Post-Process")

        ele_cbx = qtw.QComboBox()
        ele_cbx.addItem("Element #1")
        ele_cbx.addItem("Element #2")
        ele_cbx.addItem("Element #3")

        ele_box = qtw.QFrame()
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(stage_cbx)
        hbox.addWidget(ele_cbx)
        hbox.addWidget(qtw.QPushButton("Add Element"))
        ele_box.setLayout(hbox)

        # Combine pipeline tree and element commands
        pipe_box = qtw.QGroupBox("Construct Pipeline")
        vbox = qtw.QVBoxLayout()
        vbox.addWidget(ele_box)
        vbox.addWidget(self.pipe_tree)
        vbox.addWidget(pec_box)
        pipe_box.setLayout(vbox)


        # Element Properties
        prop_tbl = qtw.QTableWidget()
        prop_tbl.setRowCount(10)
        prop_tbl.setColumnCount(2)
        prop_tbl.setHorizontalHeaderLabels(("Property", "Value"))
        prop_tbl.setColumnWidth(0, 200)
        prop_tbl.setColumnWidth(1, 100)
        prop_tbl.verticalHeader().hide()
        prop_tbl.horizontalHeader().setSectionResizeMode(1, qtw.QHeaderView.Stretch)

        prop_box = qtw.QGroupBox("Configure Elements") 
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(prop_tbl)
        prop_box.setLayout(hbox)

        ele_frame = qtw.QFrame()
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(pipe_box)
        hbox.addWidget(prop_box)
        ele_frame.setLayout(hbox)

        # Layout of main window
        main_box = qtw.QVBoxLayout()
        main_box.addStretch(1)
        main_box.addWidget(ele_frame)
        main_box.addWidget(OperatePipelineView())

        f = qtw.QFrame()
        f.setLayout(main_box)
        self.setCentralWidget(f)


if __name__ == '__main__':
  
    app = qtw.QApplication(sys.argv)
    app_win = SpikelyMainWindow()
    app_win.show()
    sys.exit(app.exec_())
