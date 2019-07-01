"""Creates an MVC view-control for configuring pipeline element properties.

The Configure Element view/control consists of widgets responsible for
viewing and editing the properties of elements (extractors, sorters, etc.).
"""

import PyQt5.QtWidgets as qw

from .config import PARAM_COL, VTYPE_COL, VALUE_COL


class ConfigureElementView(qw.QGroupBox):
    """GroupBox of widgets capable of editing element properties.

    Application instance of element model is updated everytime user selects an
    element in the pipeline view.  In turn, this view keys off of those
    element model changes to display properties associated with user selected
    element.
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

        # Key to refreshing widget contents
        cfg_table.setModel(self._element_model)

        cfg_table.verticalHeader().hide()
        cfg_table.setColumnWidth(PARAM_COL, 200)
        cfg_table.setColumnWidth(VTYPE_COL, 100)
        cfg_table.setColumnWidth(VALUE_COL, 200)
        cfg_table.horizontalHeader().setStretchLastSection(True)

        """
        cfg_table.horizontalHeader().setSectionResizeMode(
            1, qw.QHeaderView.Stretch)
        """

        self.layout().addWidget(cfg_table)
