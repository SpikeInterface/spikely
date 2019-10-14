import pytest
from spikely.parameter_model import ParameterModel


@pytest.mark.parametrize(
    'type_str, value, expected_cvt_value',
    [('', 'None', None),
     ('str', 'Test', 'Test'),
     ('int_list_list', '[[0,1],[2,3]]', [[0, 1], [2, 3]]),
     ])
def test_convert_value(type_str, value, expected_cvt_value):
    pm = ParameterModel()
    success, cvt_value = pm._convert_value(type_str, value)

    assert success
    assert cvt_value == expected_cvt_value
