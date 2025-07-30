#!/usr/bin/env python3
import os
import sys
import json
import shutil
import requests
import argparse
import time
from pathlib import Path
from datetime import datetime
import configparser
import base64

CONFIG_DIR = os.path.expanduser("~/.config/wnote")
CONFIG_FILE = os.path.join(CONFIG_DIR, "sync_config.ini")
DB_PATH = os.path.join(CONFIG_DIR, "notes.db")
ATTACHMENTS_DIR = os.path.join(CONFIG_DIR, "attachments")
BACKUP_DIR = os.path.join(CONFIG_DIR, "backups")

os.makedirs(BACKUP_DIR, exist_ok=True)

def create_default_config():
    config = configparser.ConfigParser()
    
    config['DROPBOX'] = {
        'enabled': 'false',
        'token': '',
        'folder': '/wnote',
        'sync_frequency': '3600'  # seconds
    }
    
    config['GENERAL'] = {
        'last_sync': '0',
        'sync_attachments': 'true',
        'auto_sync': 'false'
    }
    
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)
    
    print(f"Created default sync config at {CONFIG_FILE}")
    return config

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return create_default_config()
    
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def backup_database():
    """Create a backup of the current database"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"notes_{timestamp}.db")
    shutil.copy2(DB_PATH, backup_path)
    print(f"Database backed up to {backup_path}")
    return backup_path

def setup_dropbox_sync():
    """Setup Dropbox sync configuration"""
    config = load_config()
    
    print("Visit https://www.dropbox.com/developers/apps to create an app and get a token")
    token = input("Enter your Dropbox access token: ")
    folder = input("Enter Dropbox folder path [/wnote]: ") or "/wnote"
    
    config['DROPBOX']['enabled'] = 'true'
    config['DROPBOX']['token'] = token
    config['DROPBOX']['folder'] = folder
    
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)
    
    print("Dropbox sync configured successfully!")

def sync_to_dropbox():
    """Sync database to Dropbox"""
    config = load_config()
    
    if config['DROPBOX']['enabled'] != 'true':
        print("Dropbox sync is not enabled. Run 'wnote sync --setup dropbox' first.")
        return
    
    token = config['DROPBOX']['token']
    folder = config['DROPBOX']['folder']
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/octet-stream"
    }
    
    # Upload database
    with open(DB_PATH, 'rb') as f:
        db_content = f.read()
    
    params = {
        "path": f"{folder}/notes.db",
        "mode": "overwrite"
    }
    
    response = requests.post(
        "https://content.dropboxapi.com/2/files/upload",
        headers={
            "Authorization": f"Bearer {token}",
            "Dropbox-API-Arg": json.dumps(params),
            "Content-Type": "application/octet-stream"
        },
        data=db_content
    )
    
    if response.status_code != 200:
        print(f"Error uploading database: {response.text}")
        return
    
    # Update config
    config['GENERAL']['last_sync'] = str(int(time.time()))
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)
    
    print(f"Successfully synced to Dropbox folder {folder}")

def sync_from_dropbox():
    """Sync database from Dropbox"""
    config = load_config()
    
    if config['DROPBOX']['enabled'] != 'true':
        print("Dropbox sync is not enabled. Run 'wnote sync --setup dropbox' first.")
        return
    
    # Backup current database
    backup_database()
    
    token = config['DROPBOX']['token']
    folder = config['DROPBOX']['folder']
    
    # Download database
    params = {
        "path": f"{folder}/notes.db"
    }
    
    response = requests.post(
        "https://content.dropboxapi.com/2/files/download",
        headers={
            "Authorization": f"Bearer {token}",
            "Dropbox-API-Arg": json.dumps(params)
        }
    )
    
    if response.status_code != 200:
        print(f"Error downloading database: {response.text}")
        return
    
    with open(DB_PATH, 'wb') as f:
        f.write(response.content)
    
    # Update config
    config['GENERAL']['last_sync'] = str(int(time.time()))
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)
    
    print(f"Successfully synced from Dropbox folder {folder}")

def main(args=None):
    """Main function for sync module.
    
    Args:
        args: List of command line arguments, can be passed from wnote.py
    """
    parser = argparse.ArgumentParser(description="WNote Sync Tool")
    subparsers = parser.add_subparsers(dest="command", help="Sync commands")
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Setup sync configuration")
    setup_parser.add_argument("provider", choices=["dropbox"], help="Sync provider")
    
    # Push command
    push_parser = subparsers.add_parser("push", help="Push notes to remote")
    push_parser.add_argument("provider", choices=["dropbox"], help="Sync provider")
    
    # Pull command
    pull_parser = subparsers.add_parser("pull", help="Pull notes from remote")
    pull_parser.add_argument("provider", choices=["dropbox"], help="Sync provider")
    
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)
    
    if args.command is None:
        parser.print_help()
        return
    
    if args.command == "setup":
        if args.provider == "dropbox":
            setup_dropbox_sync()
    
    elif args.command == "push":
        if args.provider == "dropbox":
            sync_to_dropbox()
    
    elif args.command == "pull":
        if args.provider == "dropbox":
            sync_from_dropbox()

if __name__ == "__main__":
    main() 