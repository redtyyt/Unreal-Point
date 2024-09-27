import subprocess

def run_compile_exe():
    """
    Use it for compiling and to create the .exe file
    """
    process = subprocess.Popen('pyinstaller --onefile -w "Unreal-Point/app.py" -n "Unreal-Point" -i "Unreal-Point/Unreal Pojnt ico.ico"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Error! {stderr}")
    return stdout.decode().strip(), print("Compiling Finished!")

run_compile_exe()