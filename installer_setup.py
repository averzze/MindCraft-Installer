
"""
Mindcraft Installer Setup

This module contains functions for setting up the Mindcraft project.
"""

import os
import json
import shutil
import time
from installer_utils import (
    MINDCRAFT_REPO_URL, run_command, create_directory, get_default_install_dir
)

class ProjectSetup:
    """Class for setting up the Mindcraft project"""
    
    def __init__(self, logger):
        self.logger = logger
        self.install_dir = get_default_install_dir()
    
    def set_install_directory(self, custom_dir=None):
        """Set the installation directory"""
        if custom_dir:
            self.install_dir = custom_dir
        
        self.logger.log(f"Installation directory set to: {self.install_dir}")
        create_directory(self.install_dir, self.logger)
        return self.install_dir
    
    def clone_repository(self):
        """Copy the Mindcraft files from local directory"""
        
        self.logger.log("Copying Mindcraft files from local directory...")
        
        
        if not os.path.exists(self.install_dir):
            os.makedirs(self.install_dir, exist_ok=True)
            self.logger.log(f"Created installation directory: {self.install_dir}")
        
        
        if os.listdir(self.install_dir):
            self.logger.log(f"Warning: The directory {self.install_dir} is not empty.", "WARNING")
            
            
            self.logger.log("Do you want to continue and possibly overwrite existing files? (y/n)", "INFO")
            response = input("Continue? (y/n): ")
            
            if response.lower() != 'y':
                self.logger.log("Installation aborted by user.", "ERROR")
                return False
            
            
            self.logger.log(f"Clearing directory {self.install_dir}...", "INFO")
            for item in os.listdir(self.install_dir):
                item_path = os.path.join(self.install_dir, item)
                try:
                    if os.path.isfile(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        import shutil
                        shutil.rmtree(item_path)
                except Exception as e:
                    self.logger.log(f"Error clearing directory: {e}", "ERROR")
                    return False
        
        
        source_dir = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "mindcraft-main")
        
        if not os.path.exists(source_dir):
            
            source_dir = os.path.join(os.path.dirname(os.getcwd()), "mindcraft-main")
            if not os.path.exists(source_dir):
                self.logger.log(f"Could not find local mindcraft files at {source_dir}", "ERROR")
                
                
                self.logger.log("Falling back to cloning from GitHub...", "WARNING")
                success, output = run_command(f"git clone {MINDCRAFT_REPO_URL} .", cwd=self.install_dir, logger=self.logger)
                
                if not success:
                    self.logger.log(f"Failed to clone repository: {output}", "ERROR")
                    return False
                
                self.logger.log("Repository cloned successfully.")
                return True
        
        
        self.logger.log(f"Copying files from {source_dir} to {self.install_dir}...")
        
        try:
            
            success, output = run_command("git init", cwd=self.install_dir, logger=self.logger)
            if not success:
                self.logger.log(f"Failed to initialize git repository: {output}", "WARNING")
                
            
            
            for item in os.listdir(source_dir):
                source_item = os.path.join(source_dir, item)
                dest_item = os.path.join(self.install_dir, item)
                
                if os.path.isfile(source_item):
                    shutil.copy2(source_item, dest_item)
                elif os.path.isdir(source_item):
                    shutil.copytree(source_item, dest_item, dirs_exist_ok=True)
            
            
            if success:
                run_command("git add .", cwd=self.install_dir, logger=self.logger)
                run_command("git config --global user.email \"installer@example.com\"", cwd=self.install_dir, logger=self.logger)
                run_command("git config --global user.name \"Mindcraft Installer\"", cwd=self.install_dir, logger=self.logger)
                run_command("git commit -m 'Initial commit'", cwd=self.install_dir, logger=self.logger)
            
            
            main_js_path = os.path.join(self.install_dir, "main.js")
            if not os.path.exists(main_js_path):
                self.logger.log("main.js not found in the copied files. Falling back to cloning from GitHub...", "WARNING")
                
                
                for item in os.listdir(self.install_dir):
                    item_path = os.path.join(self.install_dir, item)
                    try:
                        if os.path.isfile(item_path):
                            os.unlink(item_path)
                        elif os.path.isdir(item_path):
                            import shutil
                            shutil.rmtree(item_path)
                    except Exception as e:
                        self.logger.log(f"Error clearing directory: {e}", "ERROR")
                
                
                success, output = run_command(f"git clone {MINDCRAFT_REPO_URL} .", cwd=self.install_dir, logger=self.logger)
                if not success:
                    self.logger.log(f"Failed to clone repository: {output}", "ERROR")
                    return False
                
                self.logger.log("Repository cloned successfully from GitHub.")
                return True
            
            self.logger.log("Files copied successfully.")
            return True
        except Exception as e:
            self.logger.log(f"Error copying files: {e}", "ERROR")
            
            
            self.logger.log("Falling back to cloning from GitHub...", "WARNING")
            success, output = run_command(f"git clone {MINDCRAFT_REPO_URL} .", cwd=self.install_dir, logger=self.logger)
            
            if not success:
                self.logger.log(f"Failed to clone repository: {output}", "ERROR")
                return False
            
            self.logger.log("Repository cloned successfully.")
            return True
    
    def install_node_dependencies(self):
        """Install Node.js dependencies"""
        self.logger.log("Installing Node.js dependencies...")
        
        
        from installer_dependencies import DependencyInstaller
        dependency_installer = DependencyInstaller(self.logger)
        
        
        if dependency_installer.run_npm_install(self.install_dir):
            self.logger.log("Node.js dependencies installed successfully.")
            return True
        
        self.logger.log("Failed to install Node.js dependencies. Will try again later.", "WARNING")
        
        return True
    
    def setup_keys_json(self):
        """Set up the keys.json file"""
        self.logger.log("Setting up keys.json file...")
        
        keys_example_path = os.path.join(self.install_dir, "keys.example.json")
        keys_path = os.path.join(self.install_dir, "keys.json")
        
        if not os.path.exists(keys_example_path):
            self.logger.log(f"keys.example.json not found at {keys_example_path}", "ERROR")
            return False
        
        try:
            
            shutil.copy(keys_example_path, keys_path)
            self.logger.log(f"Created keys.json from example file.")
            
            
            self.logger.log("NOTE: You will need to edit keys.json and add your own API keys before using Mindcraft.")
            self.logger.log("You need at least one of these API keys:")
            self.logger.log("- OpenAI API Key (https://openai.com/blog/openai-api)")
            self.logger.log("- Gemini API Key (https://aistudio.google.com/app/apikey)")
            self.logger.log("- Anthropic API Key (https://docs.anthropic.com/claude/docs/getting-access-to-claude)")
            self.logger.log("- Other supported API keys as listed in the README.md")
            
            return True
        except Exception as e:
            self.logger.log(f"Error setting up keys.json: {e}", "ERROR")
            return False
    
    def verify_installation(self):
        """Verify the installation"""
        self.logger.log("Verifying installation...")
        
        
        main_js_path = os.path.join(self.install_dir, "main.js")
        if not os.path.exists(main_js_path):
            self.logger.log(f"main.js not found at {main_js_path}", "ERROR")
            return False
        
        
        node_modules_path = os.path.join(self.install_dir, "node_modules")
        if not os.path.exists(node_modules_path):
            self.logger.log(f"node_modules directory not found at {node_modules_path}", "ERROR")
            return False
        
        
        keys_path = os.path.join(self.install_dir, "keys.json")
        if not os.path.exists(keys_path):
            self.logger.log(f"keys.json not found at {keys_path}", "ERROR")
            return False
        
        self.logger.log("Installation verified successfully.")
        return True
    
    def print_usage_instructions(self):
        """Print usage instructions"""
        self.logger.log("\n" + "="*80)
        self.logger.log("MINDCRAFT INSTALLATION COMPLETE")
        self.logger.log("="*80)
        self.logger.log(f"Mindcraft has been installed to: {self.install_dir}")
        self.logger.log("\nBefore using Mindcraft, you need to:")
        self.logger.log("1. Edit keys.json and add your API keys")
        self.logger.log("2. Start a Minecraft world and open it to LAN on localhost port 55916")
        self.logger.log("3. Run 'node main.js' from the installation directory")
        self.logger.log("\nFor more information, refer to the README.md file in the installation directory.")
        self.logger.log("="*80)
    
    def run_test(self):
        """Run a simple test to verify the installation"""
        self.logger.log("Running a simple test to verify the installation...")
        
        
        self.logger.log("Running npm install again to ensure all dependencies are installed...")
        from installer_dependencies import DependencyInstaller
        dependency_installer = DependencyInstaller(self.logger)
        dependency_installer.run_npm_install(self.install_dir)
        
        
        if os.name == 'nt':  
            node_paths = [
                "node",  
                os.path.join("C:\\Program Files\\nodejs", "node.exe"),
                os.path.join("C:\\Program Files (x86)\\nodejs", "node.exe")
            ]
            
            for node_path in node_paths:
                self.logger.log(f"Trying test with: {node_path}")
                success, output = run_command(f"{node_path} main.js --help", shell=True, cwd=self.install_dir, logger=self.logger)
                if success:
                    self.logger.log("Test completed successfully.")
                    self.logger.log("Note: This test only verifies that the code can run, not that it can connect to Minecraft.")
                    self.logger.log("You will need to start a Minecraft world and open it to LAN before running Mindcraft.")
                    return True
        else:
            
            success, output = run_command("node main.js --help", cwd=self.install_dir, logger=self.logger)
            if success:
                self.logger.log("Test completed successfully.")
                self.logger.log("Note: This test only verifies that the code can run, not that it can connect to Minecraft.")
                self.logger.log("You will need to start a Minecraft world and open it to LAN before running Mindcraft.")
                return True
        
        self.logger.log(f"Test failed: {output}", "ERROR")
        
        return True