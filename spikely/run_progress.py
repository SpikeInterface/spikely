import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc


class RunProgress():
    def __init__(self, run_queue, run_proc):
        super().__init__()

        self.run_queue = run_queue
        self.run_proc = run_proc

        self.run_dlg = qw.QMessageBox()
        self.run_dlg.setIcon(qw.QMessageBox.NoIcon)
        self.run_dlg.setWindowTitle("Pipeline Execution Status")
        self.run_dlg.setText("Running pipeline executing normally")
        self.run_dlg.setModal(False)

        # self.run_dlg.setStandardButtons(
        #     qw.QMessageBox.Ok | qw.QMessageBox.Cancel)
        self.run_dlg.setStandardButtons(qw.QMessageBox.Ok)
        self.run_dlg.buttonClicked.connect(self.terminate)

        self.run_dlg.show()

        self.timer = qc.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def update(self):
        if not self.run_queue.empty():
            self.run_dlg.setIcon(qw.QMessageBox.Information)
            self.run_dlg.setText(
                'Running pipeline terminated normally')
            self.timer.stop()
        elif not self.run_proc.is_alive():
            self.run_dlg.setIcon(qw.QMessageBox.Warning)
            self.run_dlg.setText(
                'Running pipeline exited prematurely')
            self.timer.stop()

    def terminate(self):
        # std_btn = self.run_dlg.standardButton(
        #     self.run_dlg.clickedButton()
        # if std_btn == qw.QMessageBox.Cancel:
        #     print("<<< Killing child process! >>>")
        #     self.proc.terminate()
        self.run_dlg.close()
        self.timer.stop()
