"""Class definition of SpikeElement.

Implements the SpikeInterface elements responsible extracellular data
processing.
"""

import PyQt5.QtCore as qc
from pydoc import locate


class SpikeElementModel(qc.QAbstractTableModel):
    """TBD"""

    def __init__(self):
        self._element = None
        super().__init__()

    # Pythonic approach to setters/getters
    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, element):
        self.beginResetModel()
        self._element = element
        self.endResetModel()

    # Methods sub-classed from QAbstractTableModel
    def rowCount(self, parent=qc.QModelIndex()):
        return 0 if self._element is None else len(self._element.params)

    def columnCount(self, parent=qc.QModelIndex()):
        return 2

    def flags(self, mod_index):
        flags = qc.QAbstractTableModel.flags(self, mod_index)
        if mod_index.column() == 0:
            flags ^= qc.Qt.ItemIsSelectable
        elif mod_index.column() == 1:
            flags |= qc.Qt.ItemIsEditable
        return flags

    def data(self, mod_index, role=qc.Qt.DisplayRole):
        col, row = mod_index.column(), mod_index.row()
        result = qc.QVariant()
        if role == qc.Qt.DisplayRole or role == qc.Qt.EditRole:
            if col == 0:
                result = self._element.params[row]['name']
            elif col == 1:
                if 'value' in self._element.params[row].keys():
                    result = self._element.params[row]['value']
                else:
                    value_type = locate(self._element.params[row]['type'])
                    if value_type is int:
                        result = -10
                    elif value_type is float:
                        result = -10.0
                    elif value_type is bool:
                        result = False
                    elif value_type is str:
                        result = ''
                    else:
                        result = 'Unknown Type'

        return result

    def headerData(self, section, orientation, role):
        result = qc.QVariant()
        if (orientation == qc.Qt.Horizontal and
                (role == qc.Qt.DisplayRole or role == qc.Qt.EditRole)):
            result = ['Parameter', 'Value'][section]

        return result

    def setData(self, mod_index, value, role=qc.Qt.EditRole):
        row = mod_index.row()
        result = False
        if role == qc.Qt.EditRole:
            self._element.params[row]['value'] = value
            result = True
        return result
