import pytest

from tests.collections_data import deep_args_data, is_iter_data, object_to_deep_collection_data
from nrt_collections_utils.collections_utils import CollectionsUtil


@pytest.mark.parametrize('args, expected_list', deep_args_data)
def test_deep_args_to_list(args, expected_list):
    assert CollectionsUtil.deep_args_to_list(args) == expected_list


@pytest.mark.parametrize('obj, is_iter', is_iter_data)
def test_is_iter(obj, is_iter):
    assert CollectionsUtil.is_iter(obj) == is_iter


@pytest.mark.parametrize(
    'obj, expected_deep_collection', object_to_deep_collection_data)
def test_object_to_deep_collection(obj, expected_deep_collection):
    assert CollectionsUtil.object_to_deep_collection(obj) == expected_deep_collection
