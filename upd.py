import requests
import os
import shutil
import zipfile
import tkinter as tk
from tkinter import messagebox

REPO_URL = "https://raw.githubusercontent.com/redtyyt/Unreal-Point/main/version.txt"
DOWNLOAD_URL_BASE = "https://github.com/redtyyt/Unreal-Point/releases/download/"
LOCAL_VERSION_FILE = "saved/important/version.txt"
LOCAL_EXE_FILE = "Unreal-Point.exe"

def get_remote_version():
    try:
        response = requests.get(REPO_URL)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error during the update: {e}")
        return None


def get_local_version():
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as f:
            return f.read().strip()
        return None

def update():
    """
    Update the application via GitHub repo.
    """

    remote_version = get_remote_version()
    local_version = get_local_version()

    if remote_version is None:
        messagebox.showerror("Error", "Error during the update check")
        return
    
    if remote_version == local_version:
        pass
    else:
        messagebox.showinfo("Update", f"New version downloading : {remote_version}. Current version : {local_version}")
        try:
            response = requests.get(DOWNLOAD_URL_BASE + remote_version + "/Unreal.Point.exe", stream=True)
            with open("Unreal-Point.exe", "wb") as f:
                shutil.copyfileobj(response.raw, f)
                delete_ancient_file(file=LOCAL_EXE_FILE)
                change_local_version()
                messagebox.showwarning("Update", "Please reopen the application downloaded.")
                exit(code=0)
        except Exception as e:
            messagebox.showerror("Error", "Error during the update")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Error during the update: {e}")

def delete_ancient_file(file):
    """
    Delete the old executable of the application
    """

    if os.path.exists(file):
        os.remove(file)

def change_local_version():
    """
    Cambia la versione nel file locale, ma non facilmente, ma scaricando il file "version.txt" dal repo, sovrascrivendo quello non originale
    """

    remote_version = get_remote_version()

    with open(LOCAL_VERSION_FILE, "w") as f:
        f.write(remote_version)


def check_updates():
    root = tk.Tk()
    root.withdraw()
    update()

check_updates()