"""UI for SpikeInterface extracellular data processing pipelines.

The application enables a user to constuct a pipeline consisting of elements
associated with extracellular data recording extraction, pre-processing,
sorting, and curation.  The user can configure the properties of each
element, and once satisifed with the pipeline construction and element
configuration operate the pipeline.

Modules:
    ce_view.py - UI to configure element parameters
    cfg.py - Constants and globals used throughout
    cp_view.py - UI to select, insert, and manipulate elements in pipeline
    el_model.py - SpikeElementModel bridges SpikeElement to/from UI
    op_view.py - UI to manage pipeline commands (e.g., clear, run, queue)
    pi_model.py - SpikePipeline model bridges element pipeline to/from UI
    spike_element.py - SpikeElement class from which to subclass elements
    spikely.py - Main application sets up UI and executes event loop
"""

import sys

import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg

from spikely.op_view import OperatePipelineView
from spikely.cp_view import ConstructPipelineView
from spikely.ce_view import ConfigureElementView
from spikely.pi_model import SpikePipelineModel
from spikely.el_model import SpikeElementModel

import pkg_resources

from . import config as cfg
from spikely.version import __version__


class SpikelyMainWindow(qw.QMainWindow):
    """Main window for the application"""

    def __init__(self):

        super().__init__()

        # Active pipeline and element models
        self._element_model = SpikeElementModel()
        self._pipeline_model = SpikePipelineModel(
            self._element_model)

        # Enhances print() use for debug
        sys.stdout.flush()

        self._init_ui()

    def _init_ui(self):
        """Assembles the main UI from delegated sub-views."""

        # Application main window setup
        self.setWindowTitle("Spikely")
        self.setGeometry(100, 100, 1152, 448)

        spikely_png_path = pkg_resources.resource_filename(
            'spikely.resources', 'spikely.png')

        self.setWindowIcon(qg.QIcon(spikely_png_path))
        self.statusBar().addPermanentWidget(
            qw.QLabel("Version " + __version__))

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
        cp_ce_splitter.addWidget(ConstructPipelineView(
            self._pipeline_model, self._element_model))
        cp_ce_splitter.addWidget(ConfigureElementView(
            self._pipeline_model, self._element_model))
        cp_ce_splitter.setSizes([328, 640])
        main_frame.layout().addWidget(cp_ce_splitter)

        # Lay out Operate Pipeline (op) view at bottom of main window
        main_frame.layout().addWidget(OperatePipelineView(
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
