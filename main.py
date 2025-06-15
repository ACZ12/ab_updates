import os
import subprocess
import sys
import urllib.request
from tkinter import messagebox, Tk # Keep Tk for messagebox
import game
from utils import load_resource

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
        else: # pragma: no cover
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
        print("version.txt not found. Assuming version 0.0.0 for update check.")
    app_name = "main.py" # Should be main.py if restarting the current script
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
                            # messagebox.showinfo( # Commented out for silent restart
                            #     "Update Successful",
                            #     "The application will be updated and restarted.",
                            # )
                            restart_application(app_name)
                        else: # pragma: no cover
                            cleanup_temp_files(temp_dir)
                            messagebox.showerror(
                                "Update Error",
                                "Error extracting the update.",
                            )
                            # Fall through to run current version after error message
                            pass
                    else: # pragma: no cover
                         cleanup_temp_files(temp_dir)
                         messagebox.showerror("Update Error", "Error downloading the update.")
                         # Fall through to run current version
                         pass
                else:
                    print("User declined update. Starting current version.")
                    # Fall through to run current version
                    pass
            else: # Already latest version or no new version found
                print("Application is up to date or no new version found. Starting current version.")
                # Fall through to run current version
                pass
        else: # Could not get latest version from server
            print("Could not retrieve latest version information. Starting current version.")
            # Fall through to run current version
            pass
    else: # No Wi-Fi
        messagebox.showinfo(
            "No Wi-Fi", # "Nincs WLAN" is Hungarian for "No WLAN"
            "No Wi-Fi connection available. The application will be started without checking for updates.",
        )
        # Fall through to run current version
        pass

    # --- Unified Game Launch ---
    try:
        game.main_loop()
    except Exception as e:
        print("----------------------------------------------------")
        print("AN UNHANDLED ERROR OCCURRED IN THE GAME:")
        print("----------------------------------------------------")
        import traceback
        traceback.print_exc()
        print("----------------------------------------------------")
        # Try to show a Tkinter message box, but it might fail if Tk is already problematic
        try:
            root_err = Tk() # Create a new root for the error message if the old one is gone
            root_err.withdraw()
            messagebox.showerror("Critical Game Error", f"A critical error occurred and the game had to close:\n\n{e}\n\nPlease check the console for more details.")
            root_err.destroy()
        except Exception as tk_e:
            print(f"Could not display Tkinter error message: {tk_e}")
        sys.exit(1) # Exit with an error code
    finally:
        if 'root' in locals() and root.winfo_exists(): # Check if root was defined and still exists
            root.destroy() # Ensure Tkinter root is destroyed

if __name__ == "__main__":
    main()
