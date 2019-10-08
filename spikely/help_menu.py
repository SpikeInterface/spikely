# Application help menu construction and execution

import webbrowser

import PyQt5.QtWidgets as qw


def create_help_menu(main_window: qw.QMainWindow) -> qw.QMenu:
    help_menu = qw.QMenu('&Help', main_window)
    _create_help_actions(help_menu, main_window)
    return help_menu


def _create_help_actions(menu, win):
    file_actions = [
         ('Documentation', 'Ctrl+D',
          'Open spikely documentation link in web browser',
          _open_doc_browser)
        ]

    for name, shortcut, statustip, signal in file_actions:
        action = qw.QAction(name, win)
        action.setShortcut(shortcut)
        action.setStatusTip(statustip)
        action.triggered.connect(signal)
        menu.addAction(action)


def _open_doc_browser():
    webbrowser.open('https://spikely.readthedocs.io/en/latest/index.html#a-simple-extracellur-data-processing-application-based-on-spikeinterface)')  # noqa: E501
