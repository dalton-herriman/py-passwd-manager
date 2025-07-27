#!/usr/bin/env python3
"""
Basic tests for the password manager
"""

import pytest
import tempfile
import os
import json
from datetime import datetime

from pm_core.manager import PasswordManager
from pm_core.utils import generate_password, validate_password_strength
from pm_core.models import Entry, Vault

class TestPasswordManager:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Set up and tear down test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.vault_path = os.path.join(self.temp_dir, "test_vault.db")
        self.pm = PasswordManager(self.vault_path)
        
        yield
        
        # Cleanup
        if os.path.exists(self.vault_path):
            os.remove(self.vault_path)
        os.rmdir(self.temp_dir)
    
    def test_create_vault(self):
        """Test vault creation"""
        assert not self.pm.is_vault_exists()
        
        self.pm.create_vault("test_password")
        
        assert self.pm.is_vault_exists()
        assert self.pm.is_unlocked
    
    def test_unlock_vault(self):
        """Test vault unlocking"""
        # Create vault first
        self.pm.create_vault("test_password")
        self.pm.lock_vault()
        
        # Unlock vault
        self.pm.unlock_vault("test_password")
        self.assertTrue(self.pm.is_unlocked)
    
    def test_add_entry(self):
        """Test adding entries"""
        self.pm.create_vault("test_password")
        
        entry = self.pm.add_entry(
            service="Test Service",
            username="testuser",
            password="testpass",
            url="https://test.com",
            notes="Test notes"
        )
        
        self.assertIsNotNone(entry)
        self.assertEqual(entry.name, "Test Service")
        self.assertEqual(entry.username, "testuser")
        self.assertEqual(entry.password, "testpass")
        self.assertEqual(entry.url, "https://test.com")
        self.assertEqual(entry.notes, "Test notes")
    
    def test_get_entries(self):
        """Test retrieving entries"""
        self.pm.create_vault("test_password")
        
        # Add multiple entries
        self.pm.add_entry(service="Service 1", username="user1")
        self.pm.add_entry(service="Service 2", username="user2")
        
        entries = self.pm.get_entry()
        self.assertEqual(len(entries), 2)
    
    def test_search_entries(self):
        """Test entry search"""
        self.pm.create_vault("test_password")
        
        self.pm.add_entry(service="Gmail", username="user@gmail.com")
        self.pm.add_entry(service="GitHub", username="user")
        
        # Search by service
        gmail_entries = self.pm.search_entries("gmail")
        self.assertEqual(len(gmail_entries), 1)
        self.assertEqual(gmail_entries[0].name, "Gmail")
    
    def test_update_entry(self):
        """Test updating entries"""
        self.pm.create_vault("test_password")
        
        entry = self.pm.add_entry(service="Test", username="olduser")
        
        # Update entry
        self.pm.update_entry(entry.id, username="newuser")
        
        updated_entries = self.pm.get_entry(entry_id=entry.id)
        self.assertEqual(len(updated_entries), 1)
        self.assertEqual(updated_entries[0].username, "newuser")
    
    def test_delete_entry(self):
        """Test deleting entries"""
        self.pm.create_vault("test_password")
        
        entry = self.pm.add_entry(service="Test", username="user")
        
        # Delete entry
        self.pm.delete_entry(entry.id)
        
        entries = self.pm.get_entry()
        self.assertEqual(len(entries), 0)
    
    def test_generate_password(self):
        """Test password generation"""
        password = generate_password(length=16)
        self.assertEqual(len(password), 16)
        
        # Test with different options
        password_no_symbols = generate_password(length=12, include_symbols=False)
        self.assertEqual(len(password_no_symbols), 12)
        
        # Test strength validation
        strength = validate_password_strength(password)
        self.assertIn('score', strength)
        self.assertIn('strength', strength)
    
    def test_vault_stats(self):
        """Test vault statistics"""
        self.pm.create_vault("test_password")
        
        self.pm.add_entry(service="Test 1")
        self.pm.add_entry(service="Test 2")
        
        stats = self.pm.get_vault_stats()
        self.assertEqual(stats['total_entries'], 2)
        self.assertIn('vault_created', stats)
        self.assertIn('last_updated', stats)
    
    def test_export_entries(self):
        """Test entry export"""
        self.pm.create_vault("test_password")
        
        self.pm.add_entry(service="Test", username="user", password="pass")
        
        exported = self.pm.export_entries()
        data = json.loads(exported)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Test")

class TestUtils(unittest.TestCase):
    def test_password_generation(self):
        """Test password generation utilities"""
        # Test basic generation
        password = generate_password()
        self.assertGreaterEqual(len(password), 8)
        
        # Test custom length
        password = generate_password(length=20)
        self.assertEqual(len(password), 20)
        
        # Test character set options
        password = generate_password(include_symbols=False, include_numbers=False)
        self.assertTrue(password.isalpha())
    
    def test_password_strength(self):
        """Test password strength validation"""
        # Test weak password
        weak_password = "123"
        strength = validate_password_strength(weak_password)
        self.assertEqual(strength['strength'], 'weak')
        
        # Test strong password
        strong_password = "MySecurePass123!"
        strength = validate_password_strength(strong_password)
        self.assertGreaterEqual(strength['score'], 4)

if __name__ == '__main__':
    unittest.main() 