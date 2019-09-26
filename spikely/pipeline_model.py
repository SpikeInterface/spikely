import PyQt5.QtCore as qc
import PyQt5.QtWidgets as qw

import multiprocessing as mp

from . import config
from . import spike_element as sp_spe


class PipelineModel(qc.QAbstractListModel):

    def __init__(self, parameter_model):
        super().__init__()

        # Underlying data structure proxied by model
        self._elements = []

    # Overloaded methods from QAbstractListModel
    def rowCount(self, parent=None):
        return len(self._elements)

    def data(self, mod_index, role=qc.Qt.DisplayRole):
        result = None
        if mod_index.isValid() and mod_index.row() < len(self._elements):
            element = self._elements[mod_index.row()]
            if role == qc.Qt.DisplayRole or role == qc.Qt.EditRole:
                result = element.display_name
            elif role == qc.Qt.DecorationRole:
                result = element.display_icon
            # Custom role for spikely callers to access pipeline elements
            elif role == config.ELEMENT_ROLE:
                result = element

        return result

    # Methods called by app to manipulate and operate pipeline
    def run(self):

        bad_count = self._bad_param_count()
        if bad_count:
            qw.QMessageBox.warning(
                config.find_main_window(), 'Run Failure',
                f'Missing {self._bad_param_count()} required ' +
                ('parameter' if bad_count == 1 else 'parameters'))
        else:
            """Call SpikeInterface APIs on elements in pipeline"""
            config.find_main_window().statusBar().showMessage(
                'Running pipeline', config.STATUS_MSG_TIMEOUT)
            p = mp.Process(target=self.async_run)
            p.start()

    def async_run(self):
        input_payload = None
        element_count = len(self._elements)

        for i in range(0, element_count):
            next_element = self._elements[i+1] \
                if i < (element_count - 1) else None
            input_payload = self._elements[i].run(
                input_payload, next_element
            )

    def clear(self):
        if len(self._elements):
            self.beginResetModel()
            self._elements.clear()
            self.endResetModel()
        else:
            config.find_main_window().statusBar().showMessage(
                'Nothing to clear', config.STATUS_MSG_TIMEOUT)

    def add_element(self, elem: sp_spe.SpikeElement) -> None:
        insert_row = -1
        # Does it fit at the top of the pipeline?
        if not self._elements or elem.fits_between(None, self._elements[0]):
            insert_row = 0
        # Does it fit between the first and the last elements in the pipeline?
        else:
            for row in range(len(self._elements) - 1):
                if elem.fits_between(self._elements[row],
                                     self._elements[row + 1]):
                    insert_row = row + 1
                    break
        # Last chance - does it fit at the end of the pipeline?
        if insert_row == -1 and elem.fits_between(self._elements[-1], None):
            insert_row = len(self._elements)

        if insert_row >= 0:
            self.beginInsertRows(qc.QModelIndex(), insert_row, insert_row)
            self._elements.insert(insert_row, elem)
            self.endInsertRows()

    def move_up(self, element: sp_spe.SpikeElement) -> None:
        elem_row = self._elements.index(element)
        elem_moved = False
        if elem_row:
            up = None if elem_row == 1 else self._elements[elem_row - 2]
            dn = self._elements[elem_row - 1]

            if element.fits_between(up, dn):
                elem_moved = True
                self.beginMoveRows(qc.QModelIndex(), elem_row,
                    elem_row, qc.QModelIndex(), elem_row - 1)  # noqa: E128
                self._swap(self._elements, elem_row, elem_row - 1)
                self.endMoveRows()

        if not elem_moved:
            config.find_main_window().statusBar().showMessage(
                "Cannot move element any higher", config.STATUS_MSG_TIMEOUT)

    def move_down(self, element: sp_spe.SpikeElement) -> None:
        elem_row = self._elements.index(element)
        elem_moved = False
        if elem_row != len(self._elements) - 1:
            up = self._elements[elem_row + 1]
            dn = None if elem_row == len(self._elements) - 2 \
                else self._elements[elem_row + 2]
            if element.fits_between(up, dn):
                elem_moved = True
                self.beginMoveRows(qc.QModelIndex(), elem_row + 1,
                    elem_row + 1, qc.QModelIndex(), elem_row)   # noqa: E128
                self._swap(self._elements, elem_row, elem_row + 1)
                self.endMoveRows()
        if not elem_moved:
            config.find_main_window().statusBar().showMessage(
                "Cannot move element any lower", config.STATUS_MSG_TIMEOUT)

    def delete(self, element: sp_spe.SpikeElement) -> None:
        index = self._elements.index(element)
        self.beginRemoveRows(qc.QModelIndex(), index, index)
        self._elements.pop(index)
        self.endRemoveRows()

    def _swap(self, list, pos1, pos2):
        list[pos1], list[pos2] = list[pos2], list[pos1]

    def _bad_param_count(self) -> int:
        # Counts incomplete mandatory parameters in pipeline
        count = 0
        for element in self._elements:
            for param in element.params:
                if 'value' not in param.keys():
                    count += 1
        return count
