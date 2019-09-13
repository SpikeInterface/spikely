import sys
import pkg_resources

import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg

from spikely.operation_view import OperationView
from spikely.pipeline_view import PipelineView
from spikely.pipeline_model import PipelineModel
from spikely.parameter_view import ParameterView
from spikely.parameter_model import ParameterModel
from spikely import file_menu
from spikely import config as cfg

from spikely.version import __version__


class SpikelyMainWindow(qw.QMainWindow):

    def __init__(self):

        super().__init__()

        # Active pipeline and element parameter models
        self._parameter_model = ParameterModel()
        self._pipeline_model = PipelineModel(
            self._parameter_model)

        # Enhances print() use for debug
        sys.stdout.flush()

        self._init_ui()

    def _init_ui(self):

        self.setWindowTitle("spikely")
        self.setGeometry(100, 100, 1152, 448)

        spikely_png_path = pkg_resources.resource_filename(
            'spikely.resources', 'spikely.png')

        self.setWindowIcon(qg.QIcon(spikely_png_path))
        self.statusBar().addPermanentWidget(
            qw.QLabel("Version " + __version__))

        menu_bar = self.menuBar()
        menu = file_menu.create_file_menu(self, self._pipeline_model)
        menu_bar.addMenu(menu)

        main_frame = qw.QFrame()
        self.setCentralWidget(main_frame)
        main_frame.setLayout(qw.QVBoxLayout())

        pipe_param_splitter = qw.QSplitter()
        pipe_param_splitter.setChildrenCollapsible(False)

        # Actual widget construction done in View classes
        pipe_param_splitter.addWidget(PipelineView(
            self._pipeline_model, self._parameter_model))
        pipe_param_splitter.addWidget(ParameterView(
            self._pipeline_model, self._parameter_model))
        pipe_param_splitter.setSizes([328, 640])
        main_frame.layout().addWidget(pipe_param_splitter)

        main_frame.layout().addWidget(OperationView(
            self._pipeline_model, self._parameter_model))

        main_frame.layout().addStretch(1)  # Pushes app window widgets up


def launch_spikely():
    app = qw.QApplication(sys.argv)
    cfg.main_window = SpikelyMainWindow()
    cfg.status_bar = cfg.main_window.statusBar()
    cfg.main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    launch_spikely()
