import pytest
from framework.core.common import chunkify


@pytest.fixture(params=[1, 3, 10, 5000])
def chunk_size(request):
    return request.param


@pytest.fixture(params=[1, 2, 3, 5, 8, 13, 21])
def chunk_input(request):
    import string
    return string.ascii_letters * request.param


def test_chunk_strings(chunk_input, chunk_size):
    reassembled = ''
    for i in chunkify(chunk_input, chunk_size):
        assert len(i) <= chunk_size
        reassembled += i
    assert reassembled == chunk_input


def test_chunk_lists(chunk_size, chunk_input):
    s = list(chunk_input)
    reassembled = []
    for i in chunkify(s, chunk_size):
        assert len(i) <= chunk_size
        reassembled += i
    assert reassembled == s


def test_random_id_is_uuid():
    from framework.core.common import generate_random_id
    import uuid
    assert uuid.UUID(generate_random_id())


@pytest.mark.parametrize("test_input,expected",
                         [(['1', 2, '3'], 'cc209c79-020c-f993-5f78-e1a40d97b6a6'),
                          (12, 'c20ad4d7-6fe9-7759-aa27-a0c99bff6710'),
                          (dict(a=1), '42b7b4f2-9217-88ea-14da-c5566e6f06d0')])
def test_hash_id_is_uuid(test_input, expected):
    from framework.core.common import generate_hash_id
    import uuid
    hash_id = generate_hash_id(test_input)
    assert uuid.UUID(hash_id)
    assert hash_id == expected
