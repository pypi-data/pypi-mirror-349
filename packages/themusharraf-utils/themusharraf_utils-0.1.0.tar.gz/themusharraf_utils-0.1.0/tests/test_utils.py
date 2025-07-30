from src.themusharraf_utils.utils import slugify, chunk_list, is_valid_email

def test_slugify():
    assert slugify("Salom Dunyo!") == "salom-dunyo" # noqa

def test_chunk_list():
    assert chunk_list([1,2,3,4], 2) == [[1,2],[3,4]]

def test_is_valid_email():
    assert is_valid_email("test@example.com")
    assert not is_valid_email("wrong-email@")
