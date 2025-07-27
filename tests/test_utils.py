import pytest
import string
from pm_core import utils
import sys

@pytest.mark.parametrize("length,include_symbols,include_numbers,include_uppercase", [
    (16, True, True, True),
    (12, False, True, True),
    (10, True, False, True),
    (8, True, True, False),
])
def test_generate_password_various(length, include_symbols, include_numbers, include_uppercase):
    pw = utils.generate_password(length, include_symbols, include_numbers, include_uppercase)
    assert len(pw) == length
    if include_symbols:
        assert any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in pw)
    if include_numbers:
        assert any(c.isdigit() for c in pw)
    if include_uppercase:
        assert any(c.isupper() for c in pw)
    assert all(c in (string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?") for c in pw)

def test_generate_password_no_charset():
    with pytest.raises(ValueError):
        utils.generate_password(10, False, False, False)

def test_validate_password_strength():
    weak = utils.validate_password_strength("123")
    assert weak['strength'] == 'weak'
    strong = utils.validate_password_strength("GoodPass123!")
    assert strong['strength'] in ('medium', 'strong')
    assert 'score' in strong
    assert 'feedback' in strong

def test_get_system_info():
    info = utils.get_system_info()
    assert 'platform' in info
    assert 'python_version' in info
    assert 'architecture' in info

def test_wipe_memory_str():
    # Just ensure no exception is raised
    s = "sensitive"
    utils.wipe_memory(s)

def test_wipe_memory_bytes():
    b = b"sensitive"
    utils.wipe_memory(b)

def test_wipe_memory_list():
    l = ["a", b"b", [1,2,3]]
    utils.wipe_memory(l)

def test_clipboard_handler_success(monkeypatch):
    class DummyPyperclip:
        @staticmethod
        def copy(text):
            DummyPyperclip.last = text
    monkeypatch.setitem(sys.modules, 'pyperclip', DummyPyperclip)
    assert utils.clipboard_handler("secret", timeout=0)
    assert DummyPyperclip.last == "secret"

def test_clipboard_handler_importerror(monkeypatch):
    monkeypatch.setitem(sys.modules, 'pyperclip', None)
    # Should fallback and not raise
    try:
        utils.clipboard_handler("secret", timeout=0)
    except Exception as e:
        pytest.fail(f"clipboard_handler raised: {e}") 