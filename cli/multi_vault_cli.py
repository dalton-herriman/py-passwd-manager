#!/usr/bin/env python3
"""
Multi-vault CLI interface for the password manager
"""

import click
import getpass
import sys
from pathlib import Path
from typing import Optional

from pm_core.vault_manager import VaultManager
from pm_core.utils import (
    generate_password,
    clipboard_handler,
    validate_password_strength,
)


@click.group()
@click.option(
    "--vaults-dir", "-d", default="vaults", help="Directory containing vaults"
)
@click.pass_context
def cli(ctx, vaults_dir):
    """Multi-Vault Password Manager CLI - Secure password storage and management"""
    ctx.ensure_object(dict)
    ctx.obj["vault_manager"] = VaultManager(vaults_dir)


@cli.command()
@click.option("--name", "-n", required=True, help="Name for the new vault")
@click.option(
    "--master-password",
    "-p",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Master password for the vault",
)
@click.option("--description", help="Description for the vault")
@click.pass_context
def create_vault(ctx, name, master_password, description):
    """Create a new vault"""
    vm = ctx.obj["vault_manager"]

    if vm.vault_exists(name):
        click.echo(f"❌ Vault '{name}' already exists")
        sys.exit(1)

    try:
        vm.create_vault(name, master_password, description or "")
        click.echo(f"✅ Vault '{name}' created successfully")
    except Exception as e:
        click.echo(f"❌ Failed to create vault: {str(e)}")
        sys.exit(1)


