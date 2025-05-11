
"""
Mindcraft Installer Utilities

This module contains utility functions and constants used by the Mindcraft installer.
"""

import os
import sys
import platform
import subprocess
import re
import time
import urllib.request
from urllib.error import URLError
from pathlib import Path


MIN_NODE_VERSION = 14
NODE_DOWNLOAD_URLS = {
    "Windows": "https://nodejs.org/dist/v18.18.2/node-v18.18.2-x64.msi",
    "Darwin": "https://nodejs.org/dist/v18.18.2/node-v18.18.2.pkg",
    "Linux": "https://nodejs.org/dist/v18.18.2/node-v18.18.2-linux-x64.tar.xz"
}
GIT_DOWNLOAD_URLS = {
    "Windows": "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe",
    "Darwin": "https://sourceforge.net/projects/git-osx-installer/files/git-2.33.0-intel-universal-mavericks.dmg",
    "Linux": None  
}
MINDCRAFT_REPO_URL = "https://github.com/kolbytn/mindcraft.git"


DEFAULT_INSTALL_DIRS = {
    "Windows": os.path.join(os.path.expanduser("~"), "Desktop", "mindcraft"),
    "Darwin": os.path.join(os.path.expanduser("~"), "Desktop", "mindcraft"),
    "Linux": os.path.join(os.path.expanduser("~"), "Desktop", "mindcraft")
}

class Logger:
    """Simple logging utility"""
    
    def __init__(self, log_file="mindcraft_installer.log"):
        self.log_file = log_file
        self.setup_logging()
    
    def setup_logging(self):
        """Set up logging to file"""
        with open(self.log_file, 'w') as f:
            f.write(f"Mindcraft Installer Log - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"System: {platform.system()} {platform.release()}\n")
            f.write(f"Python: {sys.version}\n\n")
    
    def log(self, message, level="INFO"):
        """Log a message to both console and log file"""
        log_message = f"[{level}] {message}"
        print(log_message)
        with open(self.log_file, 'a') as f:
            f.write(f"{log_message}\n")

def run_command(command, shell=False, cwd=None, logger=None):
    """Run a command and return its output"""
    if logger:
        logger.log(f"Running command: {command}")
    
    try:
        if isinstance(command, str) and not shell:
            command = command.split()
        
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=shell,
            cwd=cwd
        )
        
        if result.returncode != 0:
            if logger:
                logger.log(f"Command failed with return code {result.returncode}", "ERROR")
                logger.log(f"Error output: {result.stderr}", "ERROR")
            return False, result.stderr
        
        return True, result.stdout
    except Exception as e:
        if logger:
            logger.log(f"Exception running command: {e}", "ERROR")
        return False, str(e)

def download_file(url, destination, logger=None):
    """Download a file from a URL to a destination"""
    if logger:
        logger.log(f"Downloading {url} to {destination}")
    
    try:
        urllib.request.urlretrieve(url, destination)
        return True
    except Exception as e:
        if logger:
            logger.log(f"Failed to download {url}: {e}", "ERROR")
        return False

def create_directory(directory, logger=None):
    """Create a directory if it doesn't exist"""
    if not os.path.exists(directory):
        if logger:
            logger.log(f"Creating directory: {directory}")
        os.makedirs(directory, exist_ok=True)
        return True
    return False

def get_default_install_dir():
    """Get the default installation directory based on the operating system"""
    system = platform.system()
    default_dir = DEFAULT_INSTALL_DIRS.get(system, os.path.join(os.path.expanduser("~"), "Desktop", "mindcraft"))
    
    
    if os.path.exists(default_dir) and os.listdir(default_dir):
        
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        default_dir = f"{default_dir}-{timestamp}"
    
    return default_dir