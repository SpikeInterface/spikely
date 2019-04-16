"""UI for SpikeInterface extracellular data processing pipelines.

The application enables a user to constuct a pipeline consisting of elements
associated with extracellular data recording extraction, pre-processing,
sorting, and post-processing.  The user can configure the properties of each
element, and once satisifed with the pipeline construction and element
configuration operate the pipeline.

Modules:
    spikely.py - Main application module
    spikely_constants.py - common application constant values.
    op_view.py - Operate Pipeline UI region
    cp_view.py - Construct Pipeline UI region
    ce_view.py - Configure Element UI region
    pi_model.py - Pipeline Model: multi-stage element execution list
    el_model.py - Element Model: SpikeInterface component wrappers
"""

import sys

import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg

from op_view import OperatePipelineView
from pi_model import SpikePipeline
from cp_view import ConstructPipelineView
from ce_view import ConfigureElementView

import spikely_constants as sc

__version__ = "0.2.0"


class SpikelyMainWindow(qw.QMainWindow):
    """Main window of application.

    No public methods other than constructor.
    """

    def __init__(self):
        """Initialize parent, instantiate object members, build UI."""
        super().__init__()

        """Primary role of app the is the construction, configuration, and
        operation of the active pipeline."""
        self._active_pipe = SpikePipeline()

        sys.stdout.flush()  # forces print() out for debugging
        self._init_ui()

    def _init_ui(self):
        """Responsible for constructing the UI from delegated views."""

        # Application main window setup
        self.setWindowTitle("Spikely")
        self.setGeometry(100, 100, 900, 400)
        self.setWindowIcon(qg.QIcon("bin/spikely.png"))
        self.statusBar().addPermanentWidget(
            qw.QLabel("Version " + __version__))

        # Lay out application views in main window from top to bottom
        main_layout = qw.QVBoxLayout()
        main_layout.addStretch(1)  # Pushes app window widgets down

        """ Lay out Construction Pipeline (cp) and Configure Element (ce)
        views in a frame at top of main window from left to right
        """
        cp_ce_frame = qw.QFrame()
        cp_ce_layout = qw.QHBoxLayout()
        cp_ce_frame.setLayout(cp_ce_layout)

        # Actual widget construction done in View classes
        cp_ce_layout.addWidget(ConstructPipelineView(self._active_pipe))
        cp_ce_layout.addWidget(ConfigureElementView(self._active_pipe))
        main_layout.addWidget(cp_ce_frame)

        # Lay out Operate Pipeline (op)view at bottom of main window
        main_layout.addWidget(OperatePipelineView(self._active_pipe))

        main_frame = qw.QFrame()
        main_frame.setLayout(main_layout)
        self.setCentralWidget(main_frame)

if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    win = SpikelyMainWindow()
    win.show()
    sys.exit(app.exec_())
