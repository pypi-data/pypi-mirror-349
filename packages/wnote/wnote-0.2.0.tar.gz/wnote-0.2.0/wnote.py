#!/usr/bin/env python3
import os
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
import json
import datetime
import tempfile
import subprocess
from pathlib import Path
import sqlite3
import shutil
from typing import List, Dict, Optional, Any

console = Console()

# Configuration
CONFIG_DIR = os.path.expanduser("~/.config/wnote")
DB_PATH = os.path.join(CONFIG_DIR, "notes.db")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
ATTACHMENTS_DIR = os.path.join(CONFIG_DIR, "attachments")

os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(ATTACHMENTS_DIR, exist_ok=True)

DEFAULT_CONFIG = {
    "editor": os.environ.get("EDITOR", "nano"),
    "default_color": "white",
    "file_opener": "xdg-open",  # xdg-open for Linux, "open" for macOS, "start" for Windows
    "tag_colors": {
        "work": "blue",
        "personal": "green",
        "urgent": "red",
        "idea": "yellow",
        "task": "cyan",
        "file": "bright_blue",
        "folder": "bright_yellow",
    }
}

def init_db():
    """Initialize the database if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create notes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create tags table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    ''')
    
    # Create note_tags table (many-to-many relationship)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS note_tags (
        note_id INTEGER,
        tag_id INTEGER,
        PRIMARY KEY (note_id, tag_id),
        FOREIGN KEY (note_id) REFERENCES notes (id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
    )
    ''')
    
    # Create attachments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attachments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        note_id INTEGER NOT NULL,
        filename TEXT NOT NULL,
        original_path TEXT NOT NULL,
        stored_path TEXT NOT NULL,
        is_directory INTEGER NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (note_id) REFERENCES notes (id) ON DELETE CASCADE
    )
    ''')
    
    conn.commit()
    conn.close()

def load_config():
    """Load or create configuration file."""
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG
    
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def save_config(config):
    """Save configuration to file."""
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

def get_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_tag_id(tag_name):
    """Get tag ID or create if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
    result = cursor.fetchone()
    
    if result:
        tag_id = result['id']
    else:
        cursor.execute("INSERT INTO tags (name) VALUES (?)", (tag_name,))
        tag_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return tag_id

def format_datetime(dt_str):
    """Format datetime string for display."""
    dt = datetime.datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    return dt.strftime("%d/%m/%Y %H:%M")

def get_tag_color(tag, config):
    """Get color for a tag, use default if not specified."""
    return config['tag_colors'].get(tag, config['default_color'])

def create_note(title, content, tags=None):
    """Create a new note with optional tags."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        (title, content)
    )
    note_id = cursor.lastrowid
    
    if tags:
        for tag in tags:
            tag_id = get_tag_id(tag)
            cursor.execute(
                "INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)",
                (note_id, tag_id)
            )
    
    conn.commit()
    conn.close()
    return note_id

def get_notes(note_id=None, tag=None):
    """Get all notes or a specific note by ID or tag."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if note_id:
        cursor.execute("""
            SELECT n.*, GROUP_CONCAT(t.name) as tags
            FROM notes n
            LEFT JOIN note_tags nt ON n.id = nt.note_id
            LEFT JOIN tags t ON nt.tag_id = t.id
            WHERE n.id = ?
            GROUP BY n.id
        """, (note_id,))
        notes = [dict(row) for row in cursor.fetchall()]
    elif tag:
        cursor.execute("""
            SELECT n.*, GROUP_CONCAT(t2.name) as tags
            FROM notes n
            JOIN note_tags nt ON n.id = nt.note_id
            JOIN tags t ON nt.tag_id = t.id
            LEFT JOIN note_tags nt2 ON n.id = nt2.note_id
            LEFT JOIN tags t2 ON nt2.tag_id = t2.id
            WHERE t.name = ?
            GROUP BY n.id
            ORDER BY n.updated_at DESC
        """, (tag,))
        notes = [dict(row) for row in cursor.fetchall()]
    else:
        cursor.execute("""
            SELECT n.*, GROUP_CONCAT(t.name) as tags
            FROM notes n
            LEFT JOIN note_tags nt ON n.id = nt.note_id
            LEFT JOIN tags t ON nt.tag_id = t.id
            GROUP BY n.id
            ORDER BY n.updated_at DESC
        """)
        notes = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    # Process tags from string to list
    for note in notes:
        if note['tags']:
            note['tags'] = note['tags'].split(',')
        else:
            note['tags'] = []
    
    return notes

