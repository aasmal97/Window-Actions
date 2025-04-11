import os
import subprocess


def find_package_json(directory):
    if (directory is None or directory == ''):
        return None
    parent = os.path.dirname(directory)
    files = os.listdir(directory)
    if 'package.json' in files:
        return os.path.join(directory)
    else:
        return find_package_json(parent)
def install_requirements():
     # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_path = find_package_json(current_dir)
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'], cwd=root_path)
if __name__ == '__main__':
   install_requirements()
