"""Creates an MVC view-control for configuring piepline element properties.

The Configure Element view/control consists of widgets responsible for
viewing and editing the properties of elements (extractors, sorters, etc.).
"""

import PyQt5.QtWidgets as qw

from el_model import SpikeElementModel


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

    def __init__(self, spike_pipe):
        """Initialize parent, set object members, build UI region."""
        super().__init__("Configure Elements")
        self.spike_pipe = spike_pipe
        self._ele_model = SpikeElementModel()

        self._init_ui()

    def _init_ui(self):
        """Build composite UI for element property configuration."""
        ce_layout = qw.QHBoxLayout()
        self.setLayout(ce_layout)

        cfg_table = qw.QTableView(self)
        cfg_table.setModel(self._ele_model)

        self.spike_pipe.ele_model = self._ele_model

        cfg_table.verticalHeader().hide()
        cfg_table.setColumnWidth(0, 200)
        cfg_table.setColumnWidth(1, 200)
        cfg_table.horizontalHeader().setSectionResizeMode(
            1, qw.QHeaderView.Stretch)

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

        ce_layout.addWidget(cfg_table)
