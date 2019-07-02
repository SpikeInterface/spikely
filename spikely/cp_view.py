"""The view-control widget set for constructing the active pipeline.

The Construct Pipeline view-control consists of widgets responsible for
constructing the active pipeline by inserting, deleting, or moving elements
within the active pipeline.
"""

import PyQt5.QtWidgets as qw

from .extractor import Extractor
from .preprocessor import Preprocessor
from .sorter import Sorter
from .curator import Curator

from . import config as cfg

import spikeextractors as se
import spiketoolkit as st


class ConstructPipelineView(qw.QGroupBox):
    """QGroupBox containing the view-control widget set

    No public methods other than constructor.  All other activites
    of object are triggered by user interaction with sub widgets.
    """

    def __init__(self, pipeline_model, element_model):
        super().__init__("Construct Pipeline")

        self._available_elements = []
        self._get_available_elements()

        self._pipeline_model = pipeline_model
        self._pipeline_view = qw.QListView(self)
        self._element_model = element_model

        self._init_ui()

    def _init_ui(self):
        """Assembles the individual widgets into the widget-set.

        The ConstructPipelineView consists of three separate UI assemblies
        stacked top to bottom: element selection, pipeline element list view,
        and pipeline element manipulation controls (move up, delete, move down)
        """
        # Lay out view from top to bottom of group box
        self.setLayout(qw.QVBoxLayout())

        self.layout().addWidget(self._element_insertion())
        self.layout().addWidget(self._pipeline_list())
        self.layout().addWidget(self._pipeline_commands())

        """This funky bit of code is an example of how a class method
        with a specific signature can be bound to an instance of that class
        using a type index, in this case QModelIndex"""
        # treeView.clicked[QModelIndex].connect(self.clicked)

    def _element_insertion(self):
        """Select for and insert elements into pipeline."""

        ui_frame = qw.QFrame()
        ui_frame.setLayout(qw.QHBoxLayout())

        # Out of order declaration needed as forward reference
        ele_cbx = qw.QComboBox(self)

        """
        # Indicates user selection of combobox entry
        def _ele_cbx_activated(index):
            print('_ele_cbx activated')
        ele_cbx.activated.connect(_ele_cbx_activated)
        """

        stage_cbx = qw.QComboBox()
        ui_frame.layout().addWidget(stage_cbx)

        # Change ele_cbx contents when user makes stage_cbx selection
        def _stage_cbx_changed(index):
            ele_cbx.clear()
            for element in self._available_elements:
                # stage_cbx items store type ID associated w/ name
                if element.interface_id == stage_cbx.itemData(index):
                    # ele_cbx items store element object w/ name
                    ele_cbx.addItem(element.name, element)
        stage_cbx.currentIndexChanged.connect(_stage_cbx_changed)

        # Must come after currentIndexChanged.connect to invoke callback
        stage_cbx.addItem('Extractors', cfg.EXTRACTOR)
        stage_cbx.addItem('Pre-Processors', cfg.PRE_PROCESSOR)
        stage_cbx.addItem('Sorters', cfg.SORTER)
        stage_cbx.addItem('Curators', cfg.CURATOR)

        # Layout after stage_cbx, but declared first as fwd reference
        ui_frame.layout().addWidget(ele_cbx)

        add_button = qw.QPushButton("Add Element")

        def _add_element_clicked():
            # Prevents the addition of nu
            if ele_cbx.currentIndex() > -1:
                # Takes advantage of actual element reference stored in ele_cbx
                self._pipeline_model.add_element(ele_cbx.currentData())
        add_button.clicked.connect(_add_element_clicked)

        ui_frame.layout().addWidget(add_button)

        return ui_frame

    def _pipeline_list(self):
        # MVC in action - connect View (widget) to Model
        self._pipeline_view.setModel(self._pipeline_model)

        self._pipeline_view.setSelectionMode(
            qw.QAbstractItemView.SingleSelection)

        # Links element (ce_view) and pipeline (cp_view) views
        def list_selection_changed(selected, deselected):
            if selected.indexes():
                # Retrieve selected element from pipeline model
                element = self._get_selected_element()
                # Link selected element to element property editor
                self._element_model.element = element
            else:
                self._element_model.element = None
        self._pipeline_view.selectionModel().selectionChanged.connect(
            list_selection_changed)

        return self._pipeline_view

    def _pipeline_commands(self):
        ui_frame = qw.QFrame()
        ui_frame.setLayout(qw.QHBoxLayout())

        # Move Up element button and associated action
        mu_btn = qw.QPushButton("Move Up")
        ui_frame.layout().addWidget(mu_btn)

        def move_up_clicked():
            element = self._get_selected_element()
            if element is None:
                cfg.status_bar.showMessage(
                    "Nothing to move up", cfg.STATUS_MSG_TIMEOUT)
            else:
                self._pipeline_model.move_up(element)
        mu_btn.clicked.connect(move_up_clicked)

        # Move Down element button and associated action
        md_btn = qw.QPushButton("Move Down")
        ui_frame.layout().addWidget(md_btn)

        def move_down_clicked():
            element = self._get_selected_element()
            if element is None:
                cfg.status_bar.showMessage(
                    "Nothing to move down", cfg.STATUS_MSG_TIMEOUT)
            else:
                self._pipeline_model.move_down(element)
        md_btn.clicked.connect(move_down_clicked)

        # Delete element button and associated action
        de_btn = qw.QPushButton("Delete")
        ui_frame.layout().addWidget(de_btn)

        def delete_clicked():
            element = self._get_selected_element()
            if element is None:
                cfg.status_bar.showMessage(
                    "Nothing to delete", cfg.STATUS_MSG_TIMEOUT)
            else:
                self._pipeline_model.delete(element)
        de_btn.clicked.connect(delete_clicked)

        return ui_frame

    def _get_selected_element(self):
        """ Convenience function to retrieve selected element in pipe view"""
        element = None
        model = self._pipeline_view.selectionModel()
        if model.hasSelection():
            index = model.selectedIndexes()[0]
            element = self._pipeline_model.data(index, cfg.ELEMENT_ROLE)
        return element

    def _get_available_elements(self):
        extractor_list = se.extractorlist.installed_recording_extractor_list
        for extractor_class in extractor_list:
            self._available_elements.append(
                Extractor(extractor_class, cfg.EXTRACTOR))

        preprocessor_list = st.preprocessing.preprocessinglist. \
            installed_preprocessers_list
        for preprocessor_class in preprocessor_list:
            self._available_elements.append(
                Preprocessor(preprocessor_class, cfg.PRE_PROCESSOR)
            )

        sorter_list = st.sorters.installed_sorter_list
        for sorter_class in sorter_list:
            self._available_elements.append(
                Sorter(sorter_class, cfg.SORTER)
            )

        curator_list = st.curation.installed_curation_list
        for curator_class in curator_list:
            self._available_elements.append(
                Curator(curator_class, cfg.CURATOR)
            )
