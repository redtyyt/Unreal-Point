import requests
import os
import shutil
import zipfile
import tkinter as tk
from tkinter import messagebox

REPO_URL = "https://raw.githubusercontent.com/redtyyt/Unreal-Point/main/version.txt"
DOWNLOAD_URL_BASE = "https://github.com/redtyyt/Unreal-Point/releases/download/"
LOCAL_VERSION_FILE = "version.txt"

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
    remote_version = get_remote_version()
    local_version = get_local_version()

    if remote_version is None:
        messagebox.showerror("Error", "Error during the update")
        return
    
    if remote_version == local_version:
        pass
    else:
        messagebox.showinfo("Update", f"New version is here! {remote_version}")

        try:
            response = requests.get(DOWNLOAD_URL_BASE + remote_version + "/Unreal-Point.exe", stream=True)
            with open("Unreal-Point.exe", "wb") as f:
                shutil.copyfileobj(response.raw, f)
        except Exception as e:
            messagebox.showerror("Error", "Error during the update")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Error during the update: {e}")

def check_updates():
    root = tk.Tk()
    root.withdraw()
    update()

check_updates()