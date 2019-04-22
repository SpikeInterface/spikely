"""The view-control widget set for constructing the active pipeline.

The Construct Pipeline view-control consists of widgets responsible for
constructing the active pipeline by inserting, deleting, or moving elements
within the active pipeline.
"""

import PyQt5.QtWidgets as qw

from el_model import SpikeElement
import spikely_core as sc


class ConstructPipelineView(qw.QGroupBox):
    """A QGroupBox containing widgets needed to construct pipeline.

    No public methods other than constructor.  All other activites
    of object are triggered by user interaction with sub widgets.
    """

    def __init__(self, active_pipe):
        super().__init__("Construct Pipeline")

        # Underlying MVC model for this view set
        self._active_pipe = active_pipe

        # Need this reference to retrieve elements from combo box
        self._ele_cbx = qw.QComboBox(self)

        self._pipe_view = qw.QListView(self)

        self._init_ui()

    def _init_ui(self):
        """Build composite UI for region.

        The ConstructPipelineView consists of three separate UI assemblies
        stacked top to bottom: element selection, pipeline element list view,
        and pipeline element manipulation controls (move up, delete, move down)
        """
        # Lay out view from top to bottom of group box
        cpv_layout = qw.QVBoxLayout()
        self.setLayout(cpv_layout)

        cpv_layout.addWidget(self._selection_frame())

        # View for pipeline construction - interacts w/ pipeline model
        # self.pipe_view = qw.QListView(self)
        self._pipe_view.setModel(self._active_pipe)  # There be dragons here
        self._pipe_view.selectionModel().selectionChanged.connect(
            self._ele_selection_changed)

        cpv_layout.addWidget(self._pipe_view)

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

        cpv_layout.addWidget(man_frame)

    def _selection_frame(self):
        """Construct the QFrame holding the element selection widgets"""
        sel_frame = qw.QFrame()
        sel_frame.setLayout(qw.QHBoxLayout())

        stage_cbx = qw.QComboBox()
        sel_frame.layout().addWidget(stage_cbx)

        # Change list of available elements based on user selected stage
        def _stage_cbx_changed(cbx_index):
            self._ele_cbx.clear()
            for element in SpikeElement.avail_elements():
                if element.stage_id == cbx_index:
                    self._ele_cbx.addItem(element.name, element)
        stage_cbx.currentIndexChanged.connect(_stage_cbx_changed)
        stage_cbx.addItems(sc.STAGE_NAMES)

        # self._ele_cbx = qw.QComboBox()
        sel_frame.layout().addWidget(self._ele_cbx)

        add_button = qw.QPushButton("Add Element")
        sel_frame.layout().addWidget(add_button)

        def _add_element_clicked():
            self._active_pipe.add_element(self._ele_cbx.currentData())
        add_button.clicked.connect(_add_element_clicked)

        return sel_frame

    def _ele_selection_changed(self, selected, deselected):
        # sel_indexes = selected.indexes()
        element = self._active_pipe.data(
            selected.indexes()[0], sc.ELEMENT_ROLE)
        self._active_pipe.ele_model.set_element(element)

    def _delete_clicked(self):
        sel_mdl = self._pipe_view.selectionModel()
        if not sel_mdl.hasSelection():
            sc.spikely_msg_box(self.parent(), "Nothing to delete.",
                               "But, you already knew that, right?")
        else:
            index = sel_mdl.selectedIndexes()[0].row()
            self._active_pipe.delete(index)

    def _move_up_clicked(self):
        sel_mdl = self._pipe_view.selectionModel()
        if not sel_mdl.hasSelection():
            sc.spikely_msg_box(self.parent(), "Nothing to move up.",
                               "But, you already knew that, right?")
        else:
            index = sel_mdl.selectedIndexes()[0].row()
            self._active_pipe.move_up(index)

    def _move_down_clicked(self):
        sel_mdl = self._pipe_view.selectionModel()
        if not sel_mdl.hasSelection():
            sc.spikely_msg_box(self.parent(), "Nothing to move down.",
                               "But, you already knew that, right?")
        else:
            index = sel_mdl.selectedIndexes()[0].row()
            self._active_pipe.move_down(index)
