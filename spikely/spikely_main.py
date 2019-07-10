"""UI for SpikeInterface extracellular data processing pipelines.

spikely enables a user to construct and execute a pipeline of elements
used extracellular data recording extraction, pre-processing, sorting, and
curation.

The code is organized along hierarchical MVC lines.  The pipeline, parameter,
and operation views represent the three primary regions of the UI, while the
element and pipeline models proxy for individual and collective SpikeInterface
objects respectively.

"""

import sys

import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg

from .operation_view import OperationView
from .pipeline_view import PipelineView
from .parameter_view import ParameterView
from .pipeline_model import PipelineModel
from .element_model import ElementModel

import pkg_resources

from . import config as cfg
from .version import __version__


class SpikelyMainWindow(qw.QMainWindow):
    """Main window for the application"""

    def __init__(self):

        super().__init__()

        # Active pipeline and element models
        self._element_model = ElementModel()
        self._pipeline_model = PipelineModel(
            self._element_model)

        # Enhances print() use for debug
        sys.stdout.flush()

        self._init_ui()

    def _init_ui(self):
        """Assembles the main UI from delegated sub-views."""

        # Application main window setup
        self.setWindowTitle("spikely")
        self.setGeometry(100, 100, 1152, 448)

        spikely_png_path = pkg_resources.resource_filename(
            'spikely.resources', 'spikely.png')

        self.setWindowIcon(qg.QIcon(spikely_png_path))
        self.statusBar().addPermanentWidget(
            qw.QLabel("Version " + __version__))

        # Menus
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')
        # tools_menu = main_menu.addMenu('Tools')

        exit_btn = qw.QAction('Exit', self)
        exit_btn.setShortcut('Ctrl+Q')
        exit_btn.setStatusTip('Exit application')
        exit_btn.triggered.connect(self.close)
        file_menu.addAction(exit_btn)

        # Core application UI in main_frame as CentralWidget of QMainWindow
        main_frame = qw.QFrame()
        self.setCentralWidget(main_frame)
        main_frame.setLayout(qw.QVBoxLayout())

        """ Lay out Construction Pipeline (cp) and Configure Element (ce)
        views in a frame at top of main window from left to right
        """
        cp_ce_splitter = qw.QSplitter()
        cp_ce_splitter.setChildrenCollapsible(False)

        # Actual widget construction done in View classes
        cp_ce_splitter.addWidget(PipelineView(
            self._pipeline_model, self._element_model))
        cp_ce_splitter.addWidget(ParameterView(
            self._pipeline_model, self._element_model))
        cp_ce_splitter.setSizes([328, 640])
        main_frame.layout().addWidget(cp_ce_splitter)

        # Lay out Operate Pipeline (op) view at bottom of main window
        main_frame.layout().addWidget(OperationView(
            self._pipeline_model, self._element_model))

        main_frame.layout().addStretch(1)  # Pushes app window widgets up

        # Allows any module to post a status message to main window
        # cfg.status_bar = self.statusBar()


def launch_spikely():
    app = qw.QApplication(sys.argv)
    cfg.main_window = SpikelyMainWindow()
    cfg.status_bar = cfg.main_window.statusBar()
    cfg.main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    launch_spikely()
