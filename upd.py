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
        exit(1)
        return
    if local_version is None:
        messagebox.showerror("Error", "Error during the update check")
        exit(1)
        return
    
    if remote_version == local_version:
        pass
    elif local_version is None:
        messagebox.showerror("Update", "What? The version file doesn't exists, pls reinstall")
    else:
        messagebox.showinfo("Update", f"New version downloading : {remote_version}. Current version : {local_version}")
        try:
            response = requests.get(DOWNLOAD_URL_BASE + remote_version + "/Unreal-Point.exe", stream=True)
            with open("Unreal-Point.exe", "wb") as f:
                shutil.copyfileobj(response.raw, f)
                delete_ancient_file(file=LOCAL_EXE_FILE)
                print("Old version removed!")
                change_local_version()
                messagebox.showwarning("Update", "Please reopen the application downloaded.")
                exit(code=0)
                return print("Finished Update!")
        except Exception as e:
            messagebox.showerror("Error", f"Error during the update: {e}. I didn't think that this can happen... Please report this as an issue on github.")
            exit(1)
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Error during the update: {e}")
            exit(1)

def delete_ancient_file(file):
    """
    Delete the old executable of the application
    """

    if os.path.exists(file):
        os.remove(file)
    else:
        print(f"The file {file} does not exist")

def change_local_version():
    """
    Cambia la versione nel file locale, ma non facilmente, ma scaricando il file "version.txt" dal repo, sovrascrivendo quello non originale
    """

    remote_version = get_remote_version()

    with open(LOCAL_VERSION_FILE, "w") as f:
        f.write(remote_version)


if os.path.exists(LOCAL_VERSION_FILE):
    print("The path exists")
else:
    messagebox.showerror("Error", "Local file doesn't exist, reinstall the app.")
    exit(1)


def check_updates():
    root = tk.Tk()
    root.withdraw()
    update()

check_updates()