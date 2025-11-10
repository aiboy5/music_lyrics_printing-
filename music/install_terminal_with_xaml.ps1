# Use TLS 1.2 for security
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# First, download and install the UI XAML framework
$xamlUrl = "https://www.nuget.org/api/v2/package/Microsoft.UI.Xaml/2.8.5"
Write-Host "Downloading UI XAML Framework..."

try {
    # Download XAML Framework
    Invoke-WebRequest -Uri $xamlUrl -OutFile "Microsoft.UI.Xaml.2.8.zip" -UseBasicParsing
    Expand-Archive -Path "Microsoft.UI.Xaml.2.8.zip" -DestinationPath ".\xaml" -Force
    
    # Install the framework
    Get-ChildItem -Path ".\xaml\tools\AppX\x64\Release\*.appx" | ForEach-Object {
        Write-Host "Installing framework from: $($_.FullName)"
        Add-AppxPackage -Path $_.FullName
    }
    
    # Clean up XAML files
    Remove-Item -Path "Microsoft.UI.Xaml.2.8.zip" -Force
    Remove-Item -Path ".\xaml" -Recurse -Force

    # Now download Windows Terminal
    $url = "https://api.github.com/repos/microsoft/terminal/releases/latest"
    Write-Host "Getting latest Windows Terminal release info..."
    
    $release = Invoke-RestMethod -Uri $url
    $asset = $release.assets | Where-Object { $_.name -like "*.msixbundle" } | Select-Object -First 1
    
    if ($asset) {
        Write-Host "Downloading Windows Terminal from: $($asset.browser_download_url)"
        Invoke-WebRequest -Uri $asset.browser_download_url -OutFile "WindowsTerminal.msixbundle" -UseBasicParsing
        
        if (Test-Path "WindowsTerminal.msixbundle") {
            Write-Host "Download complete! Installing..."
            Add-AppxPackage -Path "WindowsTerminal.msixbundle"
            Remove-Item "WindowsTerminal.msixbundle"
            Write-Host "Installation complete!"
        }
    }
} catch {
    Write-Host "Error: $_"
    Write-Host "Manual installation steps:"
    Write-Host "1. Install Microsoft.UI.Xaml.2.8 framework from Microsoft Store"
    Write-Host "2. Download Windows Terminal from: https://github.com/microsoft/terminal/releases/latest"
    Write-Host "3. Find the .msixbundle file and download it"
    Write-Host "4. Double-click to install"
}

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")