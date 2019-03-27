""" Instantiates the Operate Pipeline application view.

The Operate Pipeline application view consists of widgets responsible for
user control over the SpikeInterface pipeline of elements used for
extracellular data processing.
"""

import sys

import PyQt5.QtWidgets as qtw

class OperatePipelineView(qtw.QGroupBox):
    """ Main window of application.

    No public methods other than constructor.
    """

    def __init__(self):
        super().__init__("Operate Pipeline")

        self._init_ui()


    def btn_clicked(self):
        print(self.sender().objectName())

    def _init_ui(self):   
        # Pipeline operation commands
        run_btn, queue_btn, clear_btn = (qtw.QPushButton("Run"),
            qtw.QPushButton("Queue"), qtw.QPushButton("Clear"))


        run_btn.setObjectName("Run")
        run_btn.clicked.connect(lambda : print(self.sender().objectName()))

        # print("Button name: " + run_btn.objectName())
        # run_btn.clicked.connect(self.btn_clicked)


        hbox = qtw.QHBoxLayout()
        hbox.addWidget(run_btn)
        hbox.addWidget(queue_btn)
        hbox.addWidget(clear_btn)
        self.setLayout(hbox)
