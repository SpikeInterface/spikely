"""Creates an MVC view-control for operations on the active pipeline model.

The Operate Pipeline view/control consists of widgets responsible for
user control over the SpikeInterface pipeline of elements used for
extracellular data processing.  Those operations include running, clearing,
and queueing the active pipeline.
"""

import PyQt5.QtWidgets as qw
from . import config as cfg


class OperatePipelineView(qw.QGroupBox):
    """GroupBox of widgets capable of operating the active pipeline.

    Invokes methods on the active pipeline. No public methods other than
    constructor.  All other activites of object are triggered by user
    interaction with sub widgets.
    """

    def __init__(self, pipeline_model, element_model):
        """Initialize parent, set object members, construct UI."""
        super().__init__("Operate Pipeline")  # Applies group box label
        self._pipeline_model = pipeline_model
        self._element_model = element_model

        self._init_ui()

    def _init_ui(self):

        '''
        self._pipeline_model.rowsInserted.connect(self._pipeline_changed)
        self._pipeline_model.rowsRemoved.connect(self._pipeline_changed)
        self._pipeline_model.modelReset.connect(self._pipeline_changed)
        '''

        self.setLayout(qw.QHBoxLayout())

        # Pipeline operation commands
        self._run_btn = qw.QPushButton("Run")
        # self._run_btn.setEnabled(False)
        self._run_btn.clicked.connect(self._run_clicked)
        self.layout().addWidget(self._run_btn)

        self._clear_btn = qw.QPushButton("Clear")
        # self._clear_btn.setEnabled(False)
        self.layout().addWidget(self._clear_btn)

        def clear_clicked():
            self._pipeline_model.clear()
            # Should element model be responsible for this?
            self._element_model.element = None
        self._clear_btn.clicked.connect(clear_clicked)

        self._queue_btn = qw.QPushButton("Queue")
        self._queue_btn.clicked.connect(self._queue_clicked)
        self.layout().addWidget(self._queue_btn)

    def _queue_clicked(self):
        # Pipeline model should be responsible for this
        cfg.status_bar.showMessage(
            "Queue not implemented", cfg.STATUS_MSG_TIMEOUT)

    def _run_clicked(self):
        # Pipeline model should be responsible for this
        self._pipeline_model.run()

    '''
    def _pipeline_changed(self, parent=None, first=None, last=None):
        enabled = self._pipeline_model.rowCount(None) > 0
        self._run_btn.setEnabled(enabled)
        self._clear_btn.setEnabled(enabled)
        self._queue_btn.setEnabled(enabled)
    '''
