import os
import subprocess
def install_requirements():
     # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    new_path = os.path.normpath(os.path.abspath(os.path.join(current_dir,r"..\Sources\com.arkyasmal.windowactions.sdPlugin\app\windowsScripts")))
    # Install cx_Freeze using pip
    subprocess.run(['pip', 'install', '--force', '--no-cache', '--pre', '--extra-index-url', 'https://marcelotduarte.github.io/packages/', 'cx_Freeze'], cwd=new_path)
    # Install requirements.txt using pip
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'], cwd=new_path)
if __name__ == '__main__':
   install_requirements()
