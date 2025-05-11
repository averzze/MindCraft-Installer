
"""
Mindcraft Installer Dependencies

This module contains functions for checking and installing dependencies required by Mindcraft.
"""

import os
import platform
import re
import time
import urllib.request
from installer_utils import (
    MIN_NODE_VERSION, NODE_DOWNLOAD_URLS, GIT_DOWNLOAD_URLS,
    run_command, download_file
)

class DependencyInstaller:
    """Class for checking and installing dependencies"""
    
    def __init__(self, logger):
        self.logger = logger
        self.system = platform.system()
    
    def check_git_installed(self):
        """Check if Git is installed and return version if it is"""
        try:
            success, output = run_command("git --version", logger=self.logger)
            if success:
                match = re.search(r'git version (\d+\.\d+\.\d+)', output)
                if match:
                    version = match.group(1)
                    self.logger.log(f"Git version {version} is installed")
                    return True, version
            self.logger.log("Git is not installed", "WARNING")
            return False, None
        except Exception as e:
            self.logger.log(f"Error checking Git installation: {e}", "ERROR")
            return False, None
    
    def ensure_download_dir(self):
        """Ensure download directory exists"""
        download_dir = os.path.join(os.getcwd(), "dist")
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        return download_dir
        
    def install_git(self):
        """Install Git based on the operating system"""
        self.logger.log("Installing Git...")
        
        if self.system == "Windows":
            
            download_dir = self.ensure_download_dir()
            
            
            git_installer = os.path.join(download_dir, "git_installer.exe")
            self.logger.log(f"Downloading Git installer from {GIT_DOWNLOAD_URLS['Windows']}...")
            
            try:
                if not download_file(GIT_DOWNLOAD_URLS['Windows'], git_installer, self.logger):
                    return False
                
                self.logger.log("Download complete. Running installer...")
                self.logger.log("Please follow the Git installation wizard to complete the installation.", "INFO")
                self.logger.log("IMPORTANT: Make sure to select the option to add Git to your PATH.", "INFO")
                
                
                success, output = run_command([git_installer], logger=self.logger)
                
                if not success:
                    self.logger.log("Failed to launch Git installer.", "ERROR")
                    self.logger.log("Please install Git manually from https://git-scm.com/download/win", "ERROR")
                    return False
                
                
                self.logger.log("Waiting for you to complete the Git installation wizard...", "INFO")
                
                
                git_paths = [
                    "C:\\Program Files\\Git\\cmd",
                    "C:\\Program Files\\Git\\bin",
                    "C:\\Program Files (x86)\\Git\\cmd",
                    "C:\\Program Files (x86)\\Git\\bin"
                ]
                for path in git_paths:
                    if os.path.exists(path) and path not in os.environ['PATH']:
                        os.environ['PATH'] = f"{path};{os.environ['PATH']}"
                
                
                git_installed, _ = self.check_git_installed()
                if git_installed:
                    self.logger.log("Git installed successfully.")
                    return True
                else:
                    self.logger.log("Git installation may have failed or Git is not in your PATH.", "WARNING")
                    self.logger.log("Do you want to continue anyway? (y/n)", "INFO")
                    response = input("Continue? (y/n): ")
                    if response.lower() == 'y':
                        return True
                    else:
                        self.logger.log("Installation aborted by user.", "ERROR")
                        return False
                
            except Exception as e:
                self.logger.log(f"Error downloading or installing Git: {e}", "ERROR")
                self.logger.log("Please install Git manually from https://git-scm.com/download/win", "ERROR")
                return False
                
        elif self.system == "Darwin":  
            
            success, _ = run_command("which brew", logger=self.logger)
            if success:
                self.logger.log("Homebrew detected, attempting to install Git...")
                success, output = run_command("brew install git", logger=self.logger)
                if success:
                    self.logger.log("Git installed successfully using Homebrew.")
                    return True
            
            
            self.logger.log("Attempting to install Xcode Command Line Tools...")
            success, output = run_command("xcode-select --install", logger=self.logger)
            
            self.logger.log("Waiting for Xcode Command Line Tools installation to complete...")
            self.logger.log("This may take several minutes. Please complete the installation if prompted.")
            
            
            time.sleep(30)  
            
            git_installed, _ = self.check_git_installed()
            if git_installed:
                self.logger.log("Git installed successfully.")
                return True
            else:
                self.logger.log("Git installation may have failed.", "WARNING")
                self.logger.log("Please install Git manually using one of these methods:", "WARNING")
                self.logger.log("1. Download and install from: https://git-scm.com/download/mac", "WARNING")
                self.logger.log("2. Install using Homebrew: brew install git", "WARNING")
                self.logger.log("3. Install Xcode Command Line Tools: xcode-select --install", "WARNING")
                return False
            
        elif self.system == "Linux":
            
            package_managers = {
                "apt-get": "sudo apt-get update && sudo apt-get install -y git",
                "dnf": "sudo dnf install -y git",
                "yum": "sudo yum install -y git",
                "pacman": "sudo pacman -Sy git --noconfirm",
                "zypper": "sudo zypper install -y git"
            }
            
            for pm, cmd in package_managers.items():
                success, _ = run_command(f"which {pm}", logger=self.logger)
                if success:
                    self.logger.log(f"Detected package manager: {pm}")
                    success, output = run_command(cmd, shell=True, logger=self.logger)
                    if success:
                        self.logger.log("Git installed successfully.")
                        return True
                    else:
                        self.logger.log(f"Failed to install Git using {pm}.", "ERROR")
                        self.logger.log(f"Error: {output}", "ERROR")
            
            self.logger.log("Could not automatically install Git.", "ERROR")
            self.logger.log("Please install Git manually using your distribution's package manager.", "ERROR")
            return False
        
        return False
    
    def check_node_installed(self):
        """Check if Node.js is installed and return version if it is"""
        try:
            success, output = run_command("node --version", logger=self.logger)
            if success:
                
                version = output.strip().lstrip('v')
                major_version = int(version.split('.')[0])
                
                if major_version >= MIN_NODE_VERSION:
                    self.logger.log(f"Node.js version {version} is installed")
                    return True, version
                else:
                    self.logger.log(f"Node.js version {version} is installed, but version {MIN_NODE_VERSION} or higher is required.", "WARNING")
                    return False, version
            self.logger.log("Node.js is not installed", "WARNING")
            return False, None
        except Exception as e:
            self.logger.log(f"Error checking Node.js installation: {e}", "ERROR")
            return False, None
    
    def check_npm_installed(self):
        """Check if npm is installed and return version if it is"""
        try:
            
            if self.system == "Windows":
                
                npm_paths = [
                    "npm",  
                    os.path.join("C:\\Program Files\\nodejs", "npm.cmd"),
                    os.path.join("C:\\Program Files (x86)\\nodejs", "npm.cmd"),
                    os.path.join(os.environ.get("APPDATA", ""), "npm", "npm.cmd")
                ]
                
                for npm_path in npm_paths:
                    self.logger.log(f"Trying npm at: {npm_path}")
                    success, output = run_command(f"{npm_path} --version", shell=True, logger=self.logger)
                    if success:
                        version = output.strip()
                        self.logger.log(f"npm version {version} is installed at {npm_path}")
                        return True, version
            else:
                
                success, output = run_command("npm --version", logger=self.logger)
                if success:
                    version = output.strip()
                    self.logger.log(f"npm version {version} is installed")
                    return True, version
            
            
            self.logger.log("npm is not installed or not in PATH", "WARNING")
            return False, None
        except Exception as e:
            self.logger.log(f"Error checking npm installation: {e}", "ERROR")
            return False, None
    
    def install_node(self):
        """Install Node.js based on the operating system"""
        self.logger.log("Installing Node.js...")
        
        if self.system == "Windows":
            
            download_dir = self.ensure_download_dir()
            
            
            node_installer = os.path.join(download_dir, "node_installer.msi")
            self.logger.log(f"Downloading Node.js installer from {NODE_DOWNLOAD_URLS['Windows']}...")
            
            try:
                if not download_file(NODE_DOWNLOAD_URLS['Windows'], node_installer, self.logger):
                    return False
                
                self.logger.log("Download complete. Running installer...")
                self.logger.log("Please follow the Node.js installation wizard to complete the installation.", "INFO")
                self.logger.log("IMPORTANT: Make sure to select the option to add Node.js to your PATH.", "INFO")
                
                
                install_cmd = f'msiexec /i "{node_installer}"'
                self.logger.log(f"Running command: {install_cmd}")
                success, output = run_command(install_cmd, shell=True, logger=self.logger)
                
                if not success:
                    self.logger.log("Failed to launch Node.js installer.", "ERROR")
                    self.logger.log("Please install Node.js manually from https://nodejs.org/", "ERROR")
                    return False
                
                
                self.logger.log("Waiting for you to complete the Node.js installation wizard...", "INFO")
                
                
                nodejs_paths = [
                    "C:\\Program Files\\nodejs",
                    "C:\\Program Files (x86)\\nodejs",
                    os.path.join(os.environ.get("APPDATA", ""), "npm")
                ]
                for path in nodejs_paths:
                    if os.path.exists(path) and path not in os.environ['PATH']:
                        os.environ['PATH'] = f"{path};{os.environ['PATH']}"
                
                
                node_installed, _ = self.check_node_installed()
                if node_installed:
                    self.logger.log("Node.js installed successfully.")
                    return True
                else:
                    self.logger.log("Node.js installation may have failed or Node.js is not in your PATH.", "WARNING")
                    self.logger.log("Do you want to continue anyway? (y/n)", "INFO")
                    response = input("Continue? (y/n): ")
                    if response.lower() == 'y':
                        return True
                    else:
                        self.logger.log("Installation aborted by user.", "ERROR")
                        return False
                
            except Exception as e:
                self.logger.log(f"Error downloading or installing Node.js: {e}", "ERROR")
                self.logger.log("Please install Node.js manually from https://nodejs.org/", "ERROR")
                return False
                
        elif self.system == "Darwin":  
            
            success, _ = run_command("which brew", logger=self.logger)
            if success:
                self.logger.log("Homebrew detected, attempting to install Node.js...")
                success, output = run_command("brew install node", logger=self.logger)
                if success:
                    self.logger.log("Node.js installed successfully using Homebrew.")
                    return True
            
            self.logger.log("Could not automatically install Node.js.", "ERROR")
            self.logger.log("Please install Node.js manually using one of these methods:", "ERROR")
            self.logger.log("1. Download and install from: https://nodejs.org/", "ERROR")
            self.logger.log("2. Install using Homebrew: brew install node", "ERROR")
            return False
            
        elif self.system == "Linux":
            
            package_managers = {
                "apt-get": "curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs",
                "dnf": "sudo dnf install -y nodejs",
                "yum": "curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash - && sudo yum install -y nodejs",
                "pacman": "sudo pacman -Sy nodejs npm --noconfirm",
                "zypper": "sudo zypper install -y nodejs npm"
            }
            
            for pm, cmd in package_managers.items():
                success, _ = run_command(f"which {pm}", logger=self.logger)
                if success:
                    self.logger.log(f"Detected package manager: {pm}")
                    success, output = run_command(cmd, shell=True, logger=self.logger)
                    if success:
                        self.logger.log("Node.js installed successfully.")
                        return True
                    else:
                        self.logger.log(f"Failed to install Node.js using {pm}.", "ERROR")
                        self.logger.log(f"Error: {output}", "ERROR")
            
            self.logger.log("Could not automatically install Node.js.", "ERROR")
            self.logger.log("Please install Node.js manually from https://nodejs.org/ or using your distribution's package manager.", "ERROR")
            return False
        
        return False
    
    def install_python_dependencies(self, install_dir):
        """Install Python dependencies"""
        self.logger.log("Installing Python dependencies...")
        
        requirements_file = os.path.join(install_dir, "requirements.txt")
        if not os.path.exists(requirements_file):
            self.logger.log(f"Requirements file not found: {requirements_file}", "ERROR")
            return False
        
        success, output = run_command(f"pip install -r {requirements_file}", shell=True, cwd=install_dir, logger=self.logger)
        if not success:
            self.logger.log(f"Failed to install Python dependencies: {output}", "ERROR")
            return False
        
        self.logger.log("Python dependencies installed successfully.")
        return True
    
    def run_npm_install(self, install_dir):
        """Run npm install in the specified directory"""
        self.logger.log(f"Running npm install in {install_dir}...")
        
        
        if self.system == "Windows":
            npm_paths = [
                "npm",  
                os.path.join("C:\\Program Files\\nodejs", "npm.cmd"),
                os.path.join("C:\\Program Files (x86)\\nodejs", "npm.cmd"),
                os.path.join(os.environ.get("APPDATA", ""), "npm", "npm.cmd")
            ]
            
            for npm_path in npm_paths:
                self.logger.log(f"Trying npm install with: {npm_path}")
                success, output = run_command(f"{npm_path} install", shell=True, cwd=install_dir, logger=self.logger)
                if success:
                    self.logger.log("npm install completed successfully.")
                    return True
            
            
            node_paths = [
                "node",
                os.path.join("C:\\Program Files\\nodejs", "node.exe"),
                os.path.join("C:\\Program Files (x86)\\nodejs", "node.exe")
            ]
            
            for node_path in node_paths:
                npm_cli_path = os.path.join(install_dir, "node_modules", "npm", "bin", "npm-cli.js")
                if os.path.exists(npm_cli_path):
                    self.logger.log(f"Trying with Node.js directly: {node_path} {npm_cli_path} install")
                    success, output = run_command(f"{node_path} {npm_cli_path} install", shell=True, cwd=install_dir, logger=self.logger)
                    if success:
                        self.logger.log("npm install completed successfully.")
                        return True
        else:
            
            success, output = run_command("npm install", cwd=install_dir, logger=self.logger)
            if success:
                self.logger.log("npm install completed successfully.")
                return True
        
        self.logger.log(f"Failed to run npm install: {output}", "ERROR")
        return False
    
    def ensure_dependencies(self):
        """Ensure all dependencies are installed"""
        
        git_installed, _ = self.check_git_installed()
        if not git_installed:
            if not self.install_git():
                self.logger.log("Failed to install Git. Installation cannot continue.", "ERROR")
                return False
        
        
        node_installed, _ = self.check_node_installed()
        if not node_installed:
            if not self.install_node():
                self.logger.log("Failed to install Node.js. Installation cannot continue.", "ERROR")
                return False
        
        
        npm_installed, _ = self.check_npm_installed()
        if not npm_installed:
            self.logger.log("npm is not detected, but it should have been installed with Node.js.", "WARNING")
            self.logger.log("This might be a PATH issue. We'll continue with the installation anyway.", "WARNING")
        
        self.logger.log("All required dependencies are installed.")
        return True