import json

import pkg_resources
from PyQt5 import QtCore, QtWidgets

from . import config
from .elements import spike_element as sp_spe
from .elements import std_element_policy as sp_ste


class PipelineModel(QtCore.QAbstractListModel):

    def __init__(self, parameter_model):
        super().__init__()

        self._element_list = []
        self._element_policy = sp_ste.StdElementPolicy()
        self._parameter_model = parameter_model

    def _elem_cls_count(self, target_cls):
        elem_cls_list = [type(elem) for elem in self._element_list]
        return elem_cls_list.count(target_cls)

    def rowCount(self, parent=None):
        # Overrides base class: provides count of elements in pipeline
        return len(self._element_list)

    def data(self, mod_index, role=QtCore.Qt.DisplayRole):
        # Overrides base class: returns data for element in pipeline for role
        if mod_index.isValid() and mod_index.row() < len(self._element_list):
            element = self._element_list[mod_index.row()]
            data_dict = {
                QtCore.Qt.DisplayRole:      element.display_name,
                QtCore.Qt.EditRole:         element.display_name,
                QtCore.Qt.DecorationRole:   element.display_icon,
                config.ELEMENT_ROLE:    element}
            return data_dict.get(role)

    def run(self):
        # Called in response to user pressing Run button in UI
        missing_param_count = self._missing_param_count()
        if missing_param_count:
            QtWidgets.QMessageBox.warning(
                config.find_main_window(), 'Run Failure',
                f'Missing mandatory element parameters.  Missing parameter '
                f'count: {missing_param_count}')
            return

        for cls in self._element_policy.required_cls_list:
            if not self._elem_cls_count(cls):
                QtWidgets.QMessageBox.warning(
                    config.find_main_window(), 'Run Failure',
                    f'Missing required element: {cls.__name__}')
                return

        config.find_main_window().statusBar().showMessage(
            'Running pipeline', config.STATUS_MSG_TIMEOUT)

        elem_jdict_list = [config.cvt_elem_to_dict(element)
                           for element in self._element_list]

        elem_list_str = json.dumps(elem_jdict_list)
        pipeman_path = pkg_resources.resource_filename(
            'spikely.pipeman', 'pipeman.py')

        run_process = QtCore.QProcess()
        success = run_process.startDetached(
            'python', [f'{pipeman_path}', elem_list_str])
        if not success:
            QtWidgets.QMessageBox.warning(
                config.find_main_window(), 'Failed to Start Python Process',
                f'Command line: python {pipeman_path}, elem_list_str')

    def clear(self):
        self.beginResetModel()
        self._element_list.clear()
        self.endResetModel()
        # Synchronize parameter model and view
        self._parameter_model.element = None

    def add_element(self, new_elem: sp_spe.SpikeElement) -> None:
        # Inserts new element into  pipeline in proper order

        new_elem_cls_count = self._elem_cls_count(new_elem.__class__)
        new_elem_is_singleton = self._element_policy.\
            is_cls_singleton(new_elem.__class__)
        if new_elem_is_singleton and new_elem_cls_count:
            config.find_main_window().statusBar().showMessage(
                'Only one element of this type allowed in pipeline',
                config.STATUS_MSG_TIMEOUT)
            return

        target_positions = self._element_policy.cls_order_dict
        new_elem_target_pos = target_positions[new_elem.__class__]
        new_elem_insert_pos = 0
        for pipe_elem in self._element_list:
            pipe_elem_target_pos = target_positions[pipe_elem.__class__]
            if new_elem_target_pos >= pipe_elem_target_pos:
                new_elem_insert_pos += 1
            else:
                break

        self.beginInsertRows(QtCore.QModelIndex(), new_elem_insert_pos,
                             new_elem_insert_pos)
        self._element_list.insert(new_elem_insert_pos, new_elem)
        self.endInsertRows()

    # TODO: Clean this up in line w/ add_element method
    def move_up(self, elem: sp_spe.SpikeElement) -> None:
        rank = self._element_policy.cls_order_dict
        row = self._element_list.index(elem)

        if row > 0 and rank[type(elem)] == \
                rank[type(self._element_list[row - 1])]:
            self.beginMoveRows(QtCore.QModelIndex(), row,
                row, QtCore.QModelIndex(), row - 1)  # noqa: E128
            self._swap(self._element_list, row, row - 1)
            self.endMoveRows()
        else:
            config.find_main_window().statusBar().showMessage(
                "Cannot move element any higher", config.STATUS_MSG_TIMEOUT)

    # TODO: Clean this up in line w/ add_element method
    def move_down(self, elem: sp_spe.SpikeElement) -> None:
        rank = self._element_policy.cls_order_dict
        row = self._element_list.index(elem)

        if row < len(self._element_list) - 1 and \
                rank[type(elem)] == rank[type(self._element_list[row + 1])]:
            self.beginMoveRows(QtCore.QModelIndex(), row + 1,
                row + 1, QtCore.QModelIndex(), row)   # noqa: E128
            self._swap(self._element_list, row, row + 1)
            self.endMoveRows()
        else:
            config.find_main_window().statusBar().showMessage(
                "Cannot move element any lower", config.STATUS_MSG_TIMEOUT)

    def delete(self, element: sp_spe.SpikeElement) -> None:
        index = self._element_list.index(element)
        self.beginRemoveRows(QtCore.QModelIndex(), index, index)
        self._element_list.pop(index)
        self.endRemoveRows()

    # Helper methods

    def _swap(self, list, pos1, pos2):
        list[pos1], list[pos2] = list[pos2], list[pos1]

    def _missing_param_count(self) -> int:
        missing_param_list = [param for elem in self._element_list for param in
                              elem.param_list if 'value' not in param.keys()]
        return len(missing_param_list)
