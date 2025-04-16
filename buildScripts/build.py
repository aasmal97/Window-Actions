import os
import subprocess
import shutil

plugin_name = "com.arkyasmal.windowactions.sdPlugin"
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
    # install python packages
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'], cwd=root_path)

def create_dist_directory(curr_dir: str):
    new_dist_path = os.path.normpath(os.path.abspath(os.path.join(
        curr_dir, fr'${pluginName}\dist')))
    old_dist_path = os.path.normpath(os.path.abspath(os.path.join(
        curr_dir, fr'{pluginName}\app\scripts\dist')))
    setup_dir = os.path.normpath(os.path.abspath(os.path.join(
        curr_dir, fr'{pluginName}\app\scripts')))
    # Build the setup.py using py
    subprocess.run(['py', 'setup.py', 'build'], cwd=setup_dir)
    # Remove the dist directory
    try:
        shutil.rmtree(new_dist_path)
    except FileNotFoundError:
        pass
    # Move the dist directory to the parent directory
    shutil.move(old_dist_path, new_dist_path)


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Set variables
    pluginName = "com.arkyasmal.windowactions"
    extension = "sdPlugin"
    appPath = os.path.join(
        os.environ["APPDATA"], "Elgato", "StreamDeck", "Plugins", f"{pluginName}.{extension}")
    buildPath = os.path.normpath(os.path.abspath(
        os.path.join(current_dir, r"..\Build")))
    releasePath = os.path.normpath(os.path.abspath(
        os.path.join(current_dir, r"..\Release")))
    buildPluginPath = os.path.join(buildPath, f"{pluginName}.{extension}")
    sourcePluginPath = os.path.normpath(os.path.abspath(
        os.path.join(current_dir, r"..\Sources", f"{pluginName}.{extension}")))
    releasePluginPath = os.path.join(
        releasePath, f"{pluginName}.streamDeckPlugin")
    install_requirements()
    create_dist_directory(current_dir)
    # create_release_file(appPath, releasePath, buildPluginPath,
    #                     releasePluginPath, sourcePluginPath)


# def create_release_file(
#     appPath: str,
#     releasePath: str,
#     buildPluginPath: str,
#     releasePluginPath: str,
#     sourcePluginPath: str
# ):
#     try:
#         shutil.rmtree(buildPluginPath)
#     except FileNotFoundError:
#         pass
#     try:
#         shutil.rmtree(appPath)
#     except FileNotFoundError:
#         pass
#     # Copy files using shutil.copytree
#     shutil.copytree(sourcePluginPath, buildPluginPath, ignore=files_to_ignore)

#     # Copy files to appPath
#     shutil.copytree(buildPluginPath, appPath)
#     try:
#         # Delete previous release files
#         os.remove(releasePluginPath)
#     except FileNotFoundError:
#         pass
#     # Run DistributionTool
#     dist_path = os.path.join(releasePath, "DistributionTool.exe")
#     command = [dist_path, "-b", "-i", buildPluginPath, "-o", releasePath]
#     subprocess.run(command, shell=False, cwd=releasePath)
