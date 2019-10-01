import multiprocessing as mp

import PyQt5.QtCore as qc
import PyQt5.QtWidgets as qw

from . import config
from .elements import spike_element as sp_spe
from .elements import std_element_policy as sp_ste
import json


class PipelineModel(qc.QAbstractListModel):

    def __init__(self, parameter_model):
        super().__init__()

        self._elements = []
        self._element_policy = sp_ste.StdElementPolicy()
        self._parameter_model = parameter_model

    def _elem_cls_count(self, target_cls):
        elem_cls_list = [type(elem) for elem in self._elements]
        return elem_cls_list.count(target_cls)

    def rowCount(self, parent=None):
        # Subclassed from base: Count of elements in model

        return len(self._elements)

    def data(self, mod_index, role=qc.Qt.DisplayRole):
        # Subclassed from base: Returns role specific data from elem at index

        if mod_index.isValid() and mod_index.row() < len(self._elements):
            element = self._elements[mod_index.row()]
            data_dict = {
                qc.Qt.DisplayRole:      element.display_name,
                qc.Qt.EditRole:         element.display_name,
                qc.Qt.DecorationRole:   element.display_icon,
                config.ELEMENT_ROLE:    element}

        return None if not data_dict else data_dict.get(role)

    # Methods called by app to manipulate and operate pipeline

    def run(self):
        bad_param_count = self._bad_param_count()
        if bad_param_count:
            qw.QMessageBox.warning(
                config.find_main_window(), 'Run Failure',
                f'Missing mandatory element parameters.  Missing parameter '
                f'count: {bad_param_count}')
            return

        for cls in self._element_policy.required_cls_list:
            if not self._elem_cls_count(cls):
                qw.QMessageBox.warning(
                    config.find_main_window(), 'Run Failure',
                    f'Missing required element: {cls.__name__}')
                return

        config.find_main_window().statusBar().showMessage(
            'Running pipeline', config.STATUS_MSG_TIMEOUT)

        elem_jdict_list = [config.cvt_elem_to_dict(element)
                           for element in self._elements]

        elem_list_str = json.dumps(elem_jdict_list)

        p = mp.Process(target=config.async_run, args=[elem_list_str])
        p.start()

    def clear(self):
        self.beginResetModel()
        self._elements.clear()
        self.endResetModel()
        # Synchronize parameter model and view
        self._parameter_model.element = None

    def add_element(self, add_elem: sp_spe.SpikeElement) -> None:
        add_cls = type(add_elem)
        if self._element_policy.is_cls_singleton(add_cls) \
                and self._elem_cls_count(add_cls):
            config.find_main_window().statusBar().showMessage(
                'Only one element of that type allowed in pipeline',
                config.STATUS_MSG_TIMEOUT)
            return

        rank = self._element_policy.cls_order_dict
        add_row = 0
        while add_row < len(self._elements) \
                and rank[type(add_elem)] > rank[type(self._elements[add_row])]:
            add_row += 1

        self.beginInsertRows(qc.QModelIndex(), add_row, add_row)
        self._elements.insert(add_row, add_elem)
        self.endInsertRows()

    def move_up(self, elem: sp_spe.SpikeElement) -> None:
        rank = self._element_policy.cls_order_dict
        row = self._elements.index(elem)

        if row > 0 and rank[type(elem)] == rank[type(self._elements[row - 1])]:
            self.beginMoveRows(qc.QModelIndex(), row,
                row, qc.QModelIndex(), row - 1)  # noqa: E128
            self._swap(self._elements, row, row - 1)
            self.endMoveRows()
        else:
            config.find_main_window().statusBar().showMessage(
                "Cannot move element any higher", config.STATUS_MSG_TIMEOUT)

    def move_down(self, elem: sp_spe.SpikeElement) -> None:
        rank = self._element_policy.cls_order_dict
        row = self._elements.index(elem)

        if row < len(self._elements) - 1 and \
                rank[type(elem)] == rank[type(self._elements[row + 1])]:
            self.beginMoveRows(qc.QModelIndex(), row + 1,
                row + 1, qc.QModelIndex(), row)   # noqa: E128
            self._swap(self._elements, row, row + 1)
            self.endMoveRows()
        else:
            config.find_main_window().statusBar().showMessage(
                "Cannot move element any lower", config.STATUS_MSG_TIMEOUT)

    def delete(self, element: sp_spe.SpikeElement) -> None:
        index = self._elements.index(element)
        self.beginRemoveRows(qc.QModelIndex(), index, index)
        self._elements.pop(index)
        self.endRemoveRows()

    # Helper methods

    def _swap(self, list, pos1, pos2):
        list[pos1], list[pos2] = list[pos2], list[pos1]

    def _bad_param_count(self) -> int:
        bad_list = [param for elem in self._elements for param in
                    elem.param_list if 'value' not in param.keys()]
        return len(bad_list)
