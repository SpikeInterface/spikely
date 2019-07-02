"""Class definition of SpikeElement.

Implements the SpikeInterface elements responsible extracellular data
processing.

"""

import PyQt5.QtCore as qc
import PyQt5.QtGui as qg
import PyQt5.QtWidgets as qw

from . import config as cfg


class SpikeElementModel(qc.QAbstractTableModel):
    """Model representation of pipeline elements"""

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
        '''Count of parameters associated with an element instance'''
        return 0 if self._element is None else len(self._element.params)

    def columnCount(self, parent=qc.QModelIndex()):
        '''Number of display columns in parameter table view'''
        return 3

    def flags(self, mod_index):
        '''Sets UI policy for columns in table view for element'''
        flags = qc.QAbstractTableModel.flags(self, mod_index)
        col = mod_index.column()
        if col == cfg.PARAM_COL or col == cfg.VTYPE_COL:
            flags ^= qc.Qt.ItemIsSelectable
        elif col == cfg.VALUE_COL:
            flags |= qc.Qt.ItemIsEditable
        return flags

    def data(self, mod_index, role=qc.Qt.DisplayRole):
        '''Returns data for one row/param and one col/field at a time'''
        col, row = mod_index.column(), mod_index.row()
        param_dict = self._element.params[row]
        result = qc.QVariant()

        if role == qc.Qt.DisplayRole or role == qc.Qt.EditRole:
            if col == cfg.PARAM_COL:
                result = param_dict['name']
            elif col == cfg.VTYPE_COL:
                result = param_dict['type']
            elif col == cfg.VALUE_COL:
                if 'value' in param_dict.keys():
                    result = str(param_dict['value']).strip()
                    if not result and 'default' in param_dict.keys():
                        result = str(param_dict['default'])

        elif role == qc.Qt.ToolTipRole:
            if col == cfg.PARAM_COL and 'title' in param_dict.keys():
                result = param_dict['title']

        elif role == qc.Qt.BackgroundRole:
            if col == cfg.VALUE_COL:
                if ('value' not in param_dict.keys() and
                        'default' not in param_dict.keys()):
                    result = qg.QBrush(qg.QColor(255, 192, 192))

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
        param_dict = self._element.params[row]
        success = True

        if role == qc.Qt.EditRole:
            '''
            This is a little tricky - if user enters valid value assign it to
            'value' in the param dictionary.  If user enters nothing assign
            'default' to 'value' if 'default' exists, otherwise delete 'value'
            from param dictionary.  Talk to Cole if you don't like this.
            '''
            if value.strip():
                success, cvt_value = self._convert_value(
                    param_dict['type'], value)
                if success:
                    param_dict['value'] = cvt_value
            else:
                if 'default' in param_dict.keys():
                    param_dict['value'] = param_dict['default']
                else:
                    param_dict.pop('value', None)

        return success

    def _convert_value(self, type_str, value):
        success, cvt_value = True, None
        try:
            if value == 'None':
                cvt_value = None
            elif type_str in ['str', 'path']:
                cvt_value = value
            elif type_str == 'int':
                cvt_value = int(value)
            elif type_str == 'float':
                cvt_value = float(value)
            elif type_str == 'bool':
                if value.lower() in ['true', 'yes']:
                    cvt_value = True
                elif value.lower() in ['false', 'no']:
                    cvt_value = False
                else:
                    raise TypeError(f'{value} is not a valid bool type')
            else:
                raise TypeError(f'{type_str} is not a Spikely supported type')
        except (TypeError, ValueError) as err:
            qw.QMessageBox.warning(
                cfg.main_window, 'Type Conversion Error', repr(err))
            success = False

        return success, cvt_value
