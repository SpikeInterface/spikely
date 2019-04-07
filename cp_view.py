"""Creates an MVC view-control for constructing the active pipeline model.

The Construct Pipeline view/control consists of widgets responsible for
constructing the active pipeline by inserting, deleting, or moving elements
within the active pipeline.
"""

import sys
import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg

from pi_model import SpikePipeline
# from el_factory.py import ElementFactory 

class ConstructPipelineView(qw.QGroupBox):
    """GroupBox of widgets capable of constructing active pipeline.

    No public methods other than constructor.  All other activites
    of object are triggered by user interaction with sub widgets.
    """

    pipe_stages = ["Extraction", "Pre-Processing", "Sorting", "Post-Processing"]

    def __init__(self, active_pipe):
        """Initialize parent and member variables, construct UI."""
        super().__init__("Construct Pipeline")
        self._active_pipe = active_pipe
        self._init_ui()

    def cbx_activated(self, index):
        """Responds to state changes in stage combo box."""
        print(self.pipe_stages[index])

    def _init_ui(self):
        """Build composite UI for region.
        
        consisting of Controllers for adding and maninpulating active pipeline elements and a View of the in-construction active pipeline.
        """
        # Lay out controllers and view from top to bottom of group box
        cp_layout = qw.QVBoxLayout()
        self.setLayout(cp_layout)

        # Selection: Lay out view-controllers in frame from left to right
        sel_layout = qw.QHBoxLayout()
        sel_frame = qw.QFrame()
        sel_frame.setLayout(sel_layout)

        stage_cbx = qw.QComboBox()
        stage_cbx.currentIndexChanged.connect(self.cbx_activated)
        for stage in self.pipe_stages:
            stage_cbx.addItem(stage)
        sel_layout.addWidget(stage_cbx)
        
        ele_cbx = qw.QComboBox()
        sel_layout.addWidget(ele_cbx)
        
        sel_layout.addWidget(qw.QPushButton("Add Element"))
        cp_layout.addWidget(sel_frame)

        # Display: Hierarchical (Tree) view of in-construction pipeline

        self.pipe_view = qw.QTreeWidget(self)
        self.pipe_view.setColumnCount(1)
        self.pipe_view.header().hide()
        
        # self.pipe_view.itemClicked.connect(self.clicked)
        # self.pipe_view.setItemsExpandable(False)

        for stage in self.pipe_stages:
            an_item = qw.QTreeWidgetItem(self.pipe_view)
            an_item.setText(0, stage + " Stage")
            an_item.setForeground(0,qg.QBrush(qg.QColor("gray")))
            an_item.setExpanded(True)
            # child = qw.QTreeWidgetItem()
            # child.setText(0, "Sample Element")
            # an_item.addChild(child)

        cp_layout.addWidget(self.pipe_view)

        # Manipulation: Control buttons ordered lef to right
        man_layout = qw.QHBoxLayout()
        man_frame = qw.QFrame()
        man_frame.setEnabled(False)
        man_frame.setLayout(man_layout)

        for lbl in ["Move Up", "Delete", "Move Down"] :
            btn = qw.QPushButton(lbl)
            man_layout.addWidget(btn)
        
        cp_layout.addWidget(man_frame)