"""Creates an MVC view-control for operations on the active pipeline model.

The Operate Pipeline view/control consists of widgets responsible for
user control over the SpikeInterface pipeline of elements used for
extracellular data processing.  Those operations include running, clearing,
and queueing the active pipeline.
"""

import PyQt5.QtWidgets as qw
import config


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
        hbox = qw.QHBoxLayout()
        self.setLayout(hbox)

        # Pipeline operation commands
        run_btn = qw.QPushButton("Run")
        run_btn.clicked.connect(self._run_btn_clicked)
        hbox.addWidget(run_btn)

        clear_btn = qw.QPushButton("Clear")
        hbox.addWidget(clear_btn)

        def clear_clicked():
            self._pipeline_model.clear()
            self._element_model.element = None
        clear_btn.clicked.connect(clear_clicked)

        queue_btn = qw.QPushButton("Queue")
        queue_btn.clicked.connect(self._queue_btn_clicked)
        hbox.addWidget(queue_btn)

    def _queue_btn_clicked(self):
        config.status_bar.showMessage("Queue not implemented", config.TIMEOUT)

    def _run_btn_clicked(self):
        config.status_bar.showMessage("Run not implemented", config.TIMEOUT)
