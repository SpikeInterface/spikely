# Application help menu construction and execution

import webbrowser

import PyQt5.QtWidgets as qw


def create_help_menu(main_window: qw.QMainWindow) -> qw.QMenu:
    help_menu = qw.QMenu('&Help', main_window)
    help_menu.addAction(_create_doc_action(main_window))
    return help_menu


def _create_doc_action(main_window: qw.QMainWindow) -> qw.QAction:
    doc_action = qw.QAction('Documentation', main_window)
    doc_action.setShortcut('Ctrl+D')
    doc_action.setStatusTip('Open spikely documentation link in web browser')
    doc_action.triggered.connect(_open_doc_browser)
    return doc_action


def _open_doc_browser():
    webbrowser.open('https://spikely.readthedocs.io/en/latest/index.html#a-simple-extracellur-data-processing-application-based-on-spikeinterface)')  # noqa: E501
