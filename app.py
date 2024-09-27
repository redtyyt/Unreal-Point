import subprocess
import os
from tkinter import messagebox
import tkinter as tk
import tkinter.filedialog as fd
import time

# Funzione per eseguire comandi shell
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        messagebox.showerror("Error", f"Error: {stderr.decode()}")
    return stdout.decode().strip()

# Verifica se Azure CLI è installato
def check_azure_cli():
    stdout = run_command("az --version")
    if "az" in stdout:
        return True
    return False

# Installazione di Azure CLI (per Windows)
def install_az_cli():
    try:
        messagebox.showinfo("Installation", "I'm installing Azure CLI on your computer. This may take a while")
        run_command("curl -L https://aka.ms/InstallAzureCliWindows -o azure-cli.msi")
        run_command("msiexec /i azure-cli.msi /quiet")
        messagebox.showinfo("Installation", "Azure CLI successfully installed on your computer.")
    except Exception as e:
        messagebox.showerror("Error", f"ERROR! {e}")

def update_task():
    import upd

# Funzione per verificare se Azure DevOps è configurato e aprire la finestra di setup se necessario
def start_setup():
    global pat_entry, org_url_entry, setup  # Definisci le variabili globali

    time.sleep(3)

    update_task()

    # Controlla se Azure DevOps è già configurato
    try:
        with open('saved/important/bool.cli.azure_configured.txt', 'r') as f:
            azure_config_status = f.readline().strip()
            print(f"Azure DevOps configuration status: {azure_config_status}")  # Messaggio di debug
            
            if azure_config_status == "True":
                return  # Non aprire la finestra di configurazione se è già configurato
    except FileNotFoundError:
        pass

    # Se non è configurato, crea e mostra la finestra di configurazione
    if not check_azure_cli():
        install_cli_button.pack(pady=10)
        messagebox.showwarning("Warning", "Azure CLI is not installed. Click the button below to install it.")
    else:
        # Mostra la finestra di configurazione
        setup = tk.Toplevel(root)
        setup.title("Azure DevOps Configuration")
        setup.geometry("400x250")

        tk.Label(setup, text="Personal Access Token (PAT)").pack(pady=5)
        pat_entry = tk.Entry(setup, width=50)
        pat_entry.pack(pady=5)

        tk.Label(setup, text="Organization URL").pack(pady=5)
        org_url_entry = tk.Entry(setup, width=50)
        org_url_entry.pack(pady=5)

        config_button = tk.Button(setup, text="Config Azure DevOps", command=config_azure_devops)
        config_button.pack(pady=10)

        install_cli_button = tk.Button(setup, text="Install Azure CLI", command=install_az_cli)
        setup.mainloop()  # Inizia il loop della finestra di configurazione

# Funzione per configurare Azure DevOps
def config_azure_devops():
    global pat_entry, org_url_entry, setup  # Accesso alle variabili globali

    pat = pat_entry.get()
    org_url = org_url_entry.get()

    if not pat or not org_url:
        messagebox.showerror("Error", "Insert all details!")
        return
    
    # Salva i dati nei file di configurazione
    if not os.path.exists('config'):
        os.makedirs('config')

    with open('config/pat.txt', 'w') as f:
        f.write(pat)
    with open('config/org_url.txt', 'w') as f:
        f.write(org_url)

    messagebox.showinfo("Config", "Azure setup finished successfully.")
    setup.quit()  # Chiude la finestra di configurazione


# Funzione per assicurarsi di essere sul branch principale
def ensure_main_branch():
    output = run_command("git branch --show-current")
    if output != 'main' and output != 'master':
        run_command("git checkout main")  # Cambia 'main' con 'master' se il branch principale è chiamato 'master'
        run_command("git pull")

# Funzioni per la GUI (per clonare il repository)
def clone_repo():
    repo_url = repo_entry.get()
    local_path = path_entry.get()
    
    if not os.path.exists(local_path):
        output = run_command(f"git clone {repo_url} {local_path}")
        messagebox.showinfo("Result", output)
    else:
        os.chdir(local_path)
        output = run_command("git pull")
        messagebox.showinfo("Pull", output)

# Funzione per il commit e push
def commit_and_push():
    local_path = path_entry.get()
    message = commit_message.get()
    
    os.chdir(local_path)
    
    # Assicurati di essere sul branch principale
    ensure_main_branch()
    
    run_command("git add .")
    output = run_command(f'git commit -m "{message}"')
    messagebox.showinfo("Commit", output)
    output = run_command("git push")
    messagebox.showinfo("Push", output)

# Carica dati salvati
def load_data(useRes:bool):
    try:
        with open('saved/repo.txt', 'r') as file:
            repo_entry.delete(0, tk.END)
            repo_entry.insert(0, file.read().strip())
        with open('saved/localpath.txt', 'r') as file:
            path_entry.delete(0, tk.END)
            path_entry.insert(0, file.read().strip())
    except FileNotFoundError:
        if useRes:
            messagebox.showinfo("Info", "No saved data found.")
        else:
            pass

def check_isalreadyconfigured_azure():
    stdout = run_command("az account show")

    if "Please run 'az login'" in stdout:
        return False
    
    stdout = run_command("az devops configure --list")
    if "organization" in stdout:
        return True
    return False

def toggle_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = True  # Cambia lo stato della variabile
    root.attributes("-fullscreen", is_fullscreen)

