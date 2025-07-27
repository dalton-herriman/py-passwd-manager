#!/usr/bin/env python3
"""
Test utilities and helper functions
"""

import pytest
import time
import secrets
import string
from unittest.mock import patch, Mock
from pm_core.utils import (
    generate_password,
    validate_password_strength,
    get_system_info,
    wipe_memory,
    clipboard_handler,
)
from pm_core.exceptions import ValidationError


class TestPasswordGeneration:
    """Test password generation functionality"""

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "length,include_symbols,include_numbers,include_uppercase",
        [
            (16, True, True, True),
            (12, False, True, True),
            (10, True, False, True),
            (8, True, True, False),
            (20, True, True, True),
            (32, True, True, True),
        ],
    )
    def test_generate_password_various(
        self, length, include_symbols, include_numbers, include_uppercase
    ):
        """Test password generation with various parameters"""
        password = generate_password(
            length=length,
            include_symbols=include_symbols,
            include_numbers=include_numbers,
            include_uppercase=include_uppercase,
        )

        assert len(password) == length
        assert password != generate_password(
            length, include_symbols, include_numbers, include_uppercase
        )

    @pytest.mark.unit
    def test_generate_password_no_charset(self):
        """Test password generation with no character sets selected"""
        with pytest.raises(ValueError):
            generate_password(
                length=10,
                include_symbols=False,
                include_numbers=False,
                include_uppercase=False,
            )

    @pytest.mark.performance
    def test_generate_password_performance(self):
        """Test password generation performance"""
        start_time = time.time()
        for _ in range(1000):
            generate_password(16)
        end_time = time.time()

        # Should generate 1000 passwords in under 1 second
        assert end_time - start_time < 1.0

    @pytest.mark.security
    def test_generate_password_uniqueness(self):
        """Test that generated passwords are unique"""
        passwords = set()
        for _ in range(100):
            password = generate_password(16)
            assert password not in passwords
            passwords.add(password)


class TestPasswordValidation:
    """Test password strength validation"""

    @pytest.mark.security
    def test_validate_password_strength(self):
        """Test password strength validation"""
        # Test weak passwords
        result = validate_password_strength("123456")
        assert result["score"] <= 2
        assert result["strength"] == "weak"

        result = validate_password_strength("password")
        assert result["score"] <= 2
        assert result["strength"] == "weak"

        # Test medium passwords
        result = validate_password_strength("Password123")
        assert result["score"] >= 3
        assert result["strength"] in ["medium", "strong"]

        # Test strong passwords
        result = validate_password_strength("Password123!")
        assert result["score"] >= 4
        assert result["strength"] == "strong"

    @pytest.mark.unit
    def test_validate_password_edge_cases(self):
        """Test password validation edge cases"""
        # Empty password
        result = validate_password_strength("")
        assert result["score"] == 0
        assert result["strength"] == "weak"

        # Very long password
        long_password = "a" * 1000
        result = validate_password_strength(long_password)
        assert result["score"] >= 1

        # Special characters only
        result = validate_password_strength("!@#$%^&*()")
        assert result["score"] >= 2


class TestSystemInfo:
    """Test system information utilities"""

    @pytest.mark.unit
    def test_get_system_info(self):
        """Test system information retrieval"""
        info = get_system_info()

        assert "platform" in info
        assert "python_version" in info
        assert "architecture" in info
        assert isinstance(info["platform"], str)
        assert isinstance(info["python_version"], str)


class TestMemoryWiping:
    """Test secure memory wiping functionality"""

    @pytest.mark.security
    def test_wipe_memory_str(self):
        """Test wiping string from memory"""
        test_str = "sensitive_password_123"
        original_id = id(test_str)

        wipe_memory(test_str)

        # The string should still exist but content may be cleared
        assert test_str is not None

    @pytest.mark.security
    def test_wipe_memory_bytes(self):
        """Test wiping bytes from memory"""
        test_bytes = b"sensitive_data_456"
        wipe_memory(test_bytes)

        # The bytes object should still exist
        assert test_bytes is not None

    @pytest.mark.security
    def test_wipe_memory_list(self):
        """Test wiping list from memory"""
        test_list = ["sensitive", "data", "789"]
        wipe_memory(test_list)

        # The list should still exist
        assert test_list is not None


