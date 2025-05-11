
import os
import sys
import argparse
import time
from installer_utils import Logger, get_default_install_dir
from installer_dependencies import DependencyInstaller
from installer_setup import ProjectSetup

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Mindcraft Installer")
    parser.add_argument("--install-dir", help="Specify a custom installation directory")
    return parser.parse_args()

def main():
    """Main function"""
    
    args = parse_arguments()
    
    
    logger = Logger()
    logger.log("Starting Mindcraft installation...")
    
    try:
        
        logger.log("\n=== Step 1: Checking and installing dependencies ===")
        dependency_installer = DependencyInstaller(logger)
        if not dependency_installer.ensure_dependencies():
            logger.log("Failed to install required dependencies. Installation aborted.", "ERROR")
            return 1
        
        
        logger.log("\n=== Step 2: Setting up the project ===")
        project_setup = ProjectSetup(logger)
        
        
        install_dir = args.install_dir if args.install_dir else get_default_install_dir()
        project_setup.set_install_directory(install_dir)
        
        
        if not project_setup.clone_repository():
            logger.log("Failed to clone the repository. Installation aborted.", "ERROR")
            return 1
        
        
        logger.log("\n=== Step 3: Installing Node.js dependencies ===")
        if not project_setup.install_node_dependencies():
            logger.log("Failed to install Node.js dependencies. Installation aborted.", "ERROR")
            return 1
        
        
        logger.log("\n=== Step 4: Installing Python dependencies ===")
        if not dependency_installer.install_python_dependencies(install_dir):
            logger.log("Failed to install Python dependencies. Installation will continue, but some features may not work.", "WARNING")
        
        
        logger.log("\n=== Step 5: Setting up keys.json ===")
        if not project_setup.setup_keys_json():
            logger.log("Failed to set up keys.json. Installation will continue, but you'll need to set it up manually.", "WARNING")
        
        
        logger.log("\n=== Step 6: Verifying installation ===")
        if not project_setup.verify_installation():
            logger.log("Installation verification failed. Some components may be missing.", "WARNING")
        
        
        logger.log("\n=== Step 7: Running npm install in the root directory ===")
        if not dependency_installer.run_npm_install(install_dir):
            logger.log("Failed to run npm install in the root directory. Installation will continue, but some features may not work.", "WARNING")
        
        
        logger.log("\n=== Step 8: Running a simple test ===")
        project_setup.run_test()
        
        
        project_setup.print_usage_instructions()
        
        logger.log("Installation completed successfully!")
        return 0
        
    except KeyboardInterrupt:
        logger.log("\nInstallation interrupted by user.", "WARNING")
        return 1
    except Exception as e:
        logger.log(f"\nAn unexpected error occurred: {e}", "ERROR")
        logger.log("Installation failed.", "ERROR")
        return 1

if __name__ == "__main__":
    sys.exit(main())