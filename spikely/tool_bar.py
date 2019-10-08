from PyQt5 import QtWidgets
from . import config

# TODO: Implement instance (versus class) version of QFileDialog


# Menu and Menu Action construction methods
def create_tool_bar(main_win):
    tool_bar = QtWidgets.QToolBar(main_win)
    tool_bar.setMovable(False)
    tool_bar.setFloatable(False)

    folder_act = QtWidgets.QAction(QtWidgets.QFileIconProvider().icon(
        QtWidgets.QFileIconProvider.Folder), 'Select Folder', main_win)
    folder_act.setStatusTip('Choose folder and copy path into clipboard '
        'to enable pasting path into an element parameter field')  # noqa: E128
    folder_act.triggered.connect(_perform_folder_action)
    tool_bar.addAction(folder_act)

    file_act = QtWidgets.QAction(QtWidgets.QFileIconProvider().icon(
        QtWidgets.QFileIconProvider.File), 'Select File', main_win)
    file_act.setStatusTip('Choose file and copy path into clipboard '
        'to enable pasting path into an element parameter field')  # noqa: E128
    file_act.triggered.connect(_perform_file_action)
    tool_bar.addAction(file_act)

    return tool_bar


def _perform_file_action() -> None:

    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.DontUseNativeDialog
    file_name, _filter = QtWidgets.QFileDialog.getOpenFileName(
            config.find_main_window(), caption='Copy File Name to Clipboard',
            options=options)

    if file_name:
        QtWidgets.QApplication.clipboard().setText(file_name)


def _perform_folder_action() -> None:

    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.DontUseNativeDialog
    options |= QtWidgets.QFileDialog.ShowDirsOnly
    options |= QtWidgets.QFileDialog.DontResolveSymlinks
    folder_name = QtWidgets.QFileDialog.getExistingDirectory(
            config.find_main_window(), caption='Copy Folder Name to Clipboard',
            options=options)

    if folder_name:
        QtWidgets.QApplication.clipboard().setText(folder_name)


'''
    # tool_menu = menu_bar.addMenu(qw.QMenu('Tools', self))
    # dir_action = qw.QAction('Pick Directory', self)
    # dir_action.setShortcut('Ctrl+D')
    # dir_action.setStatusTip('Copy directory path to clipboard')
    # dir_action.triggered.connect(self.do_dir_action)
    # tool_menu.addAction(dir_action)

   # def do_dir_action(self):
    #     dlg = qw.QFileDialog(self)
    #     dlg.setFileMode(dlg.Directory)
    #     dlg.setViewMode(dlg.List)
    #     dlg.setDirectory('.')
    #     dlg.setOption(dlg.DontUseNativeDialog, True)
    #     # dlg.setOption(dlg.ShowDirsOnly, True)
    #     dlg.setOption(dlg.ReadOnly, True)
    #     dlg.setOption(dlg.HideNameFilterDetails, True)

    #     if (dlg.exec_()):
    #         file_names = dlg.selectedFiles()
    #         cb = qw.QApplication.clipboard()
    #         cb.setText(file_names[0])
'''
