import PyQt5.QtWidgets as qw


def create_file_menu(main_window):
    file_menu = qw.QMenu('&File', main_window)
    file_menu.addAction(_create_exit_action(main_window))
    return file_menu


def _create_exit_action(main_window):
    exit_action = qw.QAction('Exit', main_window)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.setStatusTip('Terminate the application')
    exit_action.triggered.connect(qw.QApplication.closeAllWindows)
    return exit_action


def _create_load_action(main_window):
    pass


def _perform_load_action():
    pass


def _create_save_action(main_window):
    pass


def _perform_save_action():
    pass