def exit_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = False
    root.attributes("-fullscreen", False)

def get_commits():
    local_path = path_entry.get()
    local_path_use = path_entry
    if not verify_is_empty(local_path_use):
        if not is_git_repo(local_path):
            messagebox.showerror("Error", "The specified path is not a valid Git repository.")
            return None
        else:
            os.chdir(local_path)
    try:
        output = run_command('git log -n 5 --pretty=format:"%h - %an, %ar : %s"')
        print(f"Git log output: {output}")  # Debug: stampa l'output per verificare se il comando funziona
        return output
    except Exception as e:
        print(f"Error: {e}")
        return None

def is_git_repo(path):
    """Verify if the path is a Git repo"""
    if not os.path.exists(path=path):
        return False
    original_dir = os.getcwd()
    os.chdir(path=path)
    result = run_command("git rev-parse --is-inside-work-tree")
    os.chdir(original_dir)
    return True

def browse_path():
    selected_path = fd.askdirectory()
    if selected_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, selected_path)

def create_comm_viewer():
    global commit_text

    commit_frame = tk.Frame(root)
    commit_frame.pack(expand=False)

    scrollbar = tk.Scrollbar(commit_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    commit_text = tk.Text(commit_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, font="TkDefaultFont 12", spacing3=10)
    commit_text.pack(fill=tk.BOTH, expand=True)

    scrollbar.config(command=commit_text.yview)

    return commit_text

def display_commits():
    recent_commits = get_commits()

    commit_text.config(state=tk.NORMAL)
    if recent_commits:
        commit_text.delete(1.0, tk.END)
        for commit in recent_commits.splitlines():
            commit_text.insert(tk.END, commit + "\n")
    else:
        commit_text.insert(tk.END, "No commits found!")

    commit_text.config(state=tk.DISABLED)

def verify_is_empty(content: tk.Entry):
    if content.get() == "":
        return True
    elif not content.get():
        return True
    elif content.getint(s=7) >= 7:
        print("Content!")
        return False

# Configurazione della finestra principale
root = tk.Tk()
root.title("Unreal Point 0.0.3")
root.geometry("1300x800")

is_fullscreen = False
root.attributes("-fullscreen", False)

# Associa il tasto F per alternare la modalità full screen
root.bind("<F>", toggle_fullscreen)

# Associa il tasto Esc per uscire dal full screen
root.bind("<Escape>", exit_fullscreen)

tk.Label(root, text="Unreal Point 0.0.3", font="TkDefaultFont 44").pack(pady=5)

def save_data_persistent():
    repo_url = repo_entry.get()
    local_path = path_entry.get()

    with open('saved/repo.txt', 'w') as file:
        file.write(repo_url)
    with open('saved/localpath.txt', 'w') as file:
        file.write(local_path)

# Etichetta e campo per il repository URL
tk.Label(root, text="Repository URL (Optional)").pack(pady=5)
repo_entry = tk.Entry(root, width=60)
repo_entry.pack(pady=5)

path_entry = tk.Entry(root, width=60)
path_entry.pack(pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_path)
browse_button.pack(pady=5)

save_data_b = tk.Button(root, text="Save data", command=save_data_persistent)
save_data_b.pack(pady=5)

# Pulsante per clonare il repository
clone_button = tk.Button(root, text="Clone/Pull", command=clone_repo)
clone_button.pack(pady=10)

# Campo per il messaggio di commit
tk.Label(root, text="Commit message").pack(pady=5)
commit_message = tk.Entry(root, width=60)
commit_message.pack(pady=5)

# Pulsante per il commit e push
commit_button = tk.Button(root, text="Commit and Push", command=commit_and_push)
commit_button.pack(pady=10)

# Pulsante per caricare dati salvati
load_button = tk.Button(root, text="Load saved data", command=lambda: load_data(useRes=True))
load_button.pack(pady=10)
load_data(useRes=False)

tk.Label(root, text="-----------------------------").pack(pady=10)

tk.Label(root, text="Recent commits", font="TkDefaultFont 44").pack(pady=5)

tk.Button(root, text="Search commits", command=display_commits).pack(pady=10)

commit_text = create_comm_viewer()

display_commits()

tk.Label(root, text="-----------------------------").pack(pady=10)

# Info 1 Label
if is_fullscreen:
    tk.Label(root, text="Click Esc to exit fullscreen").pack(pady=5)

# Verifica e crea la cartella "saved" se non esiste
if not os.path.exists('saved'):
    os.makedirs('saved')
if not os.path.exists('saved/important'):
    os.makedirs('saved/important')
if not os.path.exists('saved/important/bool.cli.already_installed'):
    with open('saved/important/bool.cli.already_installed.txt', 'w') as file:
        if not check_azure_cli():
            file.write("False")
        else:
            file.write("True")
if not os.path.exists('saved/important/bool.cli.azure_configured.txt'):
    with open('saved/important/bool.cli.azure_configured.txt', 'w') as file:
        if not check_azure_cli():
            file.write("False")
        else:
            file.write("True")
if not os.path.exists("saved/important/version.txt"):
        with open("saved/important/version.txt", "w") as f:
            f.write("0.0.3")

# Verifica l'installazione di Azure CLI e avvia la configurazione
start_setup()

# Avvio della GUI principale
root.mainloop()
