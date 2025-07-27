import pytest
from pm_core.models import Entry, Vault, Config
from datetime import datetime, timezone

def test_entry_update():
    e = Entry(id=1, name="Service", username="u", password="p")
    old_updated = e.updated_at
    e.update(username="newu", password="newp")
    assert e.username == "newu"
    assert e.password == "newp"
    assert e.updated_at > old_updated

def test_vault_add_remove_get_update_entry():
    v = Vault(owner="me")
    e1 = Entry(id=1, name="A")
    e2 = Entry(id=2, name="B")
    v.add_entry(e1)
    v.add_entry(e2)
    assert len(v.entries) == 2
    assert v.get_entry(1) == e1
    assert v.get_entry(2) == e2
    v.remove_entry(1)
    assert v.get_entry(1) is None
    assert len(v.entries) == 1
    v.update_entry(2, name="BB", notes="note")
    assert v.get_entry(2).name == "BB"
    assert v.get_entry(2).notes == "note"

def test_vault_metadata():
    v = Vault(owner="me")
    assert v.owner == "me"
    assert isinstance(v.created_at, datetime)
    assert isinstance(v.updated_at, datetime)
    assert v.version == 1
    assert v.notes is None

def test_config_defaults():
    c = Config()
    assert c.db_path == "pm_data.db"
    assert c.encryption_enabled is True
    assert c.default_vault_path is None
    assert c.autosave is True
    assert c.theme is None
    assert c.last_opened is None
    assert c.backup_enabled is False
    assert c.backup_path is None 