import os
import subprocess
import sys
import time
import urllib.request
from tkinter import messagebox, Tk
import game

def check_wifi_available():
    """
    Überprüft, ob eine WLAN-Verbindung besteht.

    Returns:
        bool: True, wenn WLAN verfügbar ist, False sonst.
    """
    try:
        # Versuche, eine Verbindung zu einem bekannten Host herzustellen (Google)
        urllib.request.urlopen("https://www.google.com", timeout=5)
        print("yes wifi")
        return True
    except:
        print("no wifi")
        return False

def get_latest_version(github_pages_url):
    """
    Ruft die neueste Version vom GitHub Pages Server ab.

    Args:
        github_pages_url (str): Die URL zum GitHub Pages Ordner,
            der die Datei 'version.txt' enthält.

    Returns:
        str: Die neueste Versionsnummer oder None bei Fehler.
    """
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
    """
    Lädt das Update-Paket (latest.zip) von GitHub Pages herunter.

    Args:
        github_pages_url (str): Die URL zum GitHub Pages Ordner,
            der die Datei 'latest.zip' enthält.
        temp_dir (str): Der Pfad zu einem temporären Verzeichnis,
            zum Speichern des Downloads.

    Returns:
        str: Der Pfad zur heruntergeladenen ZIP-Datei oder None bei Fehler.
    """
    update_file_url = f"{github_pages_url}/latest.zip"
    local_zip_path = os.path.join(temp_dir, "latest.zip")
    try:
        print(f"Herunterladen von Update von: {update_file_url}")
        with urllib.request.urlopen(update_file_url) as response, open(
            local_zip_path, "wb"
        ) as out_file:
            data = response.read()  # Lies die gesamte Antwort in den Speicher
            out_file.write(data)  # Schreibe die Daten in die Datei
        print(f"Update heruntergeladen nach: {local_zip_path}")
        return local_zip_path
    except Exception as e:
        print(f"Fehler beim Herunterladen des Updates: {e}")
        return None


def extract_update(zip_file_path, install_dir):
    """
    Extrahiert das Update-Paket in das Installationsverzeichnis der Anwendung.

    Args:
        zip_file_path (str): Der Pfad zur heruntergeladenen ZIP-Datei.
        install_dir (str): Der Pfad zum Installationsverzeichnis der Anwendung.
    """
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
    """
    Löscht temporäre Dateien und Verzeichnisse.

    Args:
        temp_dir (str): Der Pfad zum temporären Verzeichnis.
    """
    import shutil

    try:
        shutil.rmtree(temp_dir)
        print(f"Temporäre Dateien in {temp_dir} gelöscht.")
    except Exception as e:
        print(f"Fehler beim Löschen temporärer Dateien: {e}")



def restart_application(app_name):
    """
    Startet die Anwendung neu.

    Args:
        app_name (str): Der Name der ausführbaren Datei der Anwendung.
    """
    try:
        game.main_loop()
    except Exception as e:
        print(f"Fehler beim Neustart der Anwendung: {e}")
        # Zeige eine Meldung an, wenn der Neustart fehlschlägt
        messagebox.showerror(
            "Neustart Fehler",
            "Anwendung konnte nicht neu gestartet werden. Bitte starten Sie sie manuell.",
        )



def main():
    """
    Hauptfunktion deines Spiels, inklusive Update-Prüfung.
    """
    # Konfiguration
    print("main func gestartet")
    github_pages_url = "https://acz12.github.io/ab_updates/"  # Ändern!
    
    with open("version.txt","r") as f:
        
        current_version = f.read() # Aktuelle Version deiner Anwendung
        
        
    app_name = "game.py"  # Name deiner ausführbaren Datei oder Startskripts # Ändern!

    # Tkinter root für die Messagebox erstellen, aber nicht anzeigen
    root = Tk()
    root.withdraw()

    # Update-Prüfung durchführen
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

                    temp_dir = tempfile.mkdtemp()  # Erstelle ein temporäres Verzeichnis
                    print(f"Temporäres Verzeichnis erstellt: {temp_dir}")
                    zip_file_path = download_update(github_pages_url, temp_dir)
                    if zip_file_path:
                        install_dir = os.path.dirname(
                            os.path.abspath(sys.argv[0])
                        )  # Installationsverzeichnis
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
            "Kein WLAN",
            "Keine WLAN-Verbindung verfügbar. Die Anwendung wird ohne Update-Prüfung gestartet.",
        )
        game.main_loop()

    
if __name__ == "__main__":
    main()
