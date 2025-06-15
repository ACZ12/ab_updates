print("DEBUG: main.py script is being parsed by Python interpreter...")
import os
import subprocess
import sys
import urllib.request
from tkinter import messagebox, Tk # Keep Tk for messagebox
# import game # Deferred import
from utils import load_resource
import logging

# --- Setup Basic Logging ---
LOG_FILE = "updater_log.txt"
# Clear log file at the start of each run
if os.path.exists(LOG_FILE): os.remove(LOG_FILE)
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def check_wifi_available():
    try:
        urllib.request.urlopen("https://www.google.com", timeout=5)
        return True
    except:
        return False

def get_latest_version(github_pages_url):
    # Ensure the URL is constructed cleanly, avoiding double slashes
    version_file_url = f"{github_pages_url.rstrip('/')}/version.txt"
    logging.debug(f"Attempting to fetch latest version from: {version_file_url}")
    try:
        # Add a timeout, similar to check_wifi_available
        with urllib.request.urlopen(version_file_url, timeout=5) as response:
            # Explicitly decode as utf-8 and strip whitespace
            latest_version = response.read().decode('utf-8').strip()
        # Basic validation: check if the string contains only digits and dots (and is not empty)
        if latest_version and all(c.isdigit() or c == '.' for c in latest_version):
            logging.debug(f"Successfully fetched and validated latest version: '{latest_version}'")
        else:
            logging.debug(f"Fetched version string '{latest_version}' seems malformed or empty.")
            return None
        return latest_version
    except urllib.error.URLError as e: # More specific for network/URL issues
        logging.error(f"URLError in get_latest_version for {version_file_url}: {e}")
        return None
    except UnicodeDecodeError as e: # Handle issues decoding the response
        logging.error(f"UnicodeDecodeError in get_latest_version for {version_file_url}: {e}")
        return None
    except Exception as e: # Catch other potential exceptions
        logging.error(f"Generic Exception in get_latest_version for {version_file_url}: {e}")
        return None

def download_update(github_pages_url, temp_dir):

    # Ensure the URL is constructed cleanly, avoiding double slashes
    update_file_url = f"{github_pages_url.rstrip('/')}/latest.zip"
    local_zip_path = os.path.join(temp_dir, "latest.zip")
    logging.debug(f"Attempting to download update from: {update_file_url} to {local_zip_path}")
    try:
        with urllib.request.urlopen(update_file_url) as response, open(
            local_zip_path, "wb"
        ) as out_file:
            data = response.read()  
            out_file.write(data) 
        logging.info(f"Update successfully downloaded to {local_zip_path}")
        return local_zip_path
    except Exception as e:
        logging.error(f"Failed to download update from {update_file_url}: {e}")
        return None


