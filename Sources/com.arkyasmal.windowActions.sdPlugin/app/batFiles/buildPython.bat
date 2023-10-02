cd %~dp0
cd ../windowsScripts
pip install -r requirements.txt
pyinstaller pluginActions.py -F -n pluginActions --distpath ../executables --workpath ../executables --specpath ../executables --add-data ../dll:.
cd ..
cd ..