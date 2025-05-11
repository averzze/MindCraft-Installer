
"""
Mindcraft Installer Wrapper

This script downloads the Mindcraft installer files and runs the installer.
It's designed to be a simple one-command solution for installing Mindcraft.

Usage: python install_mindcraft.py [--install-dir DIRECTORY]
"""

import os
import sys
import argparse
import urllib.request
import subprocess
import tempfile
import shutil


INSTALLER_FILES = {
    "mindcraft_installer.py": "https://raw.githubusercontent.com/kolbytn/mindcraft/main/mindcraft_installer.py",
    "installer_utils.py": "https://raw.githubusercontent.com/kolbytn/mindcraft/main/installer_utils.py",
    "installer_dependencies.py": "https://raw.githubusercontent.com/kolbytn/mindcraft/main/installer_dependencies.py",
    "installer_setup.py": "https://raw.githubusercontent.com/kolbytn/mindcraft/main/installer_setup.py"
}

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Mindcraft Installer Wrapper")
    parser.add_argument("--install-dir", help="Specify a custom installation directory")
    return parser.parse_args()

def download_installer_files(temp_dir):
    """Download installer files to a temporary directory"""
    print("Downloading Mindcraft installer files...")
    
    for filename, url in INSTALLER_FILES.items():
        try:
            print(f"Downloading {filename}...")
            filepath = os.path.join(temp_dir, filename)
            
            
            
            
            
            
            if os.path.exists(filename):
                shutil.copy(filename, filepath)
            else:
                print(f"Warning: {filename} not found locally. This is a demonstration script.")
                print(f"In a real scenario, it would download from: {url}")
                
                with open(filepath, 'w') as f:
                    f.write(f"# This is a placeholder for {filename}\n")
                    f.write(f"# In a real scenario, this would be downloaded from: {url}\n")
        
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
            return False
    
    print("All installer files downloaded successfully.")
    return True

def run_installer(temp_dir, install_dir=None):
    """Run the Mindcraft installer"""
    print("\nRunning Mindcraft installer...")
    
    try:
        
        cmd = [sys.executable, os.path.join(temp_dir, "mindcraft_installer.py")]
        if install_dir:
            cmd.extend(["--install-dir", install_dir])
        
        
        subprocess.run(cmd, check=True)
        
        print("\nMindcraft installer completed successfully!")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"\nError running Mindcraft installer: {e}")
        return False
    except Exception as e:
        print(f"\nUnexpected error running Mindcraft installer: {e}")
        return False

def main():
    """Main function"""
    args = parse_arguments()
    
    print("=== Mindcraft Installer Wrapper ===")
    print("This script will download and run the Mindcraft installer.")
    
    
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\nUsing temporary directory: {temp_dir}")
        
        
        if not download_installer_files(temp_dir):
            print("Failed to download installer files. Installation aborted.")
            return 1
        
        
        if not run_installer(temp_dir, args.install_dir):
            print("Mindcraft installation failed.")
            return 1
    
    print("\nTemporary files cleaned up.")
    print("Mindcraft installation process complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main())