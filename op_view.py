""" Instantiates the Operate Pipeline application view.

The Operate Pipeline application view consists of widgets responsible for
user control over the SpikeInterface pipeline of elements used for
extracellular data processing.
"""

import sys
import PyQt5.QtWidgets as qw
from pi_model import SpikePipeline

class OperatePipelineView(qw.QGroupBox):
    """Collection of widgets tied to Operate Pipeline commands.

    No public methods other than constructor.
    """

    def __init__(self, spike_pipe):
        super().__init__("Operate Pipeline")
        self.spike_pipe = spike_pipe

        new_pipe = SpikePipeline()

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