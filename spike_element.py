import config
import copy


class SpikeElement:
    """Base class for SpikeInterface elements"""

    _available_elements = []

    @classmethod
    def available_elements(cls):
        """Returns registry of available elements as a class method"""
        if not cls._available_elements:
            # TBD: Replace this with real element registry
            _create_dummy_elements(cls._available_elements)
        return cls._available_elements

    def __init__(self, element=None):
        """To support multi instancing, makes deep copy of template element"""
        if element is None:
            self._type = None
            self._name = None
            self._props = None
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

    def __str__(self):
        return self._name


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


def _create_dummy_elements(elements):
    for proto in _proto_elements:
        type, name, props = proto
        element = SpikeElement()
        element.type = type
        element.name = name
        element.props = props
        elements.append(element)
