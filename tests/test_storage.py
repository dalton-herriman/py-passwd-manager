import pytest
import tempfile
import os
import shutil
from pm_core import storage
from pm_core.exceptions import StorageError

def temp_db_path():
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test.db")
    yield db_path
    shutil.rmtree(temp_dir)

@pytest.fixture
def db_path():
    yield from temp_db_path()

def test_sqlite_storage_set_get_delete_list(db_path):
    s = storage.SQLiteStorage(db_path)
    s.set("foo", "bar")
    assert s.get("foo") == "bar"
    s.set("baz", "qux")
    keys = s.list_keys()
    assert set(keys) >= {"foo", "baz"}
    s.delete("foo")
    assert s.get("foo") is None
    s.close()

def test_save_load_vault_file(db_path):
    storage.save_vault_file("vaultdata", "saltdata", db_path)
    vault, salt = storage.load_vault_file(db_path)
    assert vault == "vaultdata"
    assert salt == "saltdata"

def test_backup_restore_vault(db_path):
    storage.save_vault_file("vaultdata", "saltdata", db_path)
    backup_path = db_path + ".bak"
    assert storage.backup_vault(db_path, backup_path)
    assert os.path.exists(backup_path)
    # Overwrite original
    storage.save_vault_file("other", "salt2", db_path)
    assert storage.restore_vault(backup_path, db_path)
    vault, salt = storage.load_vault_file(db_path)
    assert vault == "vaultdata"
    assert salt == "saltdata"
    os.remove(backup_path)

def test_get_vault_info(db_path):
    info = storage.get_vault_info(db_path)
    assert not info["exists"]
    storage.save_vault_file("vaultdata", "saltdata", db_path)
    info = storage.get_vault_info(db_path)
    assert info["exists"]
    assert info["has_vault_data"]
    assert info["has_salt"]
    assert "size" in info
    assert "keys" in info

def test_load_vault_file_missing(db_path):
    # Should not raise
    vault, salt = storage.load_vault_file(db_path)
    assert vault is None and salt is None

def test_backup_vault_missing():
    with pytest.raises(StorageError):
        storage.backup_vault("/nonexistent/file", "/tmp/backup")

def test_restore_vault_missing():
    with pytest.raises(StorageError):
        storage.restore_vault("/nonexistent/backup", "/tmp/vault") 