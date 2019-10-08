import sys

import pkg_resources
from PyQt5 import QtCore, QtWidgets, QtGui

from spikely import version


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self._init_ui()
        self._init_piperun()

        # self.process.started.connect(lambda: print(
        #     'spikely pipeline running...'))
        # # self.process.finished.connect(lambda: p('Finished!'))

    def _init_ui(self):
        self.setWindowTitle("spikely pipeline manager")
        self.resize(640, 384)

        self.statusBar().addPermanentWidget(
            QtWidgets.QLabel("Version " + version.__version__))

        main_frame = QtWidgets.QFrame()
        self.setCentralWidget(main_frame)
        main_frame.setLayout(QtWidgets.QVBoxLayout())

        self.output = QtWidgets.QTextEdit(self)
        self.output.setReadOnly(True)
        self.output.setAcceptRichText(False)
        self.output.setStyleSheet(
            "QTextEdit { color: green; background-color: black; }")
        self.output.setWordWrapMode(QtGui.QTextOption.NoWrap)

        main_frame.layout().addWidget(self.output)

    def _init_piperun(self):
        piperun_path = pkg_resources.resource_filename(
            'spikely.pipeman', 'piperun.py')

        self.process = QtCore.QProcess(self)
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.stdout_ready)
        self.process.start('python', [piperun_path, sys.argv[1]])

    def append(self, text):
        self.output.append(text)

    def stdout_ready(self):
        text = bytearray(self.process.readAllStandardOutput()).decode()
        self.append(text)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
