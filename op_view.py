""" Creates an MVC view-control for operations on the active pipeline model.

The Operate Pipeline view/control consists of widgets responsible for
user control over the SpikeInterface pipeline of elements used for
extracellular data processing.  Those operations include running, clearing,
and queueing the active pipeline.
"""

import sys
import PyQt5.QtWidgets as qw
from pi_model import SpikePipeline  # The model for this controller

class OperatePipelineView(qw.QGroupBox):
    """GroupBox of widgets capable of controlling active pipeline.

    No public methods other than constructor.  All other activites
    of object are triggered by user interaction with sub widgets.
    """

    def __init__(self, spike_pipe):
        super().__init__("Operate Pipeline") # Labels group box parent
        self.spike_pipe = spike_pipe
        self._init_ui()


    def _init_ui(self):   
        
        hbox = qw.QHBoxLayout()
        self.setLayout(hbox)

        # Pipeline operation commands
        run_btn = qw.QPushButton("Run")
        run_btn.clicked.connect(self.spike_pipe.run)
        hbox.addWidget(run_btn)

        clear_btn = qw.QPushButton("Clear")
        clear_btn.clicked.connect(self.spike_pipe.clear)
        hbox.addWidget(clear_btn)

        queue_btn = qw.QPushButton("Queue")
        queue_btn.clicked.connect(lambda : print("Queue not implemented."))
        hbox.addWidget(queue_btn)