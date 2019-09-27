# The view-control widget set for constructing the active pipeline.

# The Construct Pipeline view-control consists of widgets responsible for
# constructing the active pipeline by adding, deleting, or moving elements
# within the active pipeline.

import PyQt5.QtWidgets as qw

from . import config
from .elements import spike_element as sp_spe


class PipelineView(qw.QGroupBox):
    # QGroupBox containing the view-control widget set

    # No public methods other than constructor.  All other object
    # behaviors are triggered by user interaction with sub widgets.

    def __init__(self, pipeline_model, parameter_model):
        super().__init__("Construct Pipeline")

        self._pipeline_model = pipeline_model
        self._pipeline_view = qw.QListView(self)
        self._parameter_model = parameter_model

        self._init_ui()

    def _init_ui(self):
        # Assembles the individual widgets into the widget-set.

        # The PipelineView consists of three separate UI assemblies
        # stacked top to bottom: element selection, pipeline element list,
        # and pipeline element commands (move up, delete, move down)

        # Lay out view from top to bottom of group box
        self.setLayout(qw.QVBoxLayout())

        self.layout().addWidget(self._element_selection())
        self.layout().addWidget(self._pipeline_list())
        self.layout().addWidget(self._pipeline_commands())

    def _element_selection(self):
        # UI to select for and add elements to pipeline.

        # The UI for element selection combines a combo box for the stages
        # (e.g., Extractor) and one for the corresponding SpikeInterface
        # classes (e.g., MEArecRecordingExtractor) - the two pieces of
        # information required to instantiate the SpikeElement inserted into
        # the pipeline.

        ui_frame = qw.QFrame()
        ui_frame.setLayout(qw.QHBoxLayout())

        # Out of order declaration needed as forward reference
        spif_cbx = qw.QComboBox(self)

        stage_cbx = qw.QComboBox()
        ui_frame.layout().addWidget(stage_cbx)

        # Change spif_cbx contents when user makes stage_cbx selection
        def _stage_cbx_changed(index):
            spif_cbx.clear()
            element_cls = stage_cbx.itemData(index)
            # SpikeElement subclasses tasked w/ generating spif class lists
            for spif_cls in element_cls.get_installed_spif_classes():
                spif_cbx.addItem(spif_cls.__name__, spif_cls)
        stage_cbx.currentIndexChanged.connect(_stage_cbx_changed)

        # Note: cbx instantiation order matters for initial m/v signalling

        # A subtle bit of introspection likely to come back and bite me
        for cls in sp_spe.SpikeElement.__subclasses__():
            stage_cbx.addItem(cls.__name__ + 's', cls)
        stage_cbx.model().sort(0)
        stage_cbx.setCurrentIndex(0)

        ui_frame.layout().addWidget(spif_cbx)

        add_button = qw.QPushButton("Add Element")

        def _add_element_clicked():
            if spif_cbx.currentIndex() > -1:
                # Classes stored as cbx user data enables object creation
                spif_class = spif_cbx.currentData()
                element_class = stage_cbx.currentData()
                element = element_class(spif_class)
                self._pipeline_model.add_element(element)
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
        # Operations applied to the pipeline as a whole (Run, Clear, Queue)
        ui_frame = qw.QFrame()
        ui_frame.setLayout(qw.QHBoxLayout())

        # Move Up element button and associated action
        mu_btn = qw.QPushButton("Move Up")
        ui_frame.layout().addWidget(mu_btn)

        def move_up_clicked():
            element = self._get_selected_element()
            if element is None:
                config.find_main_window().statusBar().showMessage(
                    "Nothing to move up", config.STATUS_MSG_TIMEOUT)
            else:
                self._pipeline_model.move_up(element)
        mu_btn.clicked.connect(move_up_clicked)

        # Move Down element button and associated action
        md_btn = qw.QPushButton("Move Down")
        ui_frame.layout().addWidget(md_btn)

        def move_down_clicked():
            element = self._get_selected_element()
            if element is None:
                config.find_main_window().statusBar().showMessage(
                    "Nothing to move down", config.STATUS_MSG_TIMEOUT)
            else:
                self._pipeline_model.move_down(element)
        md_btn.clicked.connect(move_down_clicked)

        # Delete element button and associated action
        de_btn = qw.QPushButton("Delete")
        ui_frame.layout().addWidget(de_btn)

        def delete_clicked():
            element = self._get_selected_element()
            if element is None:
                config.find_main_window().statusBar().showMessage(
                    "Nothing to delete", config.STATUS_MSG_TIMEOUT)
            else:
                self._pipeline_model.delete(element)
        de_btn.clicked.connect(delete_clicked)

        return ui_frame

    def _get_selected_element(self):
        # Convenience function to retrieve selected element in pipe view
        element = None
        model = self._pipeline_view.selectionModel()
        if model.hasSelection():
            index = model.selectedIndexes()[0]
            element = self._pipeline_model.data(index, config.ELEMENT_ROLE)
        return element
