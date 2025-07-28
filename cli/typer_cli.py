#!/usr/bin/env python3
"""
Modern CLI interface using Typer and Rich
Replaces the massive Click-based CLI with cleaner, type-hinted code
"""

import typer
import sys
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich import print as rprint

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pm_core.vault_manager import VaultManager
from pm_core.models_pydantic import (
    Entry, 
    VaultInfo, 
    PasswordGenerationConfig,
    SearchQuery,
    generate_password_from_config,
    validate_password_strength_pydantic
)

# Initialize Rich console
console = Console()

# Create Typer app
app = typer.Typer(
    name="password-manager",
    help="🔐 Multi-Vault Password Manager - Secure password storage and management",
    add_completion=False
)


def get_vault_manager(vaults_dir: str = "vaults") -> VaultManager:
    """Get vault manager instance"""
    return VaultManager(vaults_dir)


@app.command()
def create_vault(
    name: str = typer.Option(..., "--name", "-n", help="Name for the new vault"),
    password: str = typer.Option(..., "--password", "-p", hide_input=True, help="Master password"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Vault description")
):
    """Create a new vault"""
    vm = get_vault_manager()
    
    if vm.vault_exists(name):
        console.print(f"❌ Vault '{name}' already exists", style="red")
        raise typer.Exit(1)
    
    try:
        with console.status("[bold green]Creating vault..."):
            vm.create_vault(name, password, description or "")
        
        console.print(f"✅ Vault '{name}' created successfully", style="green")
        
    except Exception as e:
        console.print(f"❌ Failed to create vault: {e}", style="red")
        raise typer.Exit(1)


@app.command()
def list_vaults():
    """List all available vaults"""
    vm = get_vault_manager()
    
    try:
        vaults = vm.list_vaults()
        
        if not vaults:
            console.print("No vaults found. Create one with 'create-vault' command.", style="yellow")
            return
        
        # Create beautiful table with Rich
        table = Table(title="📋 Available Vaults")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Status", style="green")
        table.add_column("Entries", style="yellow", justify="right")
        table.add_column("Created", style="blue")
        table.add_column("Last Accessed", style="blue")
        
        for vault in vaults:
            status = "🔓 OPEN" if vm.get_current_vault_name() == vault.name else "🔒 LOCKED"
            table.add_row(
                vault.name,
                status,
                str(vault.entry_count),
                vault.created_at.strftime("%Y-%m-%d"),
                vault.last_accessed.strftime("%Y-%m-%d") if vault.last_accessed else "Never"
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"❌ Failed to list vaults: {e}", style="red")
        raise typer.Exit(1)


@app.command()
def open_vault(
    name: str = typer.Option(..., "--name", "-n", help="Name of the vault to open"),
    password: str = typer.Option(..., "--password", "-p", hide_input=True, help="Master password")
):
    """Open a vault"""
    vm = get_vault_manager()
    
    try:
        with console.status("[bold green]Opening vault..."):
            vm.open_vault(name, password)
        
        console.print(f"✅ Vault '{name}' opened successfully", style="green")
        
    except Exception as e:
        console.print(f"❌ Failed to open vault: {e}", style="red")
        raise typer.Exit(1)


@app.command()
def close_vault():
    """Close the current vault"""
    vm = get_vault_manager()
    
    try:
        vm.close_vault()
        console.print("✅ Vault closed successfully", style="green")
        
    except Exception as e:
        console.print(f"❌ Failed to close vault: {e}", style="red")
        raise typer.Exit(1)


@app.command()
def add_entry(
    name: str = typer.Option(..., "--name", "-n", help="Entry name"),
    username: str = typer.Option(..., "--username", "-u", help="Username"),
    password: str = typer.Option(..., "--password", "-p", hide_input=True, help="Password"),
    url: Optional[str] = typer.Option(None, "--url", help="Website URL"),
    notes: Optional[str] = typer.Option(None, "--notes", "-n", help="Additional notes")
):
    """Add a new entry to the current vault"""
    vm = get_vault_manager()
    
    if not vm.get_current_vault():
        console.print("❌ No vault is currently open", style="red")
        raise typer.Exit(1)
    
    try:
        # Use Pydantic for validation
        entry_data = Entry(
            name=name,
            username=username,
            password=password,
            url=url,
            notes=notes
        )
        
        with console.status("[bold green]Adding entry..."):
            vm.add_entry(entry_data.model_dump())
        
        console.print(f"✅ Added entry: {entry_data.name}", style="green")
        
    except Exception as e:
        console.print(f"❌ Failed to add entry: {e}", style="red")
        raise typer.Exit(1)


@app.command()
def list_entries(
    search: Optional[str] = typer.Option(None, "--search", "-s", help="Search query"),
    service: Optional[str] = typer.Option(None, "--service", help="Filter by service name")
):
    """List entries in the current vault"""
    vm = get_vault_manager()
    
    if not vm.get_current_vault():
        console.print("❌ No vault is currently open", style="red")
        raise typer.Exit(1)
    
    try:
        entries = vm.list_entries()
        
        if not entries:
            console.print("No entries found in the current vault.", style="yellow")
            return
        
        # Create beautiful table with Rich
        table = Table(title="📋 Entries")
        table.add_column("ID", style="cyan", justify="right")
        table.add_column("Name", style="green")
        table.add_column("Username", style="blue")
        table.add_column("URL", style="yellow")
        table.add_column("Notes", style="white")
        
        for entry in entries:
            # Truncate long fields
            notes = entry.get("notes", "")[:50] + "..." if len(entry.get("notes", "")) > 50 else entry.get("notes", "")
            url = entry.get("url", "")[:30] + "..." if len(entry.get("url", "")) > 30 else entry.get("url", "")
            
            table.add_row(
                str(entry.get("id", "")),
                entry.get("name", ""),
                entry.get("username", ""),
                url,
                notes
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"❌ Failed to list entries: {e}", style="red")
        raise typer.Exit(1)


@app.command()
def show_entry(
    entry_id: int = typer.Option(..., "--id", "-i", help="Entry ID to show"),
    copy_password: bool = typer.Option(False, "--copy-password", "-c", help="Copy password to clipboard")
):
    """Show details of a specific entry"""
    vm = get_vault_manager()
    
    if not vm.get_current_vault():
        console.print("❌ No vault is currently open", style="red")
        raise typer.Exit(1)
    
    try:
        entry = vm.get_entry(entry_id)
        
        if not entry:
            console.print(f"❌ Entry with ID {entry_id} not found", style="red")
            raise typer.Exit(1)
        
        # Create beautiful panel with Rich
        content = f"""
[bold cyan]Name:[/bold cyan] {entry.get('name', '')}
[bold cyan]Username:[/bold cyan] {entry.get('username', '')}
[bold cyan]Password:[/bold cyan] {'*' * len(entry.get('password', ''))}
[bold cyan]URL:[/bold cyan] {entry.get('url', 'N/A')}
[bold cyan]Notes:[/bold cyan] {entry.get('notes', 'N/A')}
[bold cyan]Created:[/bold cyan] {entry.get('created_at', 'N/A')}
        """
        
        panel = Panel(content, title="Entry Details", border_style="green")
        console.print(panel)
        
        if copy_password:
            try:
                import pyperclip
                pyperclip.copy(entry.get('password', ''))
                console.print("✅ Password copied to clipboard", style="green")
            except ImportError:
                console.print("❌ pyperclip not available for clipboard operations", style="red")
        
    except Exception as e:
        console.print(f"❌ Failed to show entry: {e}", style="red")
        raise typer.Exit(1)


@app.command()
def generate_password(
    length: int = typer.Option(16, "--length", "-l", help="Password length"),
    no_symbols: bool = typer.Option(False, "--no-symbols", help="Exclude symbols"),
    no_numbers: bool = typer.Option(False, "--no-numbers", help="Exclude numbers"),
    no_uppercase: bool = typer.Option(False, "--no-uppercase", help="Exclude uppercase letters"),
    copy: bool = typer.Option(False, "--copy", "-c", help="Copy to clipboard")
):
    """Generate a secure password"""
    try:
        # Use Pydantic config for validation
        config = PasswordGenerationConfig(
            length=length,
            include_symbols=not no_symbols,
            include_numbers=not no_numbers,
            include_uppercase=not no_uppercase
        )
        
        with console.status("[bold green]Generating password..."):
            password = generate_password_from_config(config)
        
        # Validate password strength
        strength_info = validate_password_strength_pydantic(password)
        
        # Display results
        console.print(f"🔐 Generated Password: [bold green]{password}[/bold green]")
        console.print(f"📊 Strength: [bold {strength_info['strength']}]{strength_info['strength']}[/bold {strength_info['strength']}]")
        console.print(f"📏 Length: {strength_info['length']} characters")
        
        if copy:
            try:
                import pyperclip
                pyperclip.copy(password)
                console.print("✅ Password copied to clipboard", style="green")
            except ImportError:
                console.print("❌ pyperclip not available for clipboard operations", style="red")
        
    except Exception as e:
        console.print(f"❌ Failed to generate password: {e}", style="red")
        raise typer.Exit(1)


@app.command()
def stats():
    """Show vault statistics"""
    vm = get_vault_manager()
    
    try:
        current_vault = vm.get_current_vault_name()
        
        if not current_vault:
            console.print("❌ No vault is currently open", style="red")
            raise typer.Exit(1)
        
        entries = vm.list_entries()
        
        # Calculate statistics
        total_entries = len(entries)
        entries_with_urls = len([e for e in entries if e.get('url')])
        entries_with_notes = len([e for e in entries if e.get('notes')])
        
        # Create statistics panel
        content = f"""
[bold cyan]Vault:[/bold cyan] {current_vault}
[bold cyan]Total Entries:[/bold cyan] {total_entries}
[bold cyan]Entries with URLs:[/bold cyan] {entries_with_urls}
[bold cyan]Entries with Notes:[/bold cyan] {entries_with_notes}
        """
        
        panel = Panel(content, title="📊 Vault Statistics", border_style="blue")
        console.print(panel)
        
    except Exception as e:
        console.print(f"❌ Failed to get statistics: {e}", style="red")
        raise typer.Exit(1)


def main():
    """Main entry point"""
    app()


if __name__ == "__main__":
    main() 