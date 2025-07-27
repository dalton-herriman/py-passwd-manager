#!/usr/bin/env python3
"""
CLI interface for the password manager
"""

import click
import getpass
import sys
from pathlib import Path
from typing import Optional

from pm_core.manager import PasswordManager
from pm_core.utils import generate_password, clipboard_handler, validate_password_strength

@click.group()
@click.option('--vault-path', '-v', default='vault.db', 
              help='Path to the vault file')
@click.pass_context
def cli(ctx, vault_path):
    """Password Manager CLI - Secure password storage and management"""
    ctx.ensure_object(dict)
    ctx.obj['vault_path'] = vault_path
    ctx.obj['pm'] = PasswordManager(vault_path)

@cli.command()
@click.option('--master-password', '-p', prompt=True, hide_input=True, 
              confirmation_prompt=True, help='Master password for the vault')
@click.pass_context
def create(ctx, master_password):
    """Create a new password vault"""
    pm = ctx.obj['pm']
    vault_path = ctx.obj['vault_path']
    
    if pm.is_vault_exists():
        click.echo(f"❌ Vault already exists at {vault_path}")
        sys.exit(1)
    
    try:
        pm.create_vault(master_password)
        click.echo(f"✅ Vault created successfully at {vault_path}")
    except Exception as e:
        click.echo(f"❌ Failed to create vault: {str(e)}")
        sys.exit(1)

@cli.command()
@click.option('--master-password', '-p', prompt=True, hide_input=True,
              help='Master password for the vault')
@click.pass_context
def unlock(ctx, master_password):
    """Unlock an existing vault"""
    pm = ctx.obj['pm']
    
    if not pm.is_vault_exists():
        click.echo("❌ Vault does not exist. Use 'create' command first.")
        sys.exit(1)
    
    try:
        pm.unlock_vault(master_password)
        click.echo("✅ Vault unlocked successfully")
    except Exception as e:
        click.echo(f"❌ Failed to unlock vault: {str(e)}")
        sys.exit(1)

@cli.command()
@click.pass_context
def lock(ctx):
    """Lock the vault"""
    pm = ctx.obj['pm']
    
    if not pm.is_unlocked:
        click.echo("❌ Vault is not unlocked")
        sys.exit(1)
    
    pm.lock_vault()
    click.echo("✅ Vault locked")

@cli.command()
@click.option('--service', '-s', required=True, help='Service name (e.g., Gmail, GitHub)')
@click.option('--username', '-u', help='Username or email')
@click.option('--password', '-p', help='Password (will prompt if not provided)')
@click.option('--url', help='Website URL')
@click.option('--notes', '-n', help='Additional notes')
@click.option('--generate', '-g', is_flag=True, help='Generate a secure password')
@click.option('--length', '-l', default=16, help='Password length for generation')
@click.pass_context
def add(ctx, service, username, password, url, notes, generate, length):
    """Add a new password entry"""
    pm = ctx.obj['pm']
    
    if not pm.is_unlocked:
        click.echo("❌ Vault is not unlocked. Use 'unlock' command first.")
        sys.exit(1)
    
    if generate:
        password = generate_password(length)
        click.echo(f"🔐 Generated password: {password}")
    elif not password:
        password = getpass.getpass("Enter password: ")
    
    try:
        entry = pm.add_entry(
            service=service,
            username=username,
            password=password,
            url=url,
            notes=notes
        )
        click.echo(f"✅ Added entry: {entry.name} (ID: {entry.id})")
    except Exception as e:
        click.echo(f"❌ Failed to add entry: {str(e)}")
        sys.exit(1)

@cli.command()
@click.option('--service', '-s', help='Filter by service name')
@click.option('--id', '-i', type=int, help='Show specific entry by ID')
@click.option('--search', help='Search in names, usernames, and notes')
@click.pass_context
def list(ctx, service, id, search):
    """List password entries"""
    pm = ctx.obj['pm']
    
    if not pm.is_unlocked:
        click.echo("❌ Vault is not unlocked. Use 'unlock' command first.")
        sys.exit(1)
    
    try:
        if id:
            entries = pm.get_entry(entry_id=id)
        elif service:
            entries = pm.get_entry(service=service)
        elif search:
            entries = pm.search_entries(search)
        else:
            entries = pm.get_entry()
        
        if not entries:
            click.echo("No entries found")
            return
        
        click.echo(f"\n📋 Found {len(entries)} entries:")
        click.echo("-" * 80)
        
        for entry in entries:
            click.echo(f"ID: {entry.id}")
            click.echo(f"Service: {entry.name}")
            if entry.username:
                click.echo(f"Username: {entry.username}")
            if entry.url:
                click.echo(f"URL: {entry.url}")
            if entry.notes:
                click.echo(f"Notes: {entry.notes}")
            click.echo(f"Created: {entry.created_at}")
            click.echo("-" * 40)
    
    except Exception as e:
        click.echo(f"❌ Failed to list entries: {str(e)}")
        sys.exit(1)

