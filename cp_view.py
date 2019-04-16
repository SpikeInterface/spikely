"""The view-control widget for constructing the active pipeline.

The Construct Pipeline view/control consists of widgets responsible for
constructing the active pipeline by inserting, deleting, or moving elements
within the active pipeline.
"""

import sys
import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg
import PyQt5.QtCore as qc

from pi_model import SpikePipeline
from el_model import SpikeElement
import spikely_constants as sc


class ConstructPipelineView(qw.QGroupBox):
    """A QGroupBox of widgets enabling user to assemble the pipeline.

    No public methods other than constructor.  All other activites
    of object are triggered by user interaction with sub widgets.
    """

    def __init__(self, active_pipe):
        """Initialize parent and member variables, construct UI."""
        super().__init__("Construct Pipeline")

        # Like the cheese, the active pipeline stands alone
        self._active_pipe = active_pipe

        # Need this reference to retrieve elements from combo box
        self._ele_cbx = qw.QComboBox(self)

        self._pipe_view = qw.QListView(self)

        self._init_ui()

    def _init_ui(self):
        """Build composite UI for region.

        Region consists of Controllers for adding and maninpulating active
        pipeline elements and a View of the in-construction active pipeline.
        """
        # Lay out view from top to bottom of group box
        cp_layout = qw.QVBoxLayout()
        self.setLayout(cp_layout)

        # Selection: Lay out view-controllers in frame from left to right
        sel_layout = qw.QHBoxLayout()
        sel_frame = qw.QFrame()
        sel_frame.setLayout(sel_layout)

        stage_cbx = qw.QComboBox()
        stage_cbx.currentIndexChanged.connect(self._stage_cbx_changed)
        for stage in sc.STAGE_NAMES:
            stage_cbx.addItem(stage)
        sel_layout.addWidget(stage_cbx)

        # self._ele_cbx = qw.QComboBox()
        sel_layout.addWidget(self._ele_cbx)

        add_button = qw.QPushButton("Add Element")
        add_button.setToolTip("Push to add element to pipeline.")
        add_button.clicked.connect(self._add_element_clicked)
        sel_layout.addWidget(add_button)
        cp_layout.addWidget(sel_frame)

        # View for pipeline construction - interacts w/ pipeline model
        # self.pipe_view = qw.QListView(self)
        self._pipe_view.setModel(self._active_pipe)  # There be dragons here
        sel_mdl = self._pipe_view.selectionModel()
        sel_mdl.selectionChanged.connect(self._ele_selection_changed)
        cp_layout.addWidget(self._pipe_view)

        """This funky bit of code is an example of how a class method
        with a specific signature can be bound to an instance of that class
        using a type index, in this case QModelIndex"""
        # treeView.clicked[QModelIndex].connect(self.clicked)

        # Manipulation: Control buttons ordered left to right
        man_layout = qw.QHBoxLayout()
        man_frame = qw.QFrame()
        # man_frame.setEnabled(False)

        man_frame.setLayout(man_layout)

        mu_btn = qw.QPushButton("Move Up")
        mu_btn.clicked.connect(self._move_up_clicked)
        man_layout.addWidget(mu_btn)

        de_btn = qw.QPushButton("Delete")
        de_btn.clicked.connect(self._delete_clicked)
        man_layout.addWidget(de_btn)

        md_btn = qw.QPushButton("Move Down")
        md_btn.clicked.connect(self._move_down_clicked)
        man_layout.addWidget(md_btn)

        cp_layout.addWidget(man_frame)

    def _ele_selection_changed(selected, deselected):
        print("Selection changed.")

    def _stage_cbx_changed(self, stage_id):
        """Receiver for currentIndexChanged signal from stage cbox."""
        self._ele_cbx.clear()
        for element in SpikeElement.avail_elements(stage_id):
            self._ele_cbx.addItem(element.name(), element)

    def _add_element_clicked(self):
        """Receiver for Add Element button clicked signal."""
        self._active_pipe.add_element(self._ele_cbx.currentData())

    def _delete_clicked(self):
        sel_mdl = self._pipe_view.selectionModel()
        if not sel_mdl.hasSelection():
            msg_box = qw.QMessageBox(self.parent())
            msg_box.setIcon(qw.QMessageBox.Information)
            msg_box.setText("Nothing to delete.")
            msg_box.setInformativeText("But, you already knew that, right?")
            msg_box.setStandardButtons(qw.QMessageBox.Ok)
            msg_box.exec()
        else:
            index = sel_mdl.selectedIndexes()[0].row()
            self._active_pipe.delete(index)

    def _move_up_clicked(self):
        sel_mdl = self._pipe_view.selectionModel()
        if not sel_mdl.hasSelection():
            msg_box = qw.QMessageBox(self.parent())
            msg_box.setIcon(qw.QMessageBox.Information)
            msg_box.setText("Nothing to move.")
            msg_box.setInformativeText("Wouldn't your time be better"
                                       " spent doing something else?")
            msg_box.setStandardButtons(qw.QMessageBox.Ok)
            msg_box.exec()
        else:
            index = sel_mdl.selectedIndexes()[0].row()
            self._active_pipe.move_up(index)

    def _move_down_clicked(self):
            sel_mdl = self._pipe_view.selectionModel()
            if not sel_mdl.hasSelection():
                msg_box = qw.QMessageBox(self.parent())
                msg_box.setIcon(qw.QMessageBox.Information)
                msg_box.setText("Nothing to move.")
                msg_box.setInformativeText("Wouldn't your time be better"
                                           " spent doing something else?")
                msg_box.setStandardButtons(qw.QMessageBox.Ok)
                msg_box.exec()
            else:
                index = sel_mdl.selectedIndexes()[0].row()
                self._active_pipe.move_down(index)
