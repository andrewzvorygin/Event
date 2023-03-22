from application.utils.hashing import get_password_hash


def test_hash_password():
    password = 'qwerty123'
    assert password != get_password_hash(password)
