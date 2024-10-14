import os
import subprocess
from virtual import find_package_json
def install_requirements():
     # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_path = find_package_json(current_dir)
    # Install cx_Freeze using pip
    # subprocess.run(['pip', 'install', '--force', '--no-cache', '--pre', '--extra-index-url', 'https://marcelotduarte.github.io/packages/', 'cx_Freeze'], cwd=root_path)
    # Install requirements.txt using pip
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'], cwd=root_path)
if __name__ == '__main__':
   install_requirements()
