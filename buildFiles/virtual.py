import os
import subprocess
def find_package_json(directory):
    if(directory is None or directory == ''):
        return None
    parent = os.path.dirname(directory)
    files =  os.listdir(directory)
    if 'package.json' in files:
        return os.path.join(directory)
    else:
        return find_package_json(parent)
def create_virtual(): 
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = find_package_json(curr_dir)
    subprocess.run(['py', '-m', 'venv', '.venv'], cwd=root_dir)
    bat_file_path = os.path.join(root_dir, '.venv', 'Scripts')
    subprocess.run(['activate.bat'], cwd=bat_file_path)
if __name__ == '__main__':
    create_virtual()