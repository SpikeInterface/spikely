import PyQt5.QtWidgets as qw
from . import config as cfg


# The collection of UI widgets assocated with pipeline operations
class OperationView(qw.QGroupBox):

    def __init__(self, pipeline_model, parameter_model):
        super().__init__("Operate Pipeline")  # Group box label
        self._pipeline_model = pipeline_model
        self._parameter_model = parameter_model

        self._init_ui()

    def _init_ui(self):

        # Removed pipeline state monitoring, but may want to put it back in
        # self._pipeline_model.rowsInserted.connect(self._pipeline_changed)
        # self._pipeline_model.rowsRemoved.connect(self._pipeline_changed)
        # self._pipeline_model.modelReset.connect(self._pipeline_changed)

        self.setLayout(qw.QHBoxLayout())

        self._run_btn = qw.QPushButton("Run")
        # self._run_btn.setEnabled(False)
        self._run_btn.clicked.connect(self._run_clicked)
        self.layout().addWidget(self._run_btn)

        self._clear_btn = qw.QPushButton("Clear")
        # self._clear_btn.setEnabled(False)
        self.layout().addWidget(self._clear_btn)

        def clear_clicked():
            self._pipeline_model.clear()
            # Ensures synchronization with parameter view
            self._parameter_model.element = None
        self._clear_btn.clicked.connect(clear_clicked)

        self._queue_btn = qw.QPushButton("Queue")
        self._queue_btn.clicked.connect(self._queue_clicked)
        self.layout().addWidget(self._queue_btn)
        # Disabled pending queue functionality
        self._queue_btn.setEnabled(False)
        self._queue_btn.setToolTip('Pipeline queueing not implemented.')

    def _queue_clicked(self):
        # Pipeline model should be responsible for this
        qw.QApplication.activeWindow().statusBar().showMessage(
            "Queue not implemented", cfg.STATUS_MSG_TIMEOUT)

    def _run_clicked(self):
        if self._pipeline_model.rowCount():
            self._pipeline_model.run()
        else:
            qw.QApplication.activeWindow().statusBar().showMessage(
                "Elements required before pipeline can be run.",
                cfg.STATUS_MSG_TIMEOUT)
    '''
    def _pipeline_changed(self, parent=None, first=None, last=None):
        enabled = self._pipeline_model.rowCount(None) > 0
        self._run_btn.setEnabled(enabled)
        self._clear_btn.setEnabled(enabled)
        self._queue_btn.setEnabled(enabled)
    '''
