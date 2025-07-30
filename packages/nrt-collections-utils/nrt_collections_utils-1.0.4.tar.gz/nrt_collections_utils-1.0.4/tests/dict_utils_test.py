import pytest
from tests.dict_utils_data import get_value_data
from nrt_collections_utils.dict_utils import DictUtil


@pytest.mark.parametrize('obj, path, default_value, expected_result', get_value_data)
def test_get_value(obj, path, default_value, expected_result):
    assert DictUtil.get_value(obj, path, default_value) == expected_result
