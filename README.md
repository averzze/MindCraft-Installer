# Mindcraft Installer

The Mindcraft Installer is a Python-based tool designed to simplify the installation process for the [Mindcraft](https://github.com/kolbytn/mindcraft) project. It automates the setup of dependencies, clones the Mindcraft repository, installs required packages, and configures the project for use. The installer supports Windows, macOS, and Linux operating systems.

## Features

- **Automated Dependency Installation**: Checks and installs Git, Node.js, and npm if they are not already present.
- **Repository Cloning**: Copies Mindcraft files from a local directory or clones the repository from GitHub.
- **Dependency Management**: Installs both Python and Node.js dependencies.
- **Configuration Setup**: Creates a `keys.json` file from an example template for API key configuration.
- **Installation Verification**: Ensures all necessary files and dependencies are correctly installed.
- **Cross-Platform Support**: Compatible with Windows, macOS, and Linux.
- **Executable Option**: Provides a precompiled executable for Windows users for easy installation.

## Prerequisites

- **Python 3.6+**: Required to run the installer scripts (not needed for the precompiled executable on Windows).
- **Internet Connection**: Needed for downloading dependencies and cloning the repository (if not using local files).
- **Administrative Privileges**: May be required for installing dependencies on some systems.

## Installation

### Option 1: Running the Python Script

1. **Clone or Download the Repository**:
   ```bash
   git clone https://github.com/averzze/mindcraft-installer.git
   cd mindcraft-installer
   ```

2. **Run the Installer**:
   ```bash
   python install_mindcraft.py
   ```
   To specify a custom installation directory:
   ```bash
   python install_mindcraft.py --install-dir /path/to/directory
   ```

3. **Follow the Prompts**:
   - The installer will check for Git, Node.js, and npm, installing them if necessary.
   - It will copy or clone the Mindcraft files to the installation directory.
   - Python and Node.js dependencies will be installed.
   - A `keys.json` file will be created, which you need to edit with your API keys.

### Option 2: Using the Precompiled Executable (Windows Only)

1. **Download the Executable**:
   - Visit the [Releases](https://github.com/averzze/mindcraft-installer/releases) section of the GitHub repository.
   - Download the latest `mindcraft_installer.exe` file.

2. **Run the Executable**:
   - Double-click `mindcraft_installer.exe` or run it from the command line:
     ```bash
     mindcraft_installer.exe
     ```

3. **Follow the Prompts**:
   - The executable will semi-automate the installation process.

## Post-Installation

1. **Edit `keys.json`**:
   - Navigate to the installation directory (default: `~/Desktop/mindcraft`).
   - Open `keys.json` and add your API keys for supported services (e.g., OpenAI, Gemini, Anthropic). Refer to the `README.md` in the Mindcraft repository for details.

2. **Start a Minecraft World**:
   - Launch Minecraft and open a world to LAN on port `55916`.

3. **Run Mindcraft**:
   From the installation directory:
   ```bash
   node main.js
   ```

## Project Structure

- `install_mindcraft.py`: Wrapper script to download and run the installer.
- `mindcraft_installer.py`: Main installer script that orchestrates the installation process.
- `installer_utils.py`: Utility functions and constants for the installer.
- `installer_dependencies.py`: Functions for checking and installing dependencies.
- `installer_setup.py`: Functions for setting up the Mindcraft project.
- `build_installer_exe.py`: Script to build a standalone executable for Windows using PyInstaller.

## Building the Executable (For Developers)

To create a standalone executable for Windows:

1. Ensure all required files (`mindcraft_installer.py`, `installer_utils.py`, `installer_dependencies.py`, `installer_setup.py`) are in the same directory.
2. Run:
   ```bash
   python build_installer_exe.py
   ```
3. The executable will be created in the `dist` folder and copied to the current directory.
4. Upload the generated `mindcraft_installer.exe` to the GitHub Releases section for distribution.

## Troubleshooting

- **Git/Node.js Installation Issues**:
  - Ensure you have administrative privileges.
  - Check the `mindcraft_installer.log` file in the installation directory for detailed error messages.
  - Manually install Git (https://git-scm.com) or Node.js (https://nodejs.org) if automatic installation fails.

- **Python Dependency Issues**:
  - Ensure `pip` is installed and up-to-date (`python -m pip install --upgrade pip`).
  - Verify that `requirements.txt` exists in the installation directory.

- **Node.js Dependency Issues**:
  - Run `npm install` manually in the installation directory to diagnose issues.

- **API Key Errors**:
  - Ensure `keys.json` is properly configured with valid API keys.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Mindcraft](https://github.com/kolbytn/mindcraft) by Kolby Nottingham.
- Built with [PyInstaller](https://www.pyinstaller.org) for executable creation.
