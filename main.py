import os
import subprocess
import sys
import time
import urllib.request
from tkinter import messagebox, Tk
import game

def check_wifi_available():
    try:
        urllib.request.urlopen("https://www.google.com", timeout=5)
        return True
    except:
        print("no wifi")
        return False

def get_latest_version(github_pages_url):
    version_file_url = f"{github_pages_url}/version.txt"
    print(version_file_url)
    try:
        with urllib.request.urlopen(version_file_url) as response:
            latest_version = response.read().decode().strip()
        return latest_version
    except Exception as e:
        print(f"Fehler beim Abrufen der neuesten Version: {e}")
        return None

def download_update(github_pages_url, temp_dir):

    update_file_url = f"{github_pages_url}/latest.zip"
    local_zip_path = os.path.join(temp_dir, "latest.zip")
    try:
        print(f"Herunterladen von Update von: {update_file_url}")
        with urllib.request.urlopen(update_file_url) as response, open(
            local_zip_path, "wb"
        ) as out_file:
            data = response.read()  
            out_file.write(data) 
        print(f"Update heruntergeladen nach: {local_zip_path}")
        return local_zip_path
    except Exception as e:
        print(f"Fehler beim Herunterladen des Updates: {e}")
        return None


def extract_update(zip_file_path, install_dir):
    import zipfile

    try:
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(install_dir)
        print(f"Update extrahiert nach: {install_dir}")
    except Exception as e:
        print(f"Fehler beim Entpacken des Updates: {e}")
        return False
    return True

def cleanup_temp_files(temp_dir):
    import shutil

    try:
        shutil.rmtree(temp_dir)
        print(f"Temporäre Dateien in {temp_dir} gelöscht.")
    except Exception as e:
        print(f"Fehler beim Löschen temporärer Dateien: {e}")



def restart_application(app_name):
    try:
        if sys.platform.startswith("win"):
            subprocess.Popen([sys.executable, app_name])  # Verwende sys.executable
        else:
            subprocess.Popen(["python3", app_name]) #TODO: check if this works for other OS
        sys.exit()
    except Exception as e:
        print(f"Fehler beim Neustart der Anwendung: {e}")
        # Zeige eine Meldung an, wenn der Neustart fehlschlägt
        messagebox.showerror(
            "Neustart Fehler",
            "Anwendung konnte nicht neu gestartet werden. Bitte starten Sie sie manuell.",
        )



def main():
    print("main func gestartet")
    github_pages_url = "https://acz12.github.io/ab_updates/"
    
    with open("version.txt","r") as f:
        
        current_version = f.read()
        
        
    app_name = "game.py"  
    root = Tk()
    root.withdraw()

    if check_wifi_available():
        print("WLAN ist verfügbar.")
        latest_version = get_latest_version(github_pages_url)
        if latest_version:
            print(f"Neueste Version auf GitHub Pages: {latest_version}")
            if latest_version > current_version:
                print("Eine neue Version ist verfügbar.")
                update_available = messagebox.askyesno(
                    "Update verfügbar",
                    f"Version {latest_version} ist verfügbar. Möchten Sie aktualisieren?",
                )
                if update_available:
                    import tempfile

                    temp_dir = tempfile.mkdtemp()  
                    print(f"Temporäres Verzeichnis erstellt: {temp_dir}")
                    zip_file_path = download_update(github_pages_url, temp_dir)
                    if zip_file_path:
                        install_dir = os.path.dirname(
                            os.path.abspath(sys.argv[0])
                        )  
                        if extract_update(zip_file_path, install_dir):
                            cleanup_temp_files(temp_dir)
                            messagebox.showinfo(
                                "Update erfolgreich",
                                "Die Anwendung wird aktualisiert und neu gestartet.",
                            )
                            restart_application(app_name)
                        else:
                            cleanup_temp_files(temp_dir)
                            messagebox.showerror(
                                "Update Fehler",
                                "Fehler beim Extrahieren des Updates.",
                            )
                    else:
                         cleanup_temp_files(temp_dir)
                else:
                    print("Benutzer hat das Update abgelehnt.")
                    game.main_loop()
            else:
                print("Die Anwendung ist auf dem neuesten Stand.")
                game.main_loop()
        else:
            print("Fehler beim Überprüfen auf Updates.")
            game.main_loop()
    else:
        print("Keine WLAN-Verbindung verfügbar. Update-Prüfung übersprungen.")
        messagebox.showinfo(
            "Nincs WLAN",
            "Nincs WLAN-Verbindung verfügbar. Die Anwendung wird ohne Update-Prüfung gestartet.",
        )
        game.main_loop()

    
if __name__ == "__main__":
    main()
