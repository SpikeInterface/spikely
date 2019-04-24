"""Creates an MVC view-control for configuring piepline element properties.

The Configure Element view/control consists of widgets responsible for
viewing and editing the properties of elements (extractors, sorters, etc.).
"""

import PyQt5.QtWidgets as qw


class ConfigureElementView(qw.QGroupBox):
    """GroupBox of widgets capable of constructing active pipeline.

    No public methods other than constructor.  All other activites
    of object are triggered by user interaction with sub widgets.

    Keys off of changes to the active_element attribute in the pipeline
    which in turn is keyed off of user interactions with elements in the
    pipeline view.  User selects element in Pipeline View causing view
    to signal model to set Active Element to selection.  In turn, the
    pipeline model signals a change to Active Element that is received
    by the Configure Element view.
    """

    def __init__(self, pipeline_model, element_model):
        """Initialize parent, set object members, build UI region."""
        super().__init__("Configure Elements")
        self._pipeline_model = pipeline_model
        self._element_model = element_model

        self._init_ui()

    def _init_ui(self):
        """Build composite UI for element property configuration."""
        self.setLayout(qw.QHBoxLayout())

        cfg_table = qw.QTableView(self)
        cfg_table.setModel(self._element_model)

        cfg_table.verticalHeader().hide()
        cfg_table.setColumnWidth(0, 200)
        cfg_table.setColumnWidth(1, 200)
        cfg_table.horizontalHeader().setSectionResizeMode(
            1, qw.QHeaderView.Stretch)

        self.layout().addWidget(cfg_table)

        """
        cfg_table = qw.QTableWidget()
        # cfg_table.setSelectionBehavior(qw.QAbstractItemView.SelectRows)
        cfg_table.setRowCount(10)
        cfg_table.setColumnCount(2)
        cfg_table.setHorizontalHeaderLabels(("Property", "Value"))
        cfg_table.setColumnWidth(0, 200)
        cfg_table.setColumnWidth(1, 200)
        cfg_table.verticalHeader().hide()
        cfg_table.horizontalHeader().setSectionResizeMode(
            1, qw.QHeaderView.Stretch)
        """
