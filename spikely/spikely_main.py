# Python imports
import sys
import pkg_resources
# PyQt imports
import PyQt5.QtGui as qg
import PyQt5.QtCore as qc
import PyQt5.QtWidgets as qw
# spikely imports
from . import file_menu
from . import config
from . import operation_view as sp_opv
from . import parameter_model as sp_pam
from . import parameter_view as sp_pav
from . import pipeline_model as sp_pim
from . import pipeline_view as sp_piv
from . import version


class SpikelyMainWindow(qw.QMainWindow):
    # Parent UI for application delegates to subwindow views/models
    def __init__(self):
        super().__init__()

        # Subwindows Views need underlying Model references
        self._parameter_model = sp_pam.ParameterModel()
        self._pipeline_model = sp_pim.PipelineModel(
            self._parameter_model)
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("spikely")
        self.setGeometry(100, 100, 1152, 472)

        try:
            spikely_png_path = pkg_resources.resource_filename(
                'spikely.resources', 'spikely.png')
            self.setWindowIcon(qg.QIcon(spikely_png_path))
        except KeyError:
            print('<<spikely error: Failed to find spikely.png in resource '
                  'directory>>', file=sys.stderr)

        self.statusBar().addPermanentWidget(
            qw.QLabel("Version " + version.__version__))

        menu_bar = self.menuBar()
        menu = file_menu.create_file_menu(self, self._pipeline_model)
        menu_bar.addMenu(menu)

        tool_bar = qw.QToolBar(self)
        tool_bar.setMovable(False)
        tool_bar.setFloatable(False)

        folder_act = qw.QAction(qw.QFileIconProvider().icon(
            qw.QFileIconProvider.Folder), 'Select Folder', self)
        folder_act.triggered.connect(_perform_folder_action)
        tool_bar.addAction(folder_act)

        file_act = qw.QAction(qw.QFileIconProvider().icon(
            qw.QFileIconProvider.File), 'Select File', self)
        file_act.triggered.connect(_perform_file_action)
        tool_bar.addAction(file_act)

        self.addToolBar(qc.Qt.RightToolBarArea, tool_bar)

        main_frame = qw.QFrame()
        self.setCentralWidget(main_frame)
        main_frame.setLayout(qw.QVBoxLayout())

        # Push subwindows down - create negative space below menu bar
        main_frame.layout().addStretch(1)

        pipe_param_splitter = qw.QSplitter()
        pipe_param_splitter.setChildrenCollapsible(False)

        # Subwindows for element pipeline and current element parameters
        pipe_param_splitter.addWidget(sp_piv.PipelineView(
            self._pipeline_model, self._parameter_model))
        pipe_param_splitter.addWidget(sp_pav.ParameterView(
            self._pipeline_model, self._parameter_model))
        pipe_param_splitter.setSizes([328, 640])
        main_frame.layout().addWidget(pipe_param_splitter)

        # Subwindow at bottom for pipeline operations (run, clear, queue)
        main_frame.layout().addWidget(sp_opv.OperationView(
            self._pipeline_model, self._parameter_model))


def _perform_file_action() -> None:
    global _pipeline_model

    options = qw.QFileDialog.Options()
    options |= qw.QFileDialog.DontUseNativeDialog
    file_name, _filter = qw.QFileDialog.getOpenFileName(
            config.find_main_window(), caption='Copy File Name',
            options=options)
    clip = qw.QApplication.clipboard()
    clip.setText('' if not file_name else file_name)


def _perform_folder_action() -> None:
    global _pipeline_model

    options = qw.QFileDialog.Options()
    options |= qw.QFileDialog.DontUseNativeDialog
    options |= qw.QFileDialog.ShowDirsOnly
    options |= qw.QFileDialog.DontResolveSymlinks
    folder_name = qw.QFileDialog.getExistingDirectory(
            config.find_main_window(), caption='Copy Folder Name',
            options=options)
    clip = qw.QApplication.clipboard()
    clip.setText('' if not folder_name else folder_name)


def launch_spikely():
    app = qw.QApplication(sys.argv)
    win = SpikelyMainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    launch_spikely()
