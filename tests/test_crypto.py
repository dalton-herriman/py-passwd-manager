import pytest
from pm_core import crypto
from pm_core.exceptions import CryptoError


def test_generate_salt_uniqueness():
    s1 = crypto.generate_salt()
    s2 = crypto.generate_salt()
    assert s1 != s2
    assert len(s1) >= 16


def test_apply_salt():
    s = crypto.apply_salt("foo")
    salt, val = s.split(":", 1)
    assert val == "foo"
    assert len(salt) >= 16


def test_apply_hash_argon2():
    h = crypto.apply_hash_argon2("password")
    assert isinstance(h, str)
    assert "password" not in h


def test_derive_key_deterministic():
    valid_salt = "12345678"  # 8 bytes
    k1 = crypto.derive_key("pw", valid_salt)
    k2 = crypto.derive_key("pw", valid_salt)
    assert k1 == k2
    assert isinstance(k1, bytes)
    assert len(k1) == 32


def test_encrypt_decrypt_roundtrip():
    pw = "masterpw"
    salt = crypto.generate_salt()
    data = "secret data"
    enc = crypto.encrypt_data(data, pw, salt)
    dec = crypto.decrypt_data(enc, pw, salt)
    assert dec == data


def test_encrypt_data_bytes():
    pw = "masterpw"
    salt = crypto.generate_salt()
    data = b"bytes data"
    enc = crypto.encrypt_data(data, pw, salt)
    dec = crypto.decrypt_data(enc, pw, salt)
    assert dec == "bytes data"


def test_decrypt_data_bad_key():
    pw = "masterpw"
    salt = crypto.generate_salt()
    data = "secret data"
    enc = crypto.encrypt_data(data, pw, salt)
    with pytest.raises(CryptoError):
        crypto.decrypt_data(enc, "wrongpw", salt)
