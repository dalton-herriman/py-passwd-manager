import pytest
from pm_core import exceptions


def test_password_manager_error():
    with pytest.raises(exceptions.PasswordManagerError):
        raise exceptions.PasswordManagerError("msg")


def test_vault_error():
    with pytest.raises(exceptions.VaultError):
        raise exceptions.VaultError("msg")


def test_crypto_error():
    with pytest.raises(exceptions.CryptoError):
        raise exceptions.CryptoError("msg")


def test_storage_error():
    with pytest.raises(exceptions.StorageError):
        raise exceptions.StorageError("msg")


def test_validation_error():
    with pytest.raises(exceptions.ValidationError):
        raise exceptions.ValidationError("msg")


def test_authentication_error():
    with pytest.raises(exceptions.AuthenticationError):
        raise exceptions.AuthenticationError("msg")


def test_configuration_error():
    with pytest.raises(exceptions.ConfigurationError):
        raise exceptions.ConfigurationError("msg")
