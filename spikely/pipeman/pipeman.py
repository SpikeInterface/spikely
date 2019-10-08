from PyQt5 import QtCore, QtWidgets
from spikely import version
import pkg_resources
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self._init_ui()
        self._init_run()

        # self.process.started.connect(lambda: p('Started!'))
        # self.process.finished.connect(lambda: p('Finished!'))
        # print 'Starting process'
        # self.process.start('python', ['speak.py'])

    def _init_ui(self):
        self.setWindowTitle("spikely pipeman")
        self.resize(384, 256)

        self.statusBar().addPermanentWidget(
            QtWidgets.QLabel("Version " + version.__version__))

        main_frame = QtWidgets.QFrame()
        self.setCentralWidget(main_frame)
        main_frame.setLayout(QtWidgets.QVBoxLayout())

        self.output = QtWidgets.QTextEdit(self)
        self.output.setReadOnly(True)
        self.output.setAcceptRichText(False)

        main_frame.layout().addWidget(self.output)

    def _init_run(self):
        fn = pkg_resources.resource_filename('spikely.pipeman', 'piperun.py')

        self.process = QtCore.QProcess(self)
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.stdout_ready)
        # self.process.readyReadStandardError.connect(self.stderr_ready)
        self.process.start('python', [fn, sys.argv[1]])

    def append(self, text):
        # cursor = self.output.textCursor()
        # cursor.movePosition(cursor.End)
        # cursor.insertText(text)
        # self.output.ensureCursorVisible()
        self.output.append(text)

    def stdout_ready(self):
        text = bytearray(self.process.readAllStandardOutput()).decode()
        # text = ba.decode('utf-8')
        self.append(text)

    def stderr_ready(self):
        text = bytearray(self.process.readAllStandardError()).decode()
        # text = ba.decode('utf-8')
        self.append(text)


def main():
    app = QtWidgets.QApplication(sys.argv)

    # for index, arg in enumerate(sys.argv):
    #     print(f'index: {index}\n{arg}\n')

    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
