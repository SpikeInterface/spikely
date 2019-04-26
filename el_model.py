"""Class definition of SpikeElement.

Implements the SpikeInterface elements responsible extracellular data
processing.
"""

import copy

import PyQt5.QtCore as qc

import config


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
        return 0 if self._element is None else len(self._element.props)

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
                result = list(self._element.props.keys())[row]
            elif col == 1:
                result = list(self._element.props.values())[row]

        return result

    def headerData(self, section, orientation, role):
        result = qc.QVariant()
        if (orientation == qc.Qt.Horizontal and
                (role == qc.Qt.DisplayRole or role == qc.Qt.EditRole)):
            result = ['Property', 'Value'][section]

        return result


class SpikeElement:
    """Base class for SpikeInterface elements"""

    _avail_elements = []
    _proto_elements = [
        (config.EXTRACTOR, "Extractor A", {
            'Extractor A1 Name': 'Extractor A1 Value',
            'Extractor A2 Name': 'Extractor A2 Value'
        }),
        (config.EXTRACTOR, "Extractor B", {
            'Extractor B1 Name': 'Extractor B1 Value',
            'Extractor B2 Name': 'Extractor B2 Value'
        }),
        (config.PRE_PROCESSOR, "Pre-Processor A", {
            'Pre-Processor A1 Name': 'Pre-Processor A1 Value',
            'Pre-Processor A2 Name': 'Pre-Processor A2 Value'
        }),
        (config.PRE_PROCESSOR, "Pre-Processor B", {
            'Pre-Processor B1 Name': 'Pre-Processor B1 Value',
            'Pre-Processor B2 Name': 'Pre-Processor B2 Value'
        }),
        (config.SORTER, "Sorter A", {
            'Sorter A1 Name': 'Sorter A1 Value',
            'Sorter A2 Name': 'Sorter A2 Value'
        }),
        (config.SORTER, "Sorter B", {
            'Sorter B1 Name': 'Sorter B1 Value',
            'Sorter B2 Name': 'Sorter B2 Value'
        }),
        (config.POST_PROCESSOR, "Post-Processor A", {
            'Post-Processor A1 Name': 'Post-Processor A1 Value',
            'Post-Processor A2 Name': 'Post-Processor A2 Value'
        }),
        (config.POST_PROCESSOR, "Post-Processor B", {
            'Post-Processor B1 Name': 'Post-Processor B1 Value',
            'Post-Processor B2 Name': 'Post-Processor B2 Value'
        })
    ]

    @classmethod
    def available_elements(cls):
        """TBD."""
        if not cls._avail_elements:
            cls._fill_elements()
        return cls._avail_elements

    @classmethod
    def _fill_elements(cls):
        for proto in cls._proto_elements:
            type, name, props = proto
            element = SpikeElement()
            element.type = type
            element.name = name
            element.props = props
            cls._avail_elements.append(element)

    def __init__(self, element=None):
        """TBD."""
        if element is None:
            self._type = None
            self._name = None
        else:
            self._type = element.type
            self._name = element.name
            self._props = copy.deepcopy(element.props)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def props(self):
        return self._props

    @props.setter
    def props(self, props):
        self._props = props

    def __repr__(self):
        return self._name
