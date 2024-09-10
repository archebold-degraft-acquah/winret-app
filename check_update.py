import requests
import wx
import subprocess
import os


# Current version of the app
CURRENT_VERSION = "v1.0.0"
GITHUB_REPO = "archebold-degraft-acquah/winret-app" 
RELEASES_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases"  # GitHub API for latest release

# Function to check for an app update from GitHub
def check_for_update():
    try:
        # Fetch the latest release information from GitHub API
        response = requests.get(RELEASES_API_URL)
        response.raise_for_status()
        release_info = response.json()
        
        latest_version = release_info[-1].get('tag_name', CURRENT_VERSION)
        download_url = None

        # Search for the download link in the assets of the release
        for asset in release_info[-1].get('assets', []):
            if asset['name'].endswith('.exe'):  # The installer is a .exe file
                download_url = asset['browser_download_url']
                break

        if download_url and latest_version > CURRENT_VERSION:  # Compare versions
            # Ask the user if they want to install the update
            app = wx.App(False)
            dialog = wx.MessageDialog(None, 
                                      f"Winret ({latest_version}) is available. Would you like to update?",
                                      "Update Available", wx.YES_NO | wx.ICON_QUESTION)
            result = dialog.ShowModal()
            dialog.Destroy()

            if result == wx.ID_YES:
                # If the user chooses to update, download and install the update
                if download_and_install_update(download_url, latest_version):
                    wx.MessageBox("Update installed successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
                else:
                    wx.MessageBox("Failed to install the update. Please try again later.", "Error", wx.OK | wx.ICON_ERROR)
            else:
                wx.MessageBox("Update skipped. You can update later.", "Info", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("You already have the latest version.", "Up to Date", wx.OK | wx.ICON_INFORMATION)
    except requests.exceptions.RequestException as e:
        wx.MessageBox(f"Error checking for updates: {e}", "Error", wx.OK | wx.ICON_ERROR)

# Function to download and install the update
def download_and_install_update(download_url, latest_version):
    try:
        # Download the update installer
        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        installer_path = f"C:\\Program Files\\winret\\winret_{latest_version}.exe"
        with open(installer_path, 'wb') as installer_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    installer_file.write(chunk)

        # Run the installer
        subprocess.run([installer_path], check=True)

        return True  # Return True if the update was successful
    except (requests.exceptions.RequestException, subprocess.CalledProcessError) as e:
        wx.MessageBox(f"Error during update: {e}", "Error", wx.OK | wx.ICON_ERROR)
        return False