def update_note(note_id, title=None, content=None, tags=None):
    """Update an existing note."""
    conn = get_connection()
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if title is not None:
        updates.append("title = ?")
        params.append(title)
    
    if content is not None:
        updates.append("content = ?")
        params.append(content)
    
    if updates:
        updates.append("updated_at = CURRENT_TIMESTAMP")
        query = f"UPDATE notes SET {', '.join(updates)} WHERE id = ?"
        params.append(note_id)
        cursor.execute(query, params)
    
    if tags is not None:
        # Remove existing tags
        cursor.execute("DELETE FROM note_tags WHERE note_id = ?", (note_id,))
        
        # Add new tags
        for tag in tags:
            tag_id = get_tag_id(tag)
            cursor.execute(
                "INSERT INTO note_tags (note_id, tag_id) VALUES (?, ?)",
                (note_id, tag_id)
            )
    
    conn.commit()
    conn.close()

def delete_note(note_id):
    """Delete a note by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get any attachments to delete from disk
    cursor.execute("SELECT stored_path FROM attachments WHERE note_id = ?", (note_id,))
    attachments = cursor.fetchall()
    
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    
    conn.commit()
    conn.close()
    
    # Delete attachment files from disk
    for attachment in attachments:
        stored_path = attachment['stored_path']
        if os.path.exists(stored_path):
            if os.path.isdir(stored_path):
                shutil.rmtree(stored_path)
            else:
                os.remove(stored_path)
            
    return True

def get_all_tags():
    """Get all existing tags."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM tags ORDER BY name")
    tags = [row['name'] for row in cursor.fetchall()]
    
    conn.close()
    return tags

