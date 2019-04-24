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

    def __init__(self, pipeline_model, element_model):
        super().__init__("Construct Pipeline")

        # Underlying MVC model for this view set
        self._pipeline_model = pipeline_model
        self._element_model = element_model

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

        cpv_layout.addWidget(self._selection_widget())
        cpv_layout.addWidget(self._pipeline_widget())
        cpv_layout.addWidget(self._pipe_ops_widget())

        """This funky bit of code is an example of how a class method
        with a specific signature can be bound to an instance of that class
        using a type index, in this case QModelIndex"""
        # treeView.clicked[QModelIndex].connect(self.clicked)

    def _selection_widget(self):
        """Construct the QFrame holding the element selection widgets"""

        ele_cbx = qw.QComboBox(self)

        sel_frame = qw.QFrame()
        sel_frame.setLayout(qw.QHBoxLayout())

        stage_cbx = qw.QComboBox()
        sel_frame.layout().addWidget(stage_cbx)

        # Change list of available elements based on user selected stage
        def stage_cbx_changed(cbx_index):
            ele_cbx.clear()
            for element in SpikeElement.avail_elements():
                if element.stage_id == cbx_index:
                    ele_cbx.addItem(element.name, element)
        stage_cbx.currentIndexChanged.connect(stage_cbx_changed)
        stage_cbx.addItems(sc.STAGE_NAMES)

        # self._ele_cbx = qw.QComboBox()
        sel_frame.layout().addWidget(ele_cbx)

        add_button = qw.QPushButton("Add Element")

        def _add_element_clicked():
            self._pipeline_model.add_element(ele_cbx.currentData())
        add_button.clicked.connect(_add_element_clicked)

        sel_frame.layout().addWidget(add_button)

        return sel_frame

    def _pipeline_widget(self):
        self.pipe_view = qw.QListView(self)
        self.pipe_view.setModel(self._pipeline_model)
        self.pipe_view.setSelectionMode(
            qw.QAbstractItemView.SingleSelection)

        def ele_selection_changed(selected, deselected):
            if len(selected.indexes()) > 0:
                element = (self._pipeline_model.data(
                    selected.indexes()[0], sc.ELEMENT_ROLE))
                self._element_model.element = element
            else:
                self._element_model.element = None

        self.pipe_view.selectionModel().selectionChanged.connect(
            ele_selection_changed)

        return self.pipe_view

    def _pipe_ops_widget(self):
        man_frame = qw.QFrame()
        man_frame.setLayout(qw.QHBoxLayout())

        mu_btn = qw.QPushButton("Move Up")
        man_frame.layout().addWidget(mu_btn)

        def move_up_clicked():
            if self._element_model.element is None:
                sc.spikely_msg_box(self.parent(), "Nothing to move up.")
            else:
                self._pipeline_model.move_up(
                    self._element_model.element)
                index = self.pipe_view.currentIndex()
                index = self.pipe_view.model().index(index.row() - 1, 0)
                self.pipe_view.setCurrentIndex(index)
                # self.pipe_view.clearSelection()
        mu_btn.clicked.connect(move_up_clicked)

        return man_frame


"""

        de_btn = qw.QPushButton("Delete")
        de_btn.setProperty("pipe_view_sm", self._pipe_view.selectionModel())
        man_frame.layout().addWidget(de_btn)
        de_btn.clicked.connect(self._delete_clicked)

        md_btn = qw.QPushButton("Move Down")
        man_frame.layout().addWidget(md_btn)
        md_btn.clicked.connect(self._move_down_clicked)

    def _delete_clicked(self):
        # sel_mdl = self._pipe_view.selectionModel()
        sel_mdl = self.sender().property("pipe_view_sm")
        if not sel_mdl.hasSelection():
            sc.spikely_msg_box(self.parent(), "Nothing to delete.",
                               "But, you already knew that, right?")
        else:
            index = sel_mdl.selectedIndexes()[0].row()
            self._active_pipeline.delete(index)

    def _move_down_clicked(self):
        sel_mdl = self._pipe_view.selectionModel()
        if not sel_mdl.hasSelection():
            sc.spikely_msg_box(self.parent(), "Nothing to move down.",
                               "But, you already knew that, right?")
        else:
            index = sel_mdl.selectedIndexes()[0].row()
            self._active_pipeline.move_down(index)
"""
