import sys
import locale

import pkg_resources
from PyQt5 import QtCore, QtWidgets, QtGui

from spikely import version, config

# TODO: Clean up code and comment


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.process = QtCore.QProcess(self)
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.stdout_ready)

        self._init_ui()

        piperun_path = pkg_resources.resource_filename(
            'spikely.pipeman', 'piperun.py')
        self.process.start('python', [piperun_path, sys.argv[1]])

        if self.process.state() == QtCore.QProcess.Starting \
                or self.process.state() == QtCore.QProcess.Running:
            self.cancel_btn.setDisabled(False)
            self.process.finished.connect(
                lambda: self.cancel_btn.setDisabled(True))

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

        self.cancel_btn = QtWidgets.QPushButton('Terminate Process')
        btn_box = QtWidgets.QHBoxLayout()
        btn_box.addStretch(1)
        btn_box.addWidget(self.cancel_btn)
        btn_box.addStretch(1)
        self.cancel_btn.setDisabled(True)
        self.cancel_btn.clicked.connect(self.process.kill)
        main_frame.layout().addLayout(btn_box)

    def append(self, text):
        self.output.append(text)

    def stdout_ready(self):
        text = bytearray(self.process.readAllStandardOutput())\
            .decode(locale.getdefaultlocale()[1])

        self.append(text)

    def closeEvent(self, event):
        if self.process.state() == QtCore.QProcess.Running:
            reply = QtWidgets.QMessageBox.question(
                config.find_main_window(), 'Exiting', 'Exiting will terminate'
                ' pipeline execution.  Are you sure you want to exit?',
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                event.ignore()


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

    # config.find_main_window().statusBar().showMessage(
    #     "Error Message", config.STATUS_MSG_TIMEOUT)


if __name__ == '__main__':
    main()
