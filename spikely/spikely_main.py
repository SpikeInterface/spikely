""" Main module for spikely application

This module is home to the entry point for the application, launch_spikely(),
called when the user invokes spikely from the command line. In response,
spikely_main instantiates the PyQt Application class (QApplication) and the
associated widget hierarchy starting w/ SpikelyMainWindow at the top.  Once
these tasks are performed, execution shifts to the xxx_view.py and xxx_menu.py
modules whose methods are called in response to user interactions with the UI.

"""
import sys

import pkg_resources
from PyQt5 import QtWidgets, QtCore, QtGui

from spikely import (
    PipelineModel, PipelineView, ParameterView, ParameterModel,
    OperationView, file_menu, help_menu, tool_bar, __version__)


class SpikelyMainWindow(QtWidgets.QMainWindow):
    # Parent UI for application delegates to subwindow views/models
    def __init__(self):
        super().__init__()

        # Subwindows Views need underlying Model references
        self._parameter_model = ParameterModel()
        self._pipeline_model = PipelineModel(self._parameter_model)
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("spikely")
        self.setGeometry(100, 100, 1280, 512)

        # Disable maximize button on title bar
        # self.setWindowFlags(self.windowFlags()
        #                     & ~QtCore.Qt.WindowMaximizeButtonHint)

        try:
            spikely_png_path = pkg_resources.resource_filename(
                "spikely.resources", "spikely.png")
        except KeyError:
            print(
                "<<spikely error: Failed to find spikely.png in resource "
                "directory>>", file=sys.stderr,)
        else:
            self.setWindowIcon(QtGui.QIcon(spikely_png_path))

        self.statusBar().addPermanentWidget(
            QtWidgets.QLabel("Version " + __version__))

        menu_bar = self.menuBar()
        menu_bar.addMenu(file_menu.create_file_menu(
            self, self._pipeline_model))
        menu_bar.addMenu(help_menu.create_help_menu(self))

        bar = tool_bar.create_tool_bar(self)
        self.addToolBar(QtCore.Qt.RightToolBarArea, bar)

        main_frame = QtWidgets.QFrame()
        self.setCentralWidget(main_frame)
        main_frame.setLayout(QtWidgets.QVBoxLayout())

        pipe_param_splitter = QtWidgets.QSplitter()
        pipe_param_splitter.setChildrenCollapsible(False)

        # Subwindows for element pipeline and selected element parameters
        pipe_param_splitter.addWidget(
            PipelineView(self._pipeline_model, self._parameter_model))
        pipe_param_splitter.addWidget(
            ParameterView(self._pipeline_model, self._parameter_model))
        pipe_param_splitter.setSizes([256, 1024])
        main_frame.layout().addWidget(pipe_param_splitter)

        # Subwindow at bottom for pipeline operations (run, clear, queue)
        main_frame.layout().addWidget(
            OperationView(self._pipeline_model, self._parameter_model))

        # Stretches pipeline and parameter widgets down as window grows
        main_frame.layout().setStretch(0, 1)


def launch_spikely():
    app = QtWidgets.QApplication(sys.argv)
    win = SpikelyMainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    launch_spikely()
