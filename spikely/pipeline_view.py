"""The view-control widget set for constructing the active pipeline.

The Construct Pipeline view-control consists of widgets responsible for
constructing the active pipeline by adding, deleting, or moving elements
within the active pipeline.
"""

import PyQt5.QtWidgets as qw

import spikely as sly
import spikeextractors as se
import spiketoolkit as st
import spikesorters as ss

from spikely import config as cfg
from spikely.spike_element import SpikeElement2


class PipelineView(qw.QGroupBox):
    """QGroupBox containing the view-control widget set

    No public methods other than constructor.  All other activites
    of object are triggered by user interaction with sub widgets.
    """

    def __init__(self, pipeline_model, parameter_model):
        super().__init__("Construct Pipeline")

        self._available_elements = []
        self._get_available_elements()

        self._pipeline_model = pipeline_model
        self._pipeline_view = qw.QListView(self)
        self._parameter_model = parameter_model

        self._init_ui()

    def _init_ui(self):
        """Assembles the individual widgets into the widget-set.

        The PipelineView consists of three separate UI assemblies
        stacked top to bottom: element selection, pipeline element list,
        and pipeline element commands (move up, delete, move down)
        """
        # Lay out view from top to bottom of group box
        self.setLayout(qw.QVBoxLayout())

        self.layout().addWidget(self._element_selection())
        self.layout().addWidget(self._pipeline_list())
        self.layout().addWidget(self._pipeline_commands())

    def _element_selection(self):
        """Select for and insert elements into pipeline."""

        ui_frame = qw.QFrame()
        ui_frame.setLayout(qw.QHBoxLayout())

        # Out of order declaration needed as forward reference
        ele_cbx = qw.QComboBox(self)

        stage_cbx = qw.QComboBox()
        ui_frame.layout().addWidget(stage_cbx)

        # Change ele_cbx contents when user makes stage_cbx selection
        def _stage_cbx_changed(index):

            ele_cbx.clear()

            element_cls = stage_cbx.itemData(index)
            for spif_cls in element_cls.get_installed_spif_classes():
                ele_cbx.addItem(spif_cls.__name__, spif_cls)
        stage_cbx.currentIndexChanged.connect(_stage_cbx_changed)

        # Must come after currentIndexChanged.connect to invoke callback
        for cls in SpikeElement2.__subclasses__():
            stage_cbx.addItem(cls.__name__ + 's', cls)

        # Layout after stage_cbx, but declared first as fwd reference
        ui_frame.layout().addWidget(ele_cbx)

        add_button = qw.QPushButton("Add Element")

        def _add_element_clicked():
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

        # Links element (parameter_view) and pipeline (pipeline_view) views
        def list_selection_changed(selected, deselected):
            if selected.indexes():
                # Retrieve selected element from pipeline model
                element = self._get_selected_element()
                # Link selected element to element property editor
                self._parameter_model.element = element
            else:
                self._parameter_model.element = None
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
                qw.QApplication.activeWindow().statusBar().showMessage(
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
                qw.QApplication.activeWindow().statusBar().showMessage(
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
                qw.QApplication.activeWindow().statusBar().showMessage(
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
                sly.Extractor(extractor_class, cfg.EXTRACTOR))

        preprocessor_list = st.preprocessing.preprocessinglist. \
            installed_preprocessers_list
        for preprocessor_class in preprocessor_list:
            self._available_elements.append(
                sly.Preprocessor(preprocessor_class, cfg.PRE_PROCESSOR)
            )

        sorter_list = ss.installed_sorter_list
        for sorter_class in sorter_list:
            self._available_elements.append(
                sly.Sorter(sorter_class, cfg.SORTER)
            )

        curator_list = st.curation.installed_curation_list
        for curator_class in curator_list:
            self._available_elements.append(
                sly.Curator(curator_class, cfg.CURATOR)
            )

        for exporter_class in sly.exporters_list:
            self._available_elements.append(
                sly.Exporter(exporter_class, cfg.EXPORTER)
            )
