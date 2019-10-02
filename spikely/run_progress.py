import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import queue


class RunProgress():
    def __init__(self, pqueue):
        super().__init__()

        self.pqueue = pqueue

        self.msgBox = qw.QMessageBox()
        self.msgBox.setIcon(qw.QMessageBox.Information)
        self.msgBox.setText("Pipeline is running")
        self.msgBox.setWindowTitle("Pipeline Execution Status")
        self.msgBox.setStandardButtons(qw.QMessageBox.Ok)
        self.msgBox.setModal(False)
        self.msgBox.buttonClicked.connect(self.cancel)

        self.msgBox.show()

        self.t = qc.QTimer()
        self.t.timeout.connect(self.perform)
        self.t.start(500)

    def perform(self):
        try:
            self.pqueue.get(False)
        except queue.Empty:
            pass
        else:
            self.msgBox.close()
            self.t.stop()

    def cancel(self):
        self.msgBox.close()
