import os
import subprocess
import sys
import time
import urllib.request
from tkinter import messagebox, Tk
import game

def load_resource(path):
    """
    Helper to get resource paths, works for normal run & PyInstaller bundle.
    Also handles if the path is already absolute.
    """
    if os.path.isabs(path): # If path is already absolute, return it directly
        return path
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller bundles stuff here
        base_path = sys._MEIPASS
    else:
        # Normal execution path
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, path)

def check_wifi_available():
    try:
        urllib.request.urlopen("https://www.google.com", timeout=5)
        return True
    except:
        return False

def get_latest_version(github_pages_url):
    version_file_url = f"{github_pages_url}/version.txt"
    print(version_file_url)
    try:
        with urllib.request.urlopen(version_file_url) as response:
            latest_version = response.read().decode().strip()
        return latest_version
    except Exception as e:
        return None

def download_update(github_pages_url, temp_dir):

    update_file_url = f"{github_pages_url}/latest.zip"
    local_zip_path = os.path.join(temp_dir, "latest.zip")
    try:
        with urllib.request.urlopen(update_file_url) as response, open(
            local_zip_path, "wb"
        ) as out_file:
            data = response.read()  
            out_file.write(data) 
        return local_zip_path
    except Exception as e:
        return None


def extract_update(zip_file_path, install_dir):
    import zipfile

    try:
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(install_dir)
    except Exception as e:
        return False
    return True

def cleanup_temp_files(temp_dir):
    import shutil

    try:
        shutil.rmtree(temp_dir)
    except Exception as e:
        pass # Error cleaning temp files is not critical for app function


def restart_application(app_name):
    try:
        if sys.platform.startswith("win"):
            subprocess.Popen([sys.executable, app_name])  # Use sys.executable
        else:
            subprocess.Popen(["python3", app_name]) #TODO: check if this works for other OS
        sys.exit()
    except Exception as e:
        # Show a message if the restart fails
        messagebox.showerror(
            "Restart Error",
            "Application could not be restarted. Please start it manually.",
        )



def main():
    github_pages_url = "https://acz12.github.io/ab_updates/"
    
    current_version = "0.0.0" # Default if version.txt is missing
    try:
        # Use load_resource to ensure correct path if main.py is run from different directories
        # or if it's part of a more complex project structure.
        with open(load_resource("version.txt"), "r") as f:
            current_version = f.read().strip()
    except FileNotFoundError:
        print("version.txt not found. Assuming version 0.0.0")
    app_name = "game.py"  
    root = Tk()
    root.withdraw()

    if check_wifi_available():
        latest_version = get_latest_version(github_pages_url)
        if latest_version:
            if latest_version > current_version:
                update_available = messagebox.askyesno(
                    "Update Available",
                    f"Version {latest_version} is available. Would you like to update?",
                )
                if update_available:
                    import tempfile

                    temp_dir = tempfile.mkdtemp()  
                    zip_file_path = download_update(github_pages_url, temp_dir)
                    if zip_file_path:
                        install_dir = os.path.dirname(
                            os.path.abspath(sys.argv[0])
                        )  
                        if extract_update(zip_file_path, install_dir):
                            cleanup_temp_files(temp_dir)
                            messagebox.showinfo(
                                "Update Successful",
                                "The application will be updated and restarted.",
                            )
                            restart_application(app_name)
                        else:
                            cleanup_temp_files(temp_dir)
                            messagebox.showerror(
                                "Update Error",
                                "Error extracting the update.",
                            )
                    else:
                         cleanup_temp_files(temp_dir)
                else:
                    game.main_loop() # User chose not to update
            else:
                game.main_loop()
        else:
            game.main_loop()
    else:
        messagebox.showinfo(
            "No Wi-Fi", # "Nincs WLAN" is Hungarian for "No WLAN"
            "No Wi-Fi connection available. The application will be started without checking for updates.",
        )
        game.main_loop()

    
if __name__ == "__main__":
    main()
