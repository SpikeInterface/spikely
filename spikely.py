"""UI for SpikeInterface extracellular data processing pipelines.

The application enables a user to constuct a pipeline consisting of elements
associated with extracellular data recording extraction, pre-processing,
sorting, and post-processing.  The user can configure the properties of each
element, and once satisifed with the pipeline construction and element
configuration operate the pipeline.

Modules:
    spikely.py - Main application module
    spikely_core.py - Constants and utilities
    cp_view.py - Construct Pipeline UI region
    op_view.py - Operate Pipeline UI region
    ce_view.py - Configure Element UI region
    pi_model.py - Pipeline Model: multi-stage element execution list
    el_model.py - Element Model: SpikeInterface component wrappers
"""

import sys

import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg

from op_view import OperatePipelineView
from cp_view import ConstructPipelineView
from ce_view import ConfigureElementView

from pi_model import SpikePipeline

__version__ = "0.2.0"


class SpikelyMainWindow(qw.QMainWindow):
    """Instantiates the overall UI for the application"""

    def __init__(self):

        super().__init__()

        # The primary role of the UI is to manage the active pipeline
        self._active_pipe = SpikePipeline()

        # Enhances print() use for debug
        sys.stdout.flush()

        self._init_ui()

    def _init_ui(self):
        """Assembles the main UI from delegated sub-views."""

        # Application main window setup
        self.setWindowTitle("Spikely")
        self.setGeometry(100, 100, 1024, 384)
        self.setWindowIcon(qg.QIcon("bin/spikely.png"))
        self.statusBar().addPermanentWidget(
            qw.QLabel("Version " + __version__))

        # Lay out application views in main window from top to bottom
        main_layout = qw.QVBoxLayout()
        main_layout.addStretch(1)  # Pushes app window widgets down

        """ Lay out Construction Pipeline (cp) and Configure Element (ce)
        views in a frame at top of main window from left to right
        """
        cp_ce_splitter = qw.QSplitter()
        cp_ce_splitter.setChildrenCollapsible(False)

        # Actual widget construction done in View classes
        cp_ce_splitter.addWidget(ConstructPipelineView(self._active_pipe))
        cp_ce_splitter.addWidget(ConfigureElementView(self._active_pipe))
        cp_ce_splitter.setSizes([256, 768])
        main_layout.addWidget(cp_ce_splitter)

        # Lay out Operate Pipeline (op)view at bottom of main window
        main_layout.addWidget(OperatePipelineView(self._active_pipe))

        # Core application UI in main_frame as CentralWidget of QMainWindow
        main_frame = qw.QFrame()
        main_frame.setLayout(main_layout)
        self.setCentralWidget(main_frame)


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    win = SpikelyMainWindow()
    win.show()
    sys.exit(app.exec_())
