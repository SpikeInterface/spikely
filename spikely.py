"""UI for SpikeInterface extracellular data processing pipelines.

The application allows users to load an extracellular recording, run 
preprocessing on the recording, run an installed spike sorter, and 
then run postprocessing on the results. All results are saved into a folder.

Loosely based on a hierarchical MVC design pattern, the application is
divided into modules corresponding to the functional screen regions
(the views) and the major data structures (the models)

Modules:
    spikely.py - Main application module
    op_view.py - Operate Pipeline UI region
    cp_view.py - Construct Pipeline UI region 
    ce_view.py - Configure Element UI region 
    pi_model.py - Pipeline Model: multi-stage element execution list
    el_model.py - Element Model: SpikeInterface component wrappers
    qu_model.py - Queue Model: pipeline execution list
"""

import sys

import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg

from op_view import OperatePipelineView
from pi_model import SpikePipeline
from cp_view import ConstructPipelineView
from ce_view import ConfigureElementView

__version__ = "0.1.5"

class SpikelyMainWindow(qw.QMainWindow):
    """Main window of application.

    No public methods other than constructor.
    """

    def __init__(self):
        """Initialize parent, instantiate object members, build UI."""
        super().__init__()

        # Underlying data structure managed by UI
        self._active_pipe = SpikePipeline()

        sys.stdout.flush() # forces print() out for debugging
        self._init_ui()


    def _init_ui(self):

        # Application window setup
        self.setWindowTitle("Spikely")
        self.setGeometry(100, 100, 900, 400)
        self.setWindowIcon(qg.QIcon("spikely.png"))
        self.statusBar().addPermanentWidget(
            qw.QLabel("Version " + __version__))
        
        # Lay out application views in main window from top to bottom
        main_layout = qw.QVBoxLayout()  
        main_layout.addStretch(1) # Pushes app window widgents down

        """ Lay out Construction Pipeline (ce) and Configure Element (ce)
        views in a frame at top of main window from left to right
        """
        cp_ce_frame = qw.QFrame()
        cp_ce_layout = qw.QHBoxLayout()
        cp_ce_frame.setLayout(cp_ce_layout)
        # Actual widget construction done in View classes
        cp_ce_layout.addWidget(ConstructPipelineView(self._active_pipe))
        cp_ce_layout.addWidget(ConfigureElementView(self._active_pipe))
        main_layout.addWidget(cp_ce_frame)

        # Lay out Operation view at bottom of main window
        main_layout.addWidget(OperatePipelineView(self._active_pipe))

        main_frame = qw.QFrame()
        main_frame.setLayout(main_layout)
        self.setCentralWidget(main_frame)

if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    app_win = SpikelyMainWindow()
    app_win.show()
    sys.exit(app.exec_())
