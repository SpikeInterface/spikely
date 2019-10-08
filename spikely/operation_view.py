# Implements MVC view associated with pipeline operations (run,clear, queue)

from PyQt5 import QtWidgets
from . import config


class OperationView(QtWidgets.QGroupBox):

    def __init__(self, pipeline_model, parameter_model):
        super().__init__("Command Pipeline")  # Group box label
        self._pipeline_model = pipeline_model
        self._parameter_model = parameter_model

        self._init_ui()

    def _init_ui(self):

        # Disable/Enable command buttons on empty/non-empty pipeline state
        self._pipeline_model.rowsInserted.connect(self._pipeline_changed)
        self._pipeline_model.rowsRemoved.connect(self._pipeline_changed)
        self._pipeline_model.modelReset.connect(self._pipeline_changed)

        self.setLayout(QtWidgets.QHBoxLayout())

        self._run_btn = QtWidgets.QPushButton("Run")
        self._run_btn.setStatusTip('Command the pipeline to run - executes '
            'from top to bottom')  # noqa: E128
        self._run_btn.setEnabled(False)
        self._run_btn.clicked.connect(self._pipeline_model.run)
        self.layout().addWidget(self._run_btn)

        self._clear_btn = QtWidgets.QPushButton("Clear")
        self._clear_btn.setStatusTip('Command the pipeline to clear - '
            'removes all elements')  # noqa: E128
        self._clear_btn.setEnabled(False)
        self._clear_btn.clicked.connect(self._pipeline_model.clear)
        self.layout().addWidget(self._clear_btn)

        self._queue_btn = QtWidgets.QPushButton("Queue")
        self._queue_btn.setStatusTip('Adds pipeline to queue for '
            'batch processing - not implemented')  # noqa: E128
        self._queue_btn.clicked.connect(self._queue_clicked)
        self.layout().addWidget(self._queue_btn)
        self._queue_btn.setEnabled(False)

    def _queue_clicked(self):
        config.find_main_window().statusBar().showMessage(
            "Queue not implemented", config.STATUS_MSG_TIMEOUT)

    def _pipeline_changed(self, parent=None, first=None, last=None):
        enabled = self._pipeline_model.rowCount(None) > 0
        self._run_btn.setEnabled(enabled)
        self._clear_btn.setEnabled(enabled)
        # self._queue_btn.setEnabled(enabled)