def add_attachment(note_id, file_path):
    """Add a file or directory attachment to a note."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Make sure the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File or directory not found: {file_path}")
    
    # Create a unique filename in the attachments directory
    filename = os.path.basename(file_path)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_name = f"{note_id}_{timestamp}_{filename}"
    attachment_path = os.path.join(ATTACHMENTS_DIR, unique_name)
    
    is_directory = os.path.isdir(file_path)
    
    # Copy the file or directory to the attachments directory
    if is_directory:
        shutil.copytree(file_path, attachment_path)
    else:
        shutil.copy2(file_path, attachment_path)
    
    # Record the attachment in the database
    cursor.execute("""
        INSERT INTO attachments (note_id, filename, original_path, stored_path, is_directory)
        VALUES (?, ?, ?, ?, ?)
    """, (note_id, filename, os.path.abspath(file_path), attachment_path, 1 if is_directory else 0))
    
    conn.commit()
    conn.close()
    return True

def get_attachments(note_id):
    """Get all attachments for a note."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM attachments
        WHERE note_id = ?
        ORDER BY created_at
    """, (note_id,))
    
    attachments = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return attachments

def open_attachment(attachment):
    """Open a file or directory attachment."""
    file_path = attachment['stored_path']
    
    if not os.path.exists(file_path):
        console.print(f"[bold red]Attachment not found: {file_path}[/bold red]")
        return False
    
    try:
        # Use the configured file opener
        subprocess.run([config['file_opener'], file_path], check=False)
        return True
    except Exception as e:
        console.print(f"[bold red]Error opening attachment: {e}[/bold red]")
        return False

# Initialize
init_db()
config = load_config()

# CLI Group
@click.group()
def cli():
    """WNote - Terminal Note Taking Application"""
    pass

@cli.command()
@click.argument('title')
@click.option('--content', '-c', help='Note content (if not provided, will open editor)')
@click.option('--tags', '-t', help='Comma separated tags')
@click.option('--file', '-f', help='Attach a file or directory to the note')
def add(title, content, tags, file):
    """Add a new note"""
    if not content:
        # Create a temporary file and open it in the editor
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp:
            temp_path = temp.name
        
        # Open the editor
        editor = config['editor']
        try:
            subprocess.run([editor, temp_path], check=True)
            
            # Read the content from the file
            with open(temp_path, 'r') as f:
                content = f.read()
            
            # Remove the temporary file
            os.unlink(temp_path)
        except Exception as e:
            console.print(f"[bold red]Error opening editor: {e}[/bold red]")
            return
    
    tag_list = []
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',')]
    
    # Add file/folder type tag if attaching
    if file:
        if os.path.isdir(file):
            if 'folder' not in tag_list:
                tag_list.append('folder')
        else:
            if 'file' not in tag_list:
                tag_list.append('file')
    
    note_id = create_note(title, content, tag_list)
    
    # Add file attachment if provided
    if file:
        try:
            add_attachment(note_id, file)
            file_type = "folder" if os.path.isdir(file) else "file"
            console.print(f"[bold green]Attached {file_type}: {file}[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error attaching file: {e}[/bold red]")
    
    console.print(f"[bold green]Note created with ID: {note_id}[/bold green]")

@cli.command()
@click.argument('note_id', type=int)
@click.argument('file_path')
def attach(note_id, file_path):
    """Attach a file or directory to an existing note"""
    # Check if note exists
    notes = get_notes(note_id=note_id)
    if not notes:
        console.print(f"[bold red]Note with ID {note_id} not found[/bold red]")
        return
    
    # Add appropriate tag
    note_tags = notes[0].get('tags', [])
    if os.path.isdir(file_path):
        if 'folder' not in note_tags:
            note_tags.append('folder')
    else:
        if 'file' not in note_tags:
            note_tags.append('file')
    
    update_note(note_id, tags=note_tags)
    
    # Add the attachment
    try:
        add_attachment(note_id, file_path)
        file_type = "folder" if os.path.isdir(file_path) else "file"
        console.print(f"[bold green]Attached {file_type} to note {note_id}: {file_path}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")

@cli.command()
@click.argument('note_id', type=int, required=False)
@click.option('--tag', '-t', help='Filter notes by tag')
@click.option('--open-attachments', '-o', is_flag=True, help='Automatically open all attachments')
def show(note_id, tag, open_attachments):
    """Show notes (all, by ID, or by tag)"""
    if note_id:
        notes = get_notes(note_id=note_id)
        if not notes:
            console.print(f"[bold red]Note with ID {note_id} not found[/bold red]")
            return
        
        note = notes[0]
        
        # Format tags with colors
        formatted_tags = []
        for tag in note.get('tags', []):
            color = get_tag_color(tag, config)
            formatted_tags.append(f"[{color}]{tag}[/{color}]")
        
        tag_display = " ".join(formatted_tags) if formatted_tags else ""
        
        # Create a panel for the note
        title = Text(f"#{note['id']} - {note['title']}")
        if tag_display:
            title.append(" - ")
            title.append(Text.from_markup(tag_display))
        
        panel = Panel(
            note['content'],
            title=title,
            subtitle=f"Created: {format_datetime(note['created_at'])} | Updated: {format_datetime(note['updated_at'])}",
            box=box.ROUNDED
        )
        console.print(panel)
        
        # Show attachments
        attachments = get_attachments(note_id)
        if attachments:
            console.print("\n[bold]Attachments:[/bold]")
            
            table = Table(box=box.ROUNDED)
            table.add_column("#", style="cyan", no_wrap=True)
            table.add_column("Filename", style="green")
            table.add_column("Type", style="magenta")
            table.add_column("Original Path", style="white")
            
            for i, attachment in enumerate(attachments):
                file_type = "Directory" if attachment['is_directory'] else "File"
                color = "bright_yellow" if attachment['is_directory'] else "bright_blue"
                
                table.add_row(
                    str(i + 1),
                    attachment['filename'],
                    f"[{color}]{file_type}[/{color}]",
                    attachment['original_path']
                )
            
            console.print(table)
            
            # Open attachments if requested or ask if not specified
            if open_attachments:
                for attachment in attachments:
                    open_attachment(attachment)
            else:
                console.print("\n[bold]Would you like to open any attachments?[/bold]")
                console.print("Enter the number of the attachment to open, 'all' to open all, or press Enter to skip:")
                choice = click.prompt("Choice", default="", show_default=False)
                
                if choice.lower() == 'all':
                    for attachment in attachments:
                        open_attachment(attachment)
                elif choice and choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(attachments):
                        open_attachment(attachments[idx])
                    else:
                        console.print("[bold red]Invalid selection[/bold red]")
    else:
        notes = get_notes(tag=tag)
        
        if not notes:
            message = "No notes found"
            if tag:
                message += f" with tag '{tag}'"
            console.print(f"[bold yellow]{message}[/bold yellow]")
            return
        
        table = Table(box=box.ROUNDED)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="green")
        table.add_column("Tags", no_wrap=True)
        table.add_column("Updated", style="magenta")
        table.add_column("Attachments", style="bright_blue")
        table.add_column("Preview", style="white")
        
        for note in notes:
            # Format tags with colors
            formatted_tags = []
            for tag in note.get('tags', []):
                color = get_tag_color(tag, config)
                formatted_tags.append(f"[{color}]{tag}[/{color}]")
            
            tag_display = " ".join(formatted_tags) if formatted_tags else ""
            
            # Count attachments
            attachments = get_attachments(note['id'])
            attachment_count = len(attachments)
            attachment_display = f"{attachment_count}" if attachment_count > 0 else ""
            
            # Create a preview of the content (first 40 characters)
            preview = note['content'].replace('\n', ' ')
            if len(preview) > 40:
                preview = preview[:37] + "..."
            
            table.add_row(
                str(note['id']),
                note['title'],
                tag_display,
                format_datetime(note['updated_at']),
                attachment_display,
                preview
            )
        
        console.print(table)

@cli.command()
@click.argument('note_id', type=int)
def edit(note_id):
    """Edit a note by ID"""
    notes = get_notes(note_id=note_id)
    if not notes:
        console.print(f"[bold red]Note with ID {note_id} not found[/bold red]")
        return
    
    note = notes[0]
    
    # Create a temporary file with the note content
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp:
        temp.write(note['content'].encode())
        temp_path = temp.name
    
    # Open the editor
    editor = config['editor']
    try:
        subprocess.run([editor, temp_path], check=True)
        
        # Read the updated content
        with open(temp_path, 'r') as f:
            new_content = f.read()
        
        # Remove the temporary file
        os.unlink(temp_path)
        
        # Update the note
        update_note(note_id, content=new_content)
        console.print(f"[bold green]Note {note_id} updated[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error opening editor: {e}[/bold red]")

@cli.command()
@click.argument('note_id', type=int)
@click.option('--title', '-t', help='New title')
@click.option('--tags', help='Comma separated tags')
def update(note_id, title, tags):
    """Update a note's title or tags"""
    notes = get_notes(note_id=note_id)
    if not notes:
        console.print(f"[bold red]Note with ID {note_id} not found[/bold red]")
        return
    
    tag_list = None
    if tags is not None:
        tag_list = [tag.strip() for tag in tags.split(',')]
    
    update_note(note_id, title=title, tags=tag_list)
    console.print(f"[bold green]Note {note_id} updated[/bold green]")

