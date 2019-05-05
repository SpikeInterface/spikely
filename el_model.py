"""Class definition of SpikeElement.

Implements the SpikeInterface elements responsible extracellular data
processing.
"""

import PyQt5.QtCore as qc


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
                result = list(self._element.params.keys())[row]
            elif col == 1:
                result = list(self._element.params.values())[row]

        return result

    def headerData(self, section, orientation, role):
        result = qc.QVariant()
        if (orientation == qc.Qt.Horizontal and
                (role == qc.Qt.DisplayRole or role == qc.Qt.EditRole)):
            result = ['Property', 'Value'][section]

        return result
