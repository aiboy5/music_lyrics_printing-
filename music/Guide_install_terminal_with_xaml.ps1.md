# Windows Terminal with XAML Installation Guide

This guide will walk you through the process of installing and configuring Windows Terminal with XAML customization.

## Prerequisites

- Windows 10 or Windows 11
- PowerShell 5.1 or higher
- Administrative privileges

## Installation Steps

1. **Open PowerShell as Administrator**
   - Right-click on the Start button
   - Select "Windows PowerShell (Admin)" or "Terminal (Admin)"

2. **Set Execution Policy**
   The installation script needs to run with the appropriate execution policy. Use this command:
   ```powershell
   powershell -ExecutionPolicy Bypass -File install_terminal_with_xaml.ps1
   ```

3. **Verify Installation**
   - Open Windows Terminal
   - Check that the XAML customizations are applied
   - Verify that the settings are loaded from `windowsterminal-settings.json`

## Configuration

The Windows Terminal settings are stored in `windowsterminal-settings.json`. You can customize:
- Color schemes
- Font settings
- Background opacity
- Keyboard shortcuts
- Profile settings

## Running the Music Script

To run the included music script:
1. Ensure Python 3.x is installed
2. Double-click `run_music.bat` or
3. Run from PowerShell:
   ```powershell
   python music.py
   ```

## Troubleshooting

If you encounter any issues:
1. Check that you're running as Administrator
2. Verify PowerShell execution policy
3. Ensure all required components are installed
4. Check the Windows Terminal logs

## Additional Resources

- [Windows Terminal Documentation](https://docs.microsoft.com/en-us/windows/terminal/)
- [PowerShell Documentation](https://docs.microsoft.com/en-us/powershell/)
- [XAML Overview](https://docs.microsoft.com/en-us/windows/uwp/xaml-platform/xaml-overview)

## Support

If you need help, please:
1. Check the issues section in the repository
2. Create a new issue with detailed information about your problem
3. Include any error messages and your system configuration