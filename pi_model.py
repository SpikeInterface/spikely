"""Class definition of SpikePipeline.

Implements the pipeline of SpikeInterface elements responsible
extracellular data processing.
"""

from contextlib import contextmanager

import PyQt5.QtCore as qc
import PyQt5.QtGui as qg

import spikely_core as sc


class SpikePipeline(qc.QAbstractListModel):
    """TBD."""

    def __init__(self):
        """TBD."""
        super().__init__()
        self._ele_list = []
        self._ele_model = None
        self._decorations = [
            qg.QIcon("bin/EXTR.png"),
            qg.QIcon("bin/PREP.png"),
            qg.QIcon("bin/SORT.png"),
            qg.QIcon("bin/POST.png")
        ]

    @contextmanager
    def doResetModel(self):
        """Ensures PyQt begin/end reset model calls are made"""
        self.beginResetModel()
        yield
        self.endResetModel()

    def rowCount(self, parent):
        return len(self._ele_list)

    def data(self, mod_index, role=qc.Qt.DisplayRole):
        ret_val = None

        if mod_index.isValid() and mod_index.row() < len(self._ele_list):
            if role == qc.Qt.DisplayRole or role == qc.Qt.EditRole:
                ret_val = self._ele_list[mod_index.row()].name
            elif role == qc.Qt.DecorationRole:
                ret_val = self._decorations[
                    self._ele_list[mod_index.row()].stage_id]
            elif role == sc.ELEMENT_ROLE:
                ret_val = self._ele_list[mod_index.row()]

        return ret_val

    @property
    def ele_model(self):
        return self._ele_model

    @ele_model.setter
    def ele_model(self, ele_model):
        self._ele_model = ele_model

    def run(self):
        """TBD."""
        print("Pipeline Running")
        pass

    def clear(self):
        """TBD."""
        with self.doResetModel():
            self._ele_list.clear()
            self.ele_model.set_element(None)

    def delete(self, index):
        with self.doResetModel():
            self._ele_list.pop(index)
            self.ele_model.set_element(None)

    def add_element(self, new_ele):
        i = 0
        while (i < len(self._ele_list) and
                new_ele.stage_id >= self._ele_list[i].stage_id):
            i += 1
        self._ele_list.insert(i, new_ele)
        self.dataChanged.emit(qc.QModelIndex(), qc.QModelIndex())

    def move_up(self, i):
        ele_list = self._ele_list
        if i > 0 and ele_list[i].stage_id == ele_list[i-1].stage_id:
            with self.doResetModel():
                ele_list[i-1], ele_list[i] = ele_list[i], ele_list[i-1]
                self.ele_model.set_element(None)

    def move_down(self, i):
        ele_list = self._ele_list
        if (i < (len(ele_list) - 1) and
                ele_list[i].stage_id == ele_list[i+1].stage_id):
            with self.doResetModel():
                ele_list[i+1], ele_list[i] = ele_list[i], ele_list[i+1]
                self.ele_model.set_element(None)
