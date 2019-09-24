import PyQt5.QtCore as qc
import PyQt5.QtWidgets as qw

import multiprocessing as mp

from spikely import config as cfg


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
            elif role == cfg.ELEMENT_ROLE:
                result = element

        return result

    # Methods called by app to manipulate and operate pipeline
    def run(self):

        bad_count = self._bad_param_count()
        if bad_count:
            qw.QMessageBox.warning(
                cfg.find_main_window(), 'Run Failure',
                f'Missing {self._bad_param_count()} required ' +
                ('parameter' if bad_count == 1 else 'parameters'))
        else:
            """Call SpikeInterface APIs on elements in pipeline"""
            cfg.find_main_window().statusBar().showMessage(
                'Running pipeline', cfg.STATUS_MSG_TIMEOUT)
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
            cfg.find_main_window().statusBar().showMessage(
                'Nothing to clear', cfg.STATUS_MSG_TIMEOUT)

    def add_element(self, element):

        insert_row = -1
        if not self._elements:
            insert_row = 0
        else:
            for row in range(len(self._elements)):
                upstream = None if row == 0 else row - 1
                downstream = None if row == len(self._elements) else row
                if element.fits_between(upstream, downstream):
                    insert_row = row
                    break

        if insert_row >= 0:
            self.beginInsertRows(qc.QModelIndex(), insert_row, insert_row)
            self._elements.insert(insert_row, element)
            self.endInsertRows()

    def move_up(self, element):
        i = self._elements.index(element)
        # Elements confined to their stage
        if (i > 0 and self._elements[i].interface_id
                == self._elements[i-1].interface_id):
            self.beginMoveRows(qc.QModelIndex(), i, i, qc.QModelIndex(), i-1)
            self._swap(self._elements, i, i-1)
            self.endMoveRows()
        else:
            cfg.find_main_window().statusBar().showMessage(
                "Cannot move element any higher", cfg.STATUS_MSG_TIMEOUT)

    def move_down(self, element):
        i = self._elements.index(element)
        # Elements confined to their stage
        if (i < (len(self._elements) - 1) and
                self._elements[i].interface_id
                == self._elements[i+1].interface_id):
            # beginMoveRows behavior is fubar if move down from source to dest
            self.beginMoveRows(qc.QModelIndex(), i+1, i+1, qc.QModelIndex(), i)
            self._swap(self._elements, i, i+1)
            self.endMoveRows()
        else:
            cfg.find_main_window().statusBar().showMessage(
                "Cannot move element any lower", cfg.STATUS_MSG_TIMEOUT)

    def delete(self, element):
        index = self._elements.index(element)
        self.beginRemoveRows(qc.QModelIndex(), index, index)
        self._elements.pop(index)
        self.endRemoveRows()

    # Convenience methods used only within class
    def _has_instance(self, interface_id):
        # Checks if element instance already in pipeline
        for element in self._elements:
            if element.interface_id == interface_id:
                return True

        # Generator expression equivalent for future reference
        # return sum(1 for ele in self._elements if
        # ele.interface_id == interface_id)

    def _swap(self, list, pos1, pos2):
        list[pos1], list[pos2] = list[pos2], list[pos1]

    def _bad_param_count(self):
        # Counts incomplete mandatory parameters in pipeline
        count = 0
        for element in self._elements:
            for param in element.params:
                if 'value' not in param.keys():
                    count += 1
        return count