@cli.command()
@click.argument('note_id', type=int)
@click.option('--force', '-f', is_flag=True, help='Delete without confirmation')
def delete(note_id, force):
    """Delete a note by ID"""
    notes = get_notes(note_id=note_id)
    if not notes:
        console.print(f"[bold red]Note with ID {note_id} not found[/bold red]")
        return
    
    note = notes[0]
    
    if not force:
        console.print(f"[bold yellow]Are you sure you want to delete note #{note_id} - {note['title']}?[/bold yellow]")
        confirm = click.confirm("Delete?")
        if not confirm:
            console.print("[yellow]Deletion cancelled[/yellow]")
            return
    
    success = delete_note(note_id)
    if success:
        console.print(f"[bold green]Note {note_id} deleted[/bold green]")
    else:
        console.print(f"[bold red]Failed to delete note {note_id}[/bold red]")

@cli.command()
def tags():
    """List all available tags"""
    all_tags = get_all_tags()
    
    if not all_tags:
        console.print("[bold yellow]No tags found[/bold yellow]")
        return
    
    table = Table(box=box.ROUNDED)
    table.add_column("Tag", style="white")
    table.add_column("Color", style="white")
    
    for tag in all_tags:
        color = get_tag_color(tag, config)
        table.add_row(f"[{color}]{tag}[/{color}]", color)
    
    console.print(table)