def extract_update(zip_file_path, install_dir):
    import zipfile

    try:
        logging.debug(f"Attempting to extract {zip_file_path} to {install_dir}")
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(install_dir)
        logging.info(f"Successfully extracted {zip_file_path} to {install_dir}")
    except Exception as e:
        logging.error(f"Failed to extract update {zip_file_path}: {e}")
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
    logging.info("--- MAIN FUNCTION ENTERED (main.py) ---")

    github_pages_url = "https://ACZ12.github.io/ab_updates/"
    app_name = "main.py" # Should be main.py if restarting the current script
    current_version = "0.0" # Default if version.txt is missing
    try:
        logging.debug("Attempting to load local version.txt...")
        # Use load_resource to ensure correct path if main.py is run from different directories
        # or if it's part of a more complex project structure.
        with open(load_resource("version.txt"), "r") as f:
            current_version = f.read().strip()
        logging.debug(f"Local version loaded: {current_version}")
    except FileNotFoundError:
        logging.warning("version.txt not found. Assuming version 0.0.0 for update check.")
    except Exception as e:
        logging.error(f"Error loading local version.txt: {e}")
    
    logging.debug("--- Initial variable assignments in main() complete ---")
    root = None
    try:
        logging.debug("Initializing Tkinter for message boxes...")
        root = Tk()
        root.withdraw()
        logging.debug("Tkinter initialized and withdrawn.")
    except Exception as e:
        logging.critical(f"Failed to initialize Tkinter: {e}. GUI messages for updates may not show.")

    # Flag to indicate if the game should proceed to launch
    proceed_to_game_launch = True
    logging.debug("Checking Wi-Fi availability...")
    if check_wifi_available():
        logging.debug("Wi-Fi check returned True. Proceeding to get latest version.")
        latest_version_str = get_latest_version(github_pages_url)
        if latest_version_str:
            logging.debug(f"Fetched latest version string: {latest_version_str}. Current version string: {current_version}.")
            
            try:
                # Convert versions to tuples of integers for proper comparison
                current_v_tuple = tuple(map(int, current_version.split('.')))
                latest_v_tuple = tuple(map(int, latest_version_str.split('.')))

                if latest_v_tuple > current_v_tuple:
                    logging.info(f"Update available. Local: {current_version} {current_v_tuple}, Latest: {latest_version_str} {latest_v_tuple}. Preparing to ask user.")
                    update_available = messagebox.askyesno(
                        "Update Available",
                        f"Version {latest_version_str} is available. Would you like to update?",
                    )
                    if update_available:
                        logging.info("User chose to update.")
                        import tempfile

                        temp_dir = tempfile.mkdtemp()  
                        logging.debug(f"Downloading update to temp_dir: {temp_dir}")
                        zip_file_path = download_update(github_pages_url, temp_dir)
                        if zip_file_path:
                            logging.debug(f"Update downloaded to: {zip_file_path}")
                            install_dir = os.path.dirname(
                                os.path.abspath(sys.argv[0])
                            )  
                            logging.debug(f"Extracting update to install_dir: {install_dir}")
                            if extract_update(zip_file_path, install_dir):
                                logging.info("Update extracted successfully.")
                                cleanup_temp_files(temp_dir)
                                logging.info("Restarting application for update.")
                                proceed_to_game_launch = False # Don't launch game, we are restarting
                                restart_application(app_name)
                            else: # pragma: no cover
                                logging.error("Error extracting update.")
                                cleanup_temp_files(temp_dir) # Still cleanup
                                messagebox.showerror(
                                    "Update Error",
                                    "Error extracting the update.",
                                )
                        else: # pragma: no cover
                             # The logging.error is now inside download_update
                             logging.error("Error downloading update.")
                             cleanup_temp_files(temp_dir) # Still cleanup
                             messagebox.showerror("Update Error", "Error downloading the update.")
                    else: # pragma: no cover
                        logging.info("User declined update. Starting current version.")
                else: # Already latest version or no new version found
                    logging.info(f"Application is up to date or no new version found. Local: {current_version}, Latest: {latest_version_str}.")
            except ValueError: # pragma: no cover
                logging.error(f"Could not parse version strings for comparison ('{current_version}', '{latest_version_str}'). Skipping update.")
                # Proceed without update if versions are malformed
        else: # Could not get latest version from server
            logging.warning("Could not retrieve latest version information. Starting current version.") # pragma: no cover
    else: # No Wi-Fi
        logging.info("Wi-Fi check returned False.")
        # The messagebox is good for the user, let's add a print for the developer console.
        if root: # Only show messagebox if Tkinter was initialized
            messagebox.showinfo(
                "No Wi-Fi",
                "No Wi-Fi connection available. The application will be started without checking for updates.",
            )
        logging.info("No Wi-Fi connection available. Skipping update check and starting current version.")

    # --- Game Launch Section (only if no update/restart happened) ---
    if proceed_to_game_launch:
        logging.info("Proceeding to import game module and launch game.")
        try:
            import game # Import game module here, only if we are launching
            logging.info("--- GAME MODULE IMPORTED (main.py) ---")
            logging.info("--- PRE-GAME.MAIN_LOOP() LAUNCH (main.py) ---")
            game.main_loop()
        except Exception as e: # pragma: no cover
            logging.critical("----------------------------------------------------")
            logging.critical("AN UNHANDLED ERROR OCCURRED IN THE GAME:")
            logging.critical("----------------------------------------------------")
            import traceback
            # Log the traceback to the file
            logging.error("Traceback (most recent call last):\n%s", traceback.format_exc())
            logging.critical("----------------------------------------------------")
            
            # Try to show a Tkinter message box for game error
            if root: # Check if Tkinter was initialized earlier
                try:
                    # Create a new root for the error message if the old one is gone or problematic
                    # This is safer than reusing the 'root' from updater if game init failed badly.
                    err_tk_root = Tk()
                    err_tk_root.withdraw()
                    messagebox.showerror("Critical Game Error", f"A critical error occurred and the game had to close:\n\n{e}\n\nPlease check updater_log.txt for more details.")
                    err_tk_root.destroy()
                except Exception as tk_e:
                    logging.error(f"Could not display Tkinter error message for game error: {tk_e}")
            sys.exit(1) # Exit with an error code

    if root is not None and root.winfo_exists(): # Ensure Tkinter root is destroyed if it was created
        root.destroy()
    logging.debug("main() function finished.")

if __name__ == "__main__":
    logging.info("--- __main__ BLOCK ENTERED (main.py) ---")
    main()
    logging.info("--- __main__ BLOCK FINISHED (main.py) ---")
