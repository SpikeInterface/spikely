# The view-control widget set for constructing the active pipeline.

from PyQt5 import QtWidgets

from . import config
from .elements import spike_element as sp_spe
from .elements import std_element_policy as sp_ste


class PipelineView(QtWidgets.QGroupBox):

    def __init__(self, pipeline_model, parameter_model):
        super().__init__("Construct Pipeline")

        self._pipeline_model = pipeline_model
        self._pipeline_view = QtWidgets.QListView(self)
        self._parameter_model = parameter_model
        self._element_policy = sp_ste.StdElementPolicy()

        self._init_ui()

    def _init_ui(self):
        # Assembles the individual widgets into the widget-set.

        # The PipelineView consists of three separate UI assemblies
        # stacked top to bottom: element selection, pipeline element list,
        # and pipeline element commands (move up, delete, move down)

        # Lay out view from top to bottom of group box
        self.setLayout(QtWidgets.QVBoxLayout())

        self.layout().addWidget(self._element_selection())
        self.layout().addWidget(self._pipeline_list())
        self.layout().addWidget(self._pipeline_commands())

    def _element_selection(self):
        # UI to select for and add elements to pipeline.

        # The UI for element selection combines a combo box for the stages
        # (e.g., RecordingExtractor) and one for the corresponding
        # SpikeInterface classes (e.g., MEArecRecordingExtractor) - the two
        # pieces of information required to instantiate the SpikeElement
        # inserted into the pipeline.

        ui_frame = QtWidgets.QFrame()
        ui_frame.setLayout(QtWidgets.QHBoxLayout())

        # Out of order declaration needed as forward reference
        spif_cbx = QtWidgets.QComboBox(self)
        spif_cbx.setStatusTip('Choose an element to be added to the '
            'pipeline - listed for current element category')  # noqa: E128

        elem_cbx = QtWidgets.QComboBox()
        elem_cbx.setStatusTip('Choose an element category to list the '
            'specific elements available within that category')  # noqa: E128

        ui_frame.layout().addWidget(elem_cbx)

        # Change spif_cbx contents when user makes elem_cbx selection
        def _elem_cbx_changed(index):
            spif_cbx.clear()
            element_cls = elem_cbx.itemData(index)
            # SpikeElement subclasses tasked w/ generating spif class lists
            for spif_cls in element_cls.get_installed_spif_cls_list():
                spif_cbx.addItem(
                    element_cls.get_display_name_from_spif_class(
                        spif_cls), spif_cls)
        elem_cbx.currentIndexChanged.connect(_elem_cbx_changed)

        # Note: cbx instantiation order matters for initial m/v signalling

        # All elements are subclasses of SpikeElement, but element policy
        # determines which ones are available to the user
        elem_classes = [cls for cls in sp_spe.SpikeElement.__subclasses__()
                        if self._element_policy.is_cls_available(cls)]
        # Element (subclass) order is arbitrary, so sort by policy order
        elem_classes.sort(key=lambda e: self._element_policy.cls_order_dict[e])
        # Now that elements are sorted and filtered, set the combo box

        for cls in elem_classes:
            display_name = self._element_policy.get_cls_display_name(cls)
            elem_cbx.addItem(display_name + 's', cls)
        elem_cbx.setCurrentIndex(0)

        ui_frame.layout().addWidget(spif_cbx)

        add_button = QtWidgets.QPushButton("Add Element")
        add_button.setStatusTip('Add selected element to the pipeline - '
            'element will be inserted in category order')  # noqa: E128

        def _add_element_clicked():
            if spif_cbx.currentIndex() > -1:
                # Classes stored as cbx user data enables object creation
                spif_class = spif_cbx.currentData()
                element_class = elem_cbx.currentData()
                element = element_class(spif_class)
                self._pipeline_model.add_element(element)
        add_button.clicked.connect(_add_element_clicked)

        ui_frame.layout().addWidget(add_button)

        return ui_frame

    def _pipeline_list(self):
        # MVC in action - connect View (widget) to Model
        self._pipeline_view.setModel(self._pipeline_model)

        self._pipeline_view.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)

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
        ui_frame = QtWidgets.QFrame()
        ui_frame.setLayout(QtWidgets.QHBoxLayout())

        # Move Up element button and associated action
        mu_btn = QtWidgets.QPushButton("Move Up")
        mu_btn.setStatusTip('Move selected element up one step in the '
            'pipeline - cross element category moves barred')  # noqa: E128
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
        md_btn = QtWidgets.QPushButton("Move Down")
        md_btn.setStatusTip('Move selected element down one step in the '
            'pipeline - cross element category moves barred')  # noqa: E128
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
        de_btn = QtWidgets.QPushButton("Delete")
        de_btn.setStatusTip('Delete the selected element in the pipeline')
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
            element = self._pipeline_model.data(
                model.selectedIndexes()[0], config.ELEMENT_ROLE)
        return element