@cli.command()
@click.pass_context
def list_vaults(ctx):
    """List all available vaults"""
    vm = ctx.obj["vault_manager"]

    try:
        vaults = vm.list_vaults()

        if not vaults:
            click.echo("No vaults found. Create one with 'create-vault' command.")
            return

        click.echo(f"\n📋 Found {len(vaults)} vaults:")
        click.echo("=" * 80)

        for vault in vaults:
            status = (
                "🔓 OPEN" if vm.get_current_vault_name() == vault.name else "🔒 LOCKED"
            )
            click.echo(f"Name: {vault.name}")
            click.echo(f"Status: {status}")
            click.echo(f"Entries: {vault.entry_count}")
            click.echo(f"Created: {vault.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            click.echo(
                f"Last accessed: {vault.last_accessed.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            click.echo(f"Path: {vault.path}")
            click.echo("-" * 40)

    except Exception as e:
        click.echo(f"❌ Failed to list vaults: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option("--name", "-n", required=True, help="Name of the vault to open")
@click.option(
    "--master-password",
    "-p",
    prompt=True,
    hide_input=True,
    help="Master password for the vault",
)
@click.pass_context
def open_vault(ctx, name, master_password):
    """Open a vault"""
    vm = ctx.obj["vault_manager"]

    if not vm.vault_exists(name):
        click.echo(f"❌ Vault '{name}' not found")
        sys.exit(1)

    try:
        vm.open_vault(name, master_password)
        click.echo(f"✅ Vault '{name}' opened successfully")
    except Exception as e:
        click.echo(f"❌ Failed to open vault: {str(e)}")
        sys.exit(1)


@cli.command()
@click.pass_context
def close_vault(ctx):
    """Close the currently open vault"""
    vm = ctx.obj["vault_manager"]

    if not vm.get_current_vault():
        click.echo("❌ No vault is currently open")
        sys.exit(1)

    vm.close_vault()
    click.echo("✅ Vault closed")


@cli.command()
@click.option("--name", "-n", required=True, help="Name of the vault to delete")
@click.option("--force", "-f", is_flag=True, help="Skip confirmation")
@click.pass_context
def delete_vault(ctx, name, force):
    """Delete a vault"""
    vm = ctx.obj["vault_manager"]

    if not vm.vault_exists(name):
        click.echo(f"❌ Vault '{name}' not found")
        sys.exit(1)

    if not force:
        if not click.confirm(
            f"Are you sure you want to delete vault '{name}'? This cannot be undone."
        ):
            click.echo("Operation cancelled")
            return

    try:
        vm.delete_vault(name)
        click.echo(f"✅ Vault '{name}' deleted successfully")
    except Exception as e:
        click.echo(f"❌ Failed to delete vault: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option("--old-name", required=True, help="Current name of the vault")
@click.option("--new-name", required=True, help="New name for the vault")
@click.pass_context
def rename_vault(ctx, old_name, new_name):
    """Rename a vault"""
    vm = ctx.obj["vault_manager"]

    if not vm.vault_exists(old_name):
        click.echo(f"❌ Vault '{old_name}' not found")
        sys.exit(1)

    if vm.vault_exists(new_name):
        click.echo(f"❌ Vault '{new_name}' already exists")
        sys.exit(1)

    try:
        vm.rename_vault(old_name, new_name)
        click.echo(f"✅ Vault '{old_name}' renamed to '{new_name}'")
    except Exception as e:
        click.echo(f"❌ Failed to rename vault: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option("--name", "-n", required=True, help="Name of the vault to backup")
@click.option("--output", "-o", required=True, help="Backup file path")
@click.pass_context
def backup_vault(ctx, name, output):
    """Create a backup of a vault"""
    vm = ctx.obj["vault_manager"]

    if not vm.vault_exists(name):
        click.echo(f"❌ Vault '{name}' not found")
        sys.exit(1)

    try:
        vm.backup_vault(name, output)
        click.echo(f"✅ Vault '{name}' backed up to {output}")
    except Exception as e:
        click.echo(f"❌ Failed to backup vault: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option("--backup-file", required=True, help="Path to backup file")
@click.option("--name", "-n", required=True, help="Name for the restored vault")
@click.pass_context
def restore_vault(ctx, backup_file, name):
    """Restore a vault from backup"""
    vm = ctx.obj["vault_manager"]

    if vm.vault_exists(name):
        click.echo(f"❌ Vault '{name}' already exists")
        sys.exit(1)

    try:
        vm.restore_vault(backup_file, name)
        click.echo(f"✅ Vault '{name}' restored from backup")
    except Exception as e:
        click.echo(f"❌ Failed to restore vault: {str(e)}")
        sys.exit(1)


# Entry management commands (require an open vault)
@cli.command()
@click.option(
    "--service", "-s", required=True, help="Service name (e.g., Gmail, GitHub)"
)
@click.option("--username", "-u", help="Username or email")
@click.option("--password", "-p", help="Password (will prompt if not provided)")
@click.option("--url", help="Website URL")
@click.option("--notes", "-n", help="Additional notes")
@click.option("--generate", "-g", is_flag=True, help="Generate a secure password")
@click.option("--length", "-l", default=16, help="Password length for generation")
@click.pass_context
def add(ctx, service, username, password, url, notes, generate, length):
    """Add a new password entry to the current vault"""
    vm = ctx.obj["vault_manager"]
    pm = vm.get_current_vault()

    if not pm:
        click.echo("❌ No vault is open. Use 'open-vault' command first.")
        sys.exit(1)

    if generate:
        password = generate_password(length)
        click.echo(f"🔐 Generated password: {password}")
    elif not password:
        password = getpass.getpass("Enter password: ")

    try:
        entry = pm.add_entry(
            service=service, username=username, password=password, url=url, notes=notes
        )
        click.echo(f"✅ Added entry: {entry.name} (ID: {entry.id})")
        click.echo("💡 Note: Use 'save' command to persist changes to disk")
    except Exception as e:
        click.echo(f"❌ Failed to add entry: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option("--service", "-s", help="Filter by service name")
@click.option("--id", "-i", type=int, help="Show specific entry by ID")
@click.option("--search", help="Search in names, usernames, and notes")
@click.pass_context
def list_entries(ctx, service, id, search):
    """List password entries in the current vault"""
    vm = ctx.obj["vault_manager"]
    pm = vm.get_current_vault()

    if not pm:
        click.echo("❌ No vault is open. Use 'open-vault' command first.")
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

        click.echo(
            f"\n📋 Found {len(entries)} entries in vault '{vm.get_current_vault_name()}':"
        )
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
@click.option("--id", "-i", required=True, type=int, help="Entry ID to show")
@click.option("--copy-password", "-c", is_flag=True, help="Copy password to clipboard")
@click.pass_context
def show(ctx, id, copy_password):
    """Show details of a specific entry"""
    vm = ctx.obj["vault_manager"]
    pm = vm.get_current_vault()

    if not pm:
        click.echo("❌ No vault is open. Use 'open-vault' command first.")
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
@click.option("--id", "-i", required=True, type=int, help="Entry ID to update")
@click.option("--service", "-s", help="New service name")
@click.option("--username", "-u", help="New username")
@click.option("--password", "-p", help="New password")
@click.option("--url", help="New URL")
@click.option("--notes", "-n", help="New notes")
@click.pass_context
def update(ctx, id, service, username, password, url, notes):
    """Update an existing entry"""
    vm = ctx.obj["vault_manager"]
    pm = vm.get_current_vault()

    if not pm:
        click.echo("❌ No vault is open. Use 'open-vault' command first.")
        sys.exit(1)

    # Build update dict
    updates = {}
    if service:
        updates["name"] = service
    if username is not None:
        updates["username"] = username
    if password is not None:
        updates["password"] = password
    if url is not None:
        updates["url"] = url
    if notes is not None:
        updates["notes"] = notes

    if not updates:
        click.echo("❌ No fields to update")
        sys.exit(1)

    try:
        pm.update_entry(id, **updates)
        click.echo(f"✅ Entry {id} updated successfully")
        click.echo("💡 Note: Use 'save' command to persist changes to disk")
    except Exception as e:
        click.echo(f"❌ Failed to update entry: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option("--id", "-i", required=True, type=int, help="Entry ID to delete")
@click.option("--force", "-f", is_flag=True, help="Skip confirmation")
@click.pass_context
def delete(ctx, id, force):
    """Delete an entry"""
    vm = ctx.obj["vault_manager"]
    pm = vm.get_current_vault()

    if not pm:
        click.echo("❌ No vault is open. Use 'open-vault' command first.")
        sys.exit(1)

    if not force:
        if not click.confirm(f"Are you sure you want to delete entry {id}?"):
            click.echo("Operation cancelled")
            return

    try:
        pm.delete_entry(id)
        click.echo(f"✅ Entry {id} deleted successfully")
        click.echo("💡 Note: Use 'save' command to persist changes to disk")
    except Exception as e:
        click.echo(f"❌ Failed to delete entry: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option(
    "--master-password",
    "-p",
    prompt=True,
    hide_input=True,
    help="Master password for the vault",
)
@click.pass_context
def save(ctx, master_password):
    """Save the current vault state"""
    vm = ctx.obj["vault_manager"]
    pm = vm.get_current_vault()

    if not pm:
        click.echo("❌ No vault is open. Use 'open-vault' command first.")
        sys.exit(1)

    try:
        pm.save_vault(master_password)
        # Update entry count in registry
        current_vault_name = vm.get_current_vault_name()
        if current_vault_name:
            entry_count = len(pm.get_entry())
            vm.update_vault_entry_count(current_vault_name, entry_count)
        click.echo("✅ Vault saved successfully")
    except Exception as e:
        click.echo(f"❌ Failed to save vault: {str(e)}")
        sys.exit(1)


@cli.command()
@click.pass_context
def stats(ctx):
    """Show current vault statistics"""
    vm = ctx.obj["vault_manager"]
    pm = vm.get_current_vault()

    if not pm:
        click.echo("❌ No vault is open. Use 'open-vault' command first.")
        sys.exit(1)

    try:
        stats = pm.get_vault_stats()

        click.echo(f"\n📊 Vault Statistics for '{vm.get_current_vault_name()}':")
        click.echo("=" * 50)
        click.echo(f"Total entries: {stats['total_entries']}")
        click.echo(f"Vault created: {stats['vault_created']}")
        click.echo(f"Last updated: {stats['last_updated']}")
        click.echo(f"Vault version: {stats['vault_version']}")

    except Exception as e:
        click.echo(f"❌ Failed to get stats: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option("--length", "-l", default=16, help="Password length")
@click.option("--no-symbols", is_flag=True, help="Exclude symbols")
@click.option("--no-numbers", is_flag=True, help="Exclude numbers")
@click.option("--no-uppercase", is_flag=True, help="Exclude uppercase letters")
@click.option("--copy", "-c", is_flag=True, help="Copy to clipboard")
@click.pass_context
def generate(ctx, length, no_symbols, no_numbers, no_uppercase, copy):
    """Generate a secure password"""
    try:
        password = generate_password(
            length=length,
            include_symbols=not no_symbols,
            include_numbers=not no_numbers,
            include_uppercase=not no_uppercase,
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

        if strength["feedback"]:
            click.echo("Suggestions:")
            for feedback in strength["feedback"]:
                click.echo(f"  - {feedback}")

    except Exception as e:
        click.echo(f"❌ Failed to generate password: {str(e)}")
        sys.exit(1)


def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()
