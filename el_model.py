"""Class definition of SpikeElement.

Implements the SpikeInterface elements responsible extracellular data
processing.

name output_folder
type str
value None
default None
title Sorting output folder path
"""

import PyQt5.QtCore as qc
import PyQt5.QtGui as qg

import config

# from pydoc import locate


class SpikeElementModel(qc.QAbstractTableModel):
    """TBD"""

    def __init__(self):
        self._element = None
        super().__init__()

    # Pythonic setters/getters
    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, element):
        '''Ensures views are signaled on element changes'''
        self.beginResetModel()
        self._element = element
        self.endResetModel()

    # Methods sub-classed from QAbstractTableModel
    def rowCount(self, parent=qc.QModelIndex()):
        '''One element parameter per table view row'''
        return 0 if self._element is None else len(self._element.params)

    def columnCount(self, parent=qc.QModelIndex()):
        '''Number of display columns in parameter table view'''
        return 3

    def flags(self, mod_index):
        '''Sets UI policy for columns in table view'''
        flags = qc.QAbstractTableModel.flags(self, mod_index)
        col = mod_index.column()

        if col == config.PARAM_COL or col == config.VTYPE_COL:
            flags ^= qc.Qt.ItemIsSelectable
        elif col == config.VALUE_COL:
            flags |= qc.Qt.ItemIsEditable
        return flags

    def data(self, mod_index, role=qc.Qt.DisplayRole):
        '''Returns data for one row/param and one col/field at a time'''
        col, row = mod_index.column(), mod_index.row()
        param_dict = self._element.params[row]
        result = qc.QVariant()

        if role == qc.Qt.DisplayRole or role == qc.Qt.EditRole:
            if col == config.PARAM_COL:
                result = param_dict['name']
            elif col == config.VTYPE_COL:
                result = param_dict['type']
            elif col == config.VALUE_COL:
                if 'value' in param_dict.keys():
                    result = str(param_dict['value']).strip()
                    if not result and 'default' in param_dict.keys():
                        result = str(param_dict['default'])

        elif role == qc.Qt.ToolTipRole:
            if col == config.PARAM_COL and 'title' in param_dict.keys():
                result = param_dict['title']

        elif role == qc.Qt.BackgroundRole:
            """
            for v, k in self._element.params[row].items():
                print(v, k)
            """

            if col == config.VALUE_COL:
                if 'value' in param_dict.keys():

                    value = param_dict['value']
                    value_type = param_dict['type']

                    if value is None:
                        result = qg.QBrush(qg.QColor(255, 128, 128))
                    elif ((value_type == 'str' or value_type == 'path')
                            and not value.strip()):
                        result = qg.QBrush(qg.QColor(255, 128, 128))
                else:
                    result = qg.QBrush(qg.QColor(255, 128, 128))

        return result

    def headerData(self, section, orientation, role):
        '''Sets properties for column headers in table view'''
        result = qc.QVariant()
        if (orientation == qc.Qt.Horizontal and
                (role == qc.Qt.DisplayRole or role == qc.Qt.EditRole)):
            result = ['Parameter', 'Type', 'Value'][section]

        return result

    def setData(self, mod_index, value, role=qc.Qt.EditRole):
        '''Takes data from table view and passes it to model'''
        row = mod_index.row()
        result = False
        if role == qc.Qt.EditRole:
            self._element.params[row]['value'] = value
            result = True
        return result
