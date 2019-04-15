"""Class definition of SpikePipeline.

Implements the pipeline of SpikeInterface elements responsible
extracellular data processing.
"""

import PyQt5.QtCore as qc
import PyQt5.QtGui as qg
import PyQt5.QtWidgets as qw

import spikely_constants as sc
from el_model import SpikeElement


class SpikePipeline(qc.QAbstractListModel):
    """TBD."""

    def __init__(self):
        """TBD."""
        super().__init__()
        self._ele_list = []
        self._decorations = [
            qg.QIcon("EXTR.png"),
            qg.QIcon("PREP.png"),
            qg.QIcon("SORT.png"),
            qg.QIcon("POST.png")
        ]

    def rowCount(self, parent):
        return len(self._ele_list)

    def data(self, index, role=qc.Qt.DisplayRole):
        ret_val = None

        if index.isValid() and index.row() < len(self._ele_list):
            if role == qc.Qt.DisplayRole or role == qc.Qt.EditRole:
                ret_val = self._ele_list[index.row()].name()
            elif role == qc.Qt.DecorationRole:
                ret_val = self._decorations[
                    self._ele_list[index.row()].stage_id()]

        return ret_val

    def run(self):
        """TBD."""
        print("Pipeline Running")
        pass

    def clear(self):
        """TBD."""
        self.beginResetModel()
        self._ele_list.clear()
        # self.dataChanged.emit(qc.QModelIndex(), qc.QModelIndex())
        # self.modelReset.emit()
        self.endResetModel()

    def delete(self, index):
        self.beginResetModel()
        self._ele_list.pop(index)
        self.endResetModel()

    def add_element(self, new_ele):
        i = 0
        while (i < len(self._ele_list) and
                new_ele.stage_id() >= self._ele_list[i].stage_id()):
            i += 1

        self._ele_list.insert(i, new_ele)
        self.dataChanged.emit(qc.QModelIndex(), qc.QModelIndex())
