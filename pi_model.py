"""Class definition of SpikePipeline.

Implements the pipeline of SpikeInterface elements responsible
extracellular data processing.
"""

from contextlib import contextmanager
import copy

import PyQt5.QtCore as qc
import PyQt5.QtGui as qg

import config
from el_model import SpikeElement


class SpikePipelineModel(qc.QAbstractListModel):
    """TBD."""

    def __init__(self, element_model):
        """TBD."""
        super().__init__()
        self._elements = []
        self._element_model = element_model
        self._decorations = [
            qg.QIcon("bin/EXTR.png"),
            qg.QIcon("bin/PREP.png"),
            qg.QIcon("bin/SORT.png"),
            qg.QIcon("bin/POST.png")
        ]

    def rowCount(self, parent):
        return len(self._elements)

    def _stage_count(self, type):
        # The power of Python generator expressions ;^)
        return sum(1 for ele in self._elements if ele.type == type)

    def data(self, mod_index, role=qc.Qt.DisplayRole):
        result = None

        if mod_index.isValid() and mod_index.row() < len(self._elements):
            element = self._elements[mod_index.row()]
            if role == qc.Qt.DisplayRole or role == qc.Qt.EditRole:
                result = element.name
            elif role == qc.Qt.DecorationRole:
                result = self._decorations[element.type]
            elif role == config.ELEMENT_ROLE:
                result = element

        return result

    def run(self):
        """TBD."""
        pass

    def clear(self):
        """TBD."""
        self.beginResetModel()
        self._elements.clear()
        self.endResetModel()

    def add_element(self, element):

        # Only allow one Extractor or Sorter
        if element.type == config.EXTRACTOR or element.type == config.SORTER:
            if self._stage_count(element.type) > 0:
                config.status_bar.showMessage(
                    "Only one instance of that element type allowed.",
                    config.TIMEOUT)
                return

        i = 0
        while (i < len(self._elements) and
                element.type >= self._elements[i].type):
            i += 1
        self.beginInsertRows(qc.QModelIndex(), i, i)
        self._elements.insert(i, SpikeElement(element))
        self.endInsertRows()

    def _swap(self, list, pos1, pos2):
        list[pos1], list[pos2] = list[pos2], list[pos1]

    def move_up(self, element):
        i = self._elements.index(element)
        if i > 0 and self._elements[i].type == self._elements[i-1].type:
            self.beginMoveRows(qc.QModelIndex(), i, i, qc.QModelIndex(), i-1)
            self._swap(self._elements, i, i-1)
            self.endMoveRows()
        else:
            config.status_bar.showMessage(
                "Cannot move element any higher.", config.TIMEOUT)

    def move_down(self, element):
        i = self._elements.index(element)
        if (i < (len(self._elements) - 1) and
                self._elements[i].type == self._elements[i+1].type):
            # beginMoveRows behavior is fubar if move down from source to dest
            self.beginMoveRows(qc.QModelIndex(), i+1, i+1, qc.QModelIndex(), i)
            self._swap(self._elements, i, i+1)
            self.endMoveRows()
        else:
            config.status_bar.showMessage(
                "Cannot move element any lower.", config.TIMEOUT)

    def delete(self, element):
        index = self._elements.index(element)
        self.beginRemoveRows(qc.QModelIndex(), index, index)
        self._elements.pop(index)
        self.endRemoveRows()