@cli.command()
@click.argument('tag', required=True)
@click.argument('color', required=True)
def color(tag, color):
    """Set color for a tag"""
    valid_colors = [
        "red", "green", "blue", "yellow", "magenta", "cyan", 
        "white", "black", "bright_red", "bright_green", 
        "bright_blue", "bright_yellow", "bright_magenta", 
        "bright_cyan", "bright_white"
    ]
    
    if color not in valid_colors:
        console.print(f"[bold red]Invalid color. Choose from: {', '.join(valid_colors)}[/bold red]")
        return
    
    config['tag_colors'][tag] = color
    save_config(config)
    console.print(f"[bold green]Color for tag '{tag}' set to [{color}]{color}[/{color}][/bold green]")

@cli.command()
def config():
    """View or edit configuration"""
    console.print(Panel(json.dumps(config, indent=2), title="Current Configuration", box=box.ROUNDED))
    console.print("\n[bold]To set tag colors, use the 'wnote color <tag> <color>' command.[/bold]")
    console.print("[bold]To set the default editor, edit the config file directly at:[/bold]")
    console.print(f"[bold]{CONFIG_PATH}[/bold]")

@cli.command()
@click.argument('command', required=False, type=click.Choice(['setup', 'push', 'pull']))
@click.argument('provider', required=False, type=click.Choice(['dropbox']))
def sync(command, provider):
    """Sync notes with Dropbox"""
    try:
        from . import wnote_sync
    except ImportError:
        # Try to import from the same directory during development
        try:
            import wnote_sync
        except ImportError:
            console.print("[bold red]Error: wnote_sync module not found.[/bold red]")
            console.print("[yellow]Make sure the package is installed correctly.[/yellow]")
            return

    if not command:
        console.print("[bold]WNote Sync[/bold]")
        console.print("\nUsage: wnote sync [command] [provider]")
        console.print("\nCommands:")
        console.print("  setup   Configure sync settings")
        console.print("  push    Push notes to remote storage")
        console.print("  pull    Pull notes from remote storage")
        console.print("\nProviders:")
        console.print("  dropbox   Sync with Dropbox")
        return

    if not provider:
        console.print("[bold red]Error: Provider is required.[/bold red]")
        return

    # Set up arguments for wnote_sync
    sys_args = [command, provider]
    wnote_sync.main(sys_args)

if __name__ == "__main__":
    cli() 