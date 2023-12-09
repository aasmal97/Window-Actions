import os
import subprocess
import shutil
from install import install_requirements
from exclusion import files_to_ignore

def create_dist_directory(curr_dir: str):
    new_dist_path = os.path.normpath(os.path.abspath(os.path.join(curr_dir,r'..\Sources\com.arkyasmal.windowactions.sdPlugin\dist')))
    old_dist_path = os.path.normpath(os.path.abspath(os.path.join(curr_dir,r'..\Sources\com.arkyasmal.windowactions.sdPlugin\app\windowsScripts\dist')))
    setup_dir = os.path.normpath(os.path.abspath(os.path.join(curr_dir,r'..\Sources\com.arkyasmal.windowactions.sdPlugin\app\windowsScripts')))
    # Build the setup.py using py
    subprocess.run(['py', 'setup.py', 'build', '--build-exe', 'dist'], cwd=setup_dir)
    # Remove the dist directory
    try:
        shutil.rmtree(new_dist_path)
    except FileNotFoundError:
        pass
    # Move the dist directory to the parent directory
    shutil.move(old_dist_path, new_dist_path)

def create_release_file(
    appPath: str,
    releasePath: str,
    buildPluginPath: str,
    releasePluginPath: str,
    sourcePluginPath: str
):
    try:
        shutil.rmtree(buildPluginPath)
    except FileNotFoundError:
        pass
    try:
        shutil.rmtree(appPath)
    except FileNotFoundError:
        pass
    # Copy files using shutil.copytree
    shutil.copytree(sourcePluginPath, buildPluginPath, ignore=files_to_ignore)

    # Copy files to appPath
    shutil.copytree(buildPluginPath, appPath)
    try:
        # Delete previous release files
        os.remove(releasePluginPath)
    except FileNotFoundError:
        pass
    # Run DistributionTool
    dist_path = os.path.join(releasePath,"DistributionTool.exe")
    command = [dist_path,"-b", "-i", buildPluginPath, "-o", releasePath]
    subprocess.run(command, shell=False, cwd=releasePath)

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Set variables
    pluginName = "com.arkyasmal.windowactions"
    extension = "sdPlugin"
    appPath = os.path.join(os.environ["APPDATA"], "Elgato", "StreamDeck", "Plugins", f"{pluginName}.{extension}")
    buildPath =  os.path.normpath(os.path.abspath(os.path.join(current_dir, r"..\Build")))
    releasePath =  os.path.normpath(os.path.abspath(os.path.join(current_dir, r"..\Release")))
    buildPluginPath = os.path.join(buildPath, f"{pluginName}.{extension}")
    sourcePluginPath = os.path.normpath(os.path.abspath(os.path.join(current_dir, r"..\Sources", f"{pluginName}.{extension}")))
    releasePluginPath = os.path.join(releasePath, f"{pluginName}.streamDeckPlugin")
    install_requirements()
    create_dist_directory(current_dir)
    create_release_file( appPath, releasePath, buildPluginPath, releasePluginPath, sourcePluginPath)