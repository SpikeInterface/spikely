"""Creates an MVC view-control for operations on the active pipeline model.

The Operate Pipeline view/control consists of widgets responsible for
user control over the SpikeInterface pipeline of elements used for
extracellular data processing.  Those operations include running, clearing,
and queueing the active pipeline.
"""

import PyQt5.QtWidgets as qw
import spikely_core as sc


class OperatePipelineView(qw.QGroupBox):
    """GroupBox of widgets capable of operating the active pipeline.

    Invokes methods on the active pipeline. No public methods other than
    constructor.  All other activites of object are triggered by user
    interaction with sub widgets.
    """

    def __init__(self, active_pipe):
        """Initialize parent, set object members, construct UI."""
        super().__init__("Operate Pipeline")  # Applies group box label
        self._active_pipe = active_pipe
        self._init_ui()

    def _init_ui(self):
        hbox = qw.QHBoxLayout()
        self.setLayout(hbox)

        # Pipeline operation commands
        run_btn = qw.QPushButton("Run")
        run_btn.clicked.connect(self._active_pipe.run)
        hbox.addWidget(run_btn)

        clear_btn = qw.QPushButton("Clear")
        clear_btn.clicked.connect(self._active_pipe.clear)
        hbox.addWidget(clear_btn)

        queue_btn = qw.QPushButton("Queue")
        queue_btn.clicked.connect(self._queue_btn_clicked)
        hbox.addWidget(queue_btn)

    def _queue_btn_clicked(self):
        sc.spikely_msg_box(self.parent(), "Feature not implemented",
                           "...not to say that it is not top of mind.")
