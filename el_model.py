"""Class definition of SpikeElement.

Implements the SpikeInterface elements responsible extracellular data
processing.
"""

import PyQt5.QtCore as qc

import spikely_core as sc


class SpikeElementModel(qc.QAbstractTableModel):
    """TBD"""

    def __init__(self):
        self._element = None
        super().__init__()

    def set_element(self, element):
        self.beginResetModel()
        self._element = element
        self.endResetModel()

    def rowCount(self, parent=qc.QModelIndex()):
        ret_val = 0
        if self._element is not None:
            ret_val = len(self._element.props)
        return ret_val

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

        ret_val = qc.QVariant()
        if role == qc.Qt.DisplayRole or role == qc.Qt.EditRole:
            if col == 0:
                ret_val = list(self._element.props.keys())[row]
            elif col == 1:
                ret_val = list(self._element.props.values())[row]

        return ret_val

    def headerData(self, section, orientation, role):
        ret_val = qc.QVariant()
        if (orientation == qc.Qt.Horizontal and
                (role == qc.Qt.DisplayRole or role == qc.Qt.EditRole)):
            ret_val = ['Property', 'Value'][section]

        return ret_val


class SpikeElement:
    """TBD."""

    _avail_elements = []
    _proto_elements = [
        (sc.EXTRACT, "Extractor A", {
            'Extractor A1 Name': 'Extractor A1 Value',
            'Extractor A2 Name': 'Extractor A2 Value'
        }),
        (sc.EXTRACT, "Extractor B", {
            'Extractor B1 Name': 'Extractor B1 Value',
            'Extractor B2 Name': 'Extractor B2 Value'
        }),
        (sc.PREPROC, "Pre-Processor A", {
            'Pre-Processor A1 Name': 'Pre-Processor A1 Value',
            'Pre-Processor A2 Name': 'Pre-Processor A2 Value'
        }),
        (sc.PREPROC, "Pre-Processor B", {
            'Pre-Processor B1 Name': 'Pre-Processor B1 Value',
            'Pre-Processor B2 Name': 'Pre-Processor B2 Value'
        }),
        (sc.SORTING, "Sorter A", {
            'Sorter A1 Name': 'Sorter A1 Value',
            'Sorter A2 Name': 'Sorter A2 Value'
        }),
        (sc.SORTING, "Sorter B", {
            'Sorter B1 Name': 'Sorter B1 Value',
            'Sorter B2 Name': 'Sorter B2 Value'
        }),
        (sc.POSTPROC, "Post-Processor A", {
            'Post-Processor A1 Name': 'Post-Processor A1 Value',
            'Post-Processor A2 Name': 'Post-Processor A2 Value'
        }),
        (sc.POSTPROC, "Post-Processor B", {
            'Post-Processor B1 Name': 'Post-Processor B1 Value',
            'Post-Processor B2 Name': 'Post-Processor B2 Value'
        })
    ]

    @classmethod
    def avail_elements(cls):
        """TBD."""
        if len(cls._avail_elements) == 0:
            cls._fill_elements()
        return cls._avail_elements

    @classmethod
    def _fill_elements(cls):
        for proto in cls._proto_elements:
            stage_id, name, props = proto
            ele = SpikeElement()
            ele.stage_id = stage_id
            ele.name = name
            ele.props = props
            cls._avail_elements.append(ele)

    def __init__(self):
        """TBD."""
        self._stage_id = None
        self._name = None
        self._props = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def stage_id(self):
        return self._stage_id

    @stage_id.setter
    def stage_id(self, stage_id):
        self._stage_id = stage_id

    @property
    def props(self):
        return self._props

    @props.setter
    def props(self, props):
        self._props = props

    def __repr__(self):
        return self._name