@cli.command()
@click.option('--id', '-i', required=True, type=int, help='Entry ID to show')
@click.option('--copy-password', '-c', is_flag=True, help='Copy password to clipboard')
@click.pass_context
def show(ctx, id, copy_password):
    """Show details of a specific entry"""
    pm = ctx.obj['pm']
    
    if not pm.is_unlocked:
        click.echo("❌ Vault is not unlocked. Use 'unlock' command first.")
        sys.exit(1)
    
    try:
        entries = pm.get_entry(entry_id=id)
        if not entries:
            click.echo(f"❌ Entry with ID {id} not found")
            sys.exit(1)
        
        entry = entries[0]
        
        click.echo(f"\n📋 Entry Details (ID: {entry.id}):")
        click.echo("=" * 50)
        click.echo(f"Service: {entry.name}")
        if entry.username:
            click.echo(f"Username: {entry.username}")
        if entry.password:
            click.echo(f"Password: {'*' * len(entry.password)}")
            if copy_password:
                if clipboard_handler(entry.password):
                    click.echo("✅ Password copied to clipboard")
                else:
                    click.echo("❌ Failed to copy to clipboard")
        if entry.url:
            click.echo(f"URL: {entry.url}")
        if entry.notes:
            click.echo(f"Notes: {entry.notes}")
        click.echo(f"Created: {entry.created_at}")
        click.echo(f"Updated: {entry.updated_at}")
    
    except Exception as e:
        click.echo(f"❌ Failed to show entry: {str(e)}")
        sys.exit(1)

@cli.command()
@click.option('--id', '-i', required=True, type=int, help='Entry ID to update')
@click.option('--service', '-s', help='New service name')
@click.option('--username', '-u', help='New username')
@click.option('--password', '-p', help='New password')
@click.option('--url', help='New URL')
@click.option('--notes', '-n', help='New notes')
@click.pass_context
def update(ctx, id, service, username, password, url, notes):
    """Update an existing entry"""
    pm = ctx.obj['pm']
    
    if not pm.is_unlocked:
        click.echo("❌ Vault is not unlocked. Use 'unlock' command first.")
        sys.exit(1)
    
    # Build update dict
    updates = {}
    if service:
        updates['name'] = service
    if username is not None:
        updates['username'] = username
    if password is not None:
        updates['password'] = password
    if url is not None:
        updates['url'] = url
    if notes is not None:
        updates['notes'] = notes
    
    if not updates:
        click.echo("❌ No fields to update")
        sys.exit(1)
    
    try:
        pm.update_entry(id, **updates)
        click.echo(f"✅ Entry {id} updated successfully")
    except Exception as e:
        click.echo(f"❌ Failed to update entry: {str(e)}")
        sys.exit(1)

@cli.command()
@click.option('--id', '-i', required=True, type=int, help='Entry ID to delete')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation')
@click.pass_context
def delete(ctx, id, force):
    """Delete an entry"""
    pm = ctx.obj['pm']
    
    if not pm.is_unlocked:
        click.echo("❌ Vault is not unlocked. Use 'unlock' command first.")
        sys.exit(1)
    
    if not force:
        if not click.confirm(f"Are you sure you want to delete entry {id}?"):
            click.echo("Operation cancelled")
            return
    
    try:
        pm.delete_entry(id)
        click.echo(f"✅ Entry {id} deleted successfully")
    except Exception as e:
        click.echo(f"❌ Failed to delete entry: {str(e)}")
        sys.exit(1)

@cli.command()
@click.option('--format', '-f', default='json', help='Export format (json)')
@click.option('--output', '-o', help='Output file path')
@click.pass_context
def export(ctx, format, output):
    """Export all entries"""
    pm = ctx.obj['pm']
    
    if not pm.is_unlocked:
        click.echo("❌ Vault is not unlocked. Use 'unlock' command first.")
        sys.exit(1)
    
    try:
        data = pm.export_entries(format)
        
        if output:
            with open(output, 'w') as f:
                f.write(data)
            click.echo(f"✅ Exported to {output}")
        else:
            click.echo(data)
    
    except Exception as e:
        click.echo(f"❌ Failed to export: {str(e)}")
        sys.exit(1)

@cli.command()
@click.pass_context
def stats(ctx):
    """Show vault statistics"""
    pm = ctx.obj['pm']
    
    if not pm.is_unlocked:
        click.echo("❌ Vault is not unlocked. Use 'unlock' command first.")
        sys.exit(1)
    
    try:
        stats = pm.get_vault_stats()
        
        click.echo("\n📊 Vault Statistics:")
        click.echo("=" * 30)
        click.echo(f"Total entries: {stats['total_entries']}")
        click.echo(f"Vault created: {stats['vault_created']}")
        click.echo(f"Last updated: {stats['last_updated']}")
        click.echo(f"Vault version: {stats['vault_version']}")
    
    except Exception as e:
        click.echo(f"❌ Failed to get stats: {str(e)}")
        sys.exit(1)

@cli.command()
@click.option('--length', '-l', default=16, help='Password length')
@click.option('--no-symbols', is_flag=True, help='Exclude symbols')
@click.option('--no-numbers', is_flag=True, help='Exclude numbers')
@click.option('--no-uppercase', is_flag=True, help='Exclude uppercase letters')
@click.option('--copy', '-c', is_flag=True, help='Copy to clipboard')
@click.pass_context
def generate(ctx, length, no_symbols, no_numbers, no_uppercase, copy):
    """Generate a secure password"""
    try:
        password = generate_password(
            length=length,
            include_symbols=not no_symbols,
            include_numbers=not no_numbers,
            include_uppercase=not no_uppercase
        )
        
        click.echo(f"🔐 Generated password: {password}")
        
        if copy:
            if clipboard_handler(password):
                click.echo("✅ Password copied to clipboard")
            else:
                click.echo("❌ Failed to copy to clipboard")
        
        # Show strength analysis
        strength = validate_password_strength(password)
        click.echo(f"Strength: {strength['strength']} (Score: {strength['score']}/5)")
        
        if strength['feedback']:
            click.echo("Suggestions:")
            for feedback in strength['feedback']:
                click.echo(f"  - {feedback}")
    
    except Exception as e:
        click.echo(f"❌ Failed to generate password: {str(e)}")
        sys.exit(1)

def main():
    """Main entry point"""
    cli()

if __name__ == '__main__':
    main()