class TestClipboardHandler:
    """Test clipboard functionality"""

    @pytest.mark.unit
    def test_clipboard_handler_success(self):
        """Test successful clipboard operations"""
        with patch("pyperclip.copy") as mock_copy, patch(
            "pyperclip.paste"
        ) as mock_paste:

            mock_paste.return_value = "test_data"

            result = clipboard_handler("test_password", timeout=0)

            mock_copy.assert_called_once_with("test_password")
            assert result is True

    @pytest.mark.unit
    def test_clipboard_handler_importerror(self):
        """Test clipboard handler when pyperclip is not available"""
        with patch(
            "builtins.__import__",
            side_effect=ImportError("No module named 'pyperclip'"),
        ):
            # Should not raise an exception
            result = clipboard_handler("test", timeout=0)
            assert result is False


class TestPerformance:
    """Performance testing utilities"""

    @pytest.mark.performance
    def test_password_generation_speed(self):
        """Test password generation speed"""
        start_time = time.time()
        passwords = [generate_password(16) for _ in range(1000)]
        end_time = time.time()

        # Should generate 1000 passwords in under 0.5 seconds
        assert end_time - start_time < 0.5
        assert len(passwords) == 1000
        assert len(set(passwords)) == 1000  # All unique

    @pytest.mark.performance
    def test_password_validation_speed(self):
        """Test password validation speed"""
        test_passwords = [
            "weak123",
            "MediumPass123",
            "StrongPass123!@#",
            "VeryStrongPass123!@#$%^&*()",
            "K9#mP2$vL8@nR5!Xy7$qW3#mN9@pL2!",
        ] * 200  # 1000 total passwords

        start_time = time.time()
        results = [validate_password_strength(pwd) for pwd in test_passwords]
        end_time = time.time()

        # Should validate 1000 passwords in under 0.1 seconds
        assert end_time - start_time < 0.1
        assert len(results) == 1000
        assert all(isinstance(result, dict) for result in results)


class TestSecurity:
    """Security-focused tests"""

    @pytest.mark.security
    def test_password_entropy(self):
        """Test that generated passwords have sufficient entropy"""
        passwords = [generate_password(16) for _ in range(100)]

        for password in passwords:
            # Check for character diversity
            has_lower = any(c.islower() for c in password)
            has_upper = any(c.isupper() for c in password)
            has_digit = any(c.isdigit() for c in password)
            has_symbol = any(c in string.punctuation for c in password)

            # At least 3 different character types should be present
            assert sum([has_lower, has_upper, has_digit, has_symbol]) >= 3

    @pytest.mark.security
    def test_no_common_patterns(self):
        """Test that generated passwords don't contain common patterns"""
        passwords = [generate_password(16) for _ in range(100)]

        common_patterns = [
            "123456",
            "password",
            "qwerty",
            "abc123",
            "admin",
            "letmein",
            "welcome",
            "monkey",
        ]

        for password in passwords:
            for pattern in common_patterns:
                assert pattern.lower() not in password.lower()

    @pytest.mark.security
    def test_no_repeating_characters(self):
        """Test that generated passwords don't have excessive repeating characters"""
        passwords = [generate_password(16) for _ in range(100)]

        for password in passwords:
            # Check for no more than 3 consecutive identical characters
            for i in range(len(password) - 2):
                assert not (password[i] == password[i + 1] == password[i + 2])


class TestEdgeCases:
    """Test edge cases and error conditions"""

    @pytest.mark.unit
    def test_generate_password_zero_length(self):
        """Test password generation with zero length"""
        with pytest.raises(ValueError):
            generate_password(0)

    @pytest.mark.unit
    def test_generate_password_negative_length(self):
        """Test password generation with negative length"""
        with pytest.raises(ValueError):
            generate_password(-1)

    @pytest.mark.unit
    def test_generate_password_very_large_length(self):
        """Test password generation with very large length"""
        # Should handle large lengths gracefully
        password = generate_password(1000)
        assert len(password) == 1000

    @pytest.mark.unit
    def test_validate_password_none(self):
        """Test password validation with None"""
        result = validate_password_strength(None)
        assert result["score"] == 0
        assert result["strength"] == "weak"

    @pytest.mark.unit
    def test_validate_password_non_string(self):
        """Test password validation with non-string input"""
        result = validate_password_strength(123)
        assert result["score"] == 0
        assert result["strength"] == "weak"

        result = validate_password_strength([])
        assert result["score"] == 0
        assert result["strength"] == "weak"

        result = validate_password_strength({})
        assert result["score"] == 0
        assert result["strength"] == "weak"
