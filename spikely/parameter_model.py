import re

import numpy as np
import PyQt5.QtCore as QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from . import config


# An MVC model representation of an element's parameters
class ParameterModel(QtCore.QAbstractTableModel):

    def __init__(self):
        self._element = None
        super().__init__()

    # Pythonic setters/getters
    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, element):
        # Ensures dependent views are signaled on element changes
        self.beginResetModel()
        self._element = element
        self.endResetModel()

    #
    # QAbstractTableModel Methods
    #

    # Count of parameters associated with an element instance
    def rowCount(self, parent=QtCore.QModelIndex()):
        return 0 if self._element is None else len(self._element.param_list)

    # Number of display columns: Parameter, Type, Value
    def columnCount(self, parent=QtCore.QModelIndex()):
        return 3

    # Sets UI policy for columns in table view for element parameters
    def flags(self, mod_index):
        column_flags = QtCore.QAbstractTableModel.flags(self, mod_index)
        col = mod_index.column()

        # Parameter and Type column cells are read only
        if col == config.PARAM_COL or col == config.TYPE_COL:
            column_flags ^= QtCore.Qt.ItemIsSelectable
        elif col == config.VALUE_COL:
            column_flags |= QtCore.Qt.ItemIsEditable
        return column_flags

    # Called by Views, get element parameter data based on index and role
    def data(self, mod_index, role=QtCore.Qt.DisplayRole):
        col, row = mod_index.column(), mod_index.row()
        param_dict = self._element.param_list[row]

        # If no actual result return empty value indicator
        result = QtCore.QVariant()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if col == config.PARAM_COL:
                result = param_dict['name']
            elif col == config.TYPE_COL:
                result = param_dict['type']
            elif col == config.VALUE_COL:
                if 'value' in param_dict.keys():
                    result = str(param_dict['value']).strip()
                    if not result and 'default' in param_dict.keys():
                        result = str(param_dict['default'])

        elif role == QtCore.Qt.ToolTipRole:
            if col == config.PARAM_COL and 'title' in param_dict.keys():
                result = param_dict['title']
            elif col == config.TYPE_COL:
                type_str = param_dict['type']
                if type_str == 'int':
                    result = 'integer'
                elif type_str == 'float':
                    result = 'floating point'
                elif type_str == 'bool':
                    result = 'boolean'
                elif type_str == 'int_list':
                    result = 'list of integers'
                elif type_str == 'str':
                    result = 'text string'
                elif type_str == 'file':
                    result = 'pathname of file'
                elif type_str == 'folder':
                    result = 'pathname of folder'
                elif type_str == 'file_or_folder':
                    result = 'pathname of file or folder'
                elif type_str == 'int_list_list':
                    result = 'list of a int_lists'
                elif type_str == 'dtype':
                    result = 'numpy dtype object (e.g., int32)'

        # Paints cell red if mandatory parameter value is missing.
        # Mandatory parameters are those with no default keys
        elif role == QtCore.Qt.BackgroundRole:
            if col == config.VALUE_COL:
                if ('value' not in param_dict.keys() and
                        'default' not in param_dict.keys()):
                    result = QtGui.QBrush(QtGui.QColor(255, 192, 192))

        return result

    def headerData(self, section, orientation, role):
        result = QtCore.QVariant()
        if (orientation == QtCore.Qt.Horizontal and
                (role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole)):
            result = ['Parameter', 'Type', 'Value'][section]

        return result

    # Called after user edits parameter value to keep model in sync
    def setData(self, mod_index, value, role=QtCore.Qt.EditRole):
        row = mod_index.row()
        param_dict = self._element.param_list[row]
        success = True

        # This is a little tricky - if user enters valid value assign it to
        # 'value' in the param dictionary.  If user enters nothing assign
        # 'default' to 'value' if 'default' exists, otherwise delete 'value'
        # from param dictionary.  Talk to Cole if you don't like this.
        if role == QtCore.Qt.EditRole:
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

    #
    # Helper Methods
    #

    def _convert_value(self, type_str, value):
        success, cvt_value = True, None
        try:
            if value == 'None':
                cvt_value = None

            elif type_str in ['str', 'file', 'folder', 'file_or_folder']:
                cvt_value = value

            elif type_str == 'int':
                if value == 'inf':
                    cvt_value = float(value)
                else:
                    cvt_value = int(value)

            elif type_str == 'float':
                cvt_value = float(value)

            elif type_str == 'int_list':
                cvt_value = self._str_list_to_int_list(value)

            elif type_str == 'int_list_list':
                # Strip outer sq brackets: '[[1,2],[3,4]]' -> '[1,2],[3,4]'
                value = re.sub(r'^\[|\]$', '', value)
                # Disambiguate list separator: '[1,2],[3,4]' -> [1,2]:[3,4]'
                value = re.sub(r'\] *, *\[', ':', value)
                # Split into int_list strings and convert into int_lists
                cvt_value = list(map(
                    self._str_list_to_int_list, value.split(':')))

            elif type_str == 'bool':
                if value.lower() in ['true', 'yes']:
                    cvt_value = True
                elif value.lower() in ['false', 'no']:
                    cvt_value = False
                else:
                    raise TypeError(f'{value} is not a valid bool type')

            elif type_str == 'dtype':
                cvt_value = np.dtype(value)

            else:
                raise TypeError(f'{type_str} is not a Spikely supported type')

        except (TypeError, ValueError) as err:
            QtWidgets.QMessageBox.warning(
                config.find_main_window(), 'Type Conversion Error', repr(err))
            success = False

        return success, cvt_value

    # E.g., '[1,2,3]' -> [1,2,3]
    def _str_list_to_int_list(self, str_list):
        # Set up split by stripping square brackets
        str_list = re.sub(r'^\[|\]$', '', str_list)
        # Convert list of string ints into actual ints
        return list(map(int, str_list.split(',')))
