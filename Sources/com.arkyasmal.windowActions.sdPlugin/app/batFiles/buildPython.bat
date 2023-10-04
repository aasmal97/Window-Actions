cd %~dp0
cd ../windowsScripts
pip install -r requirements.txt
@REM pyinstaller pluginActions.py -F -n pluginActions --distpath ../executables --workpath ../executables --specpath ../executables --add-data ../dll:.
pyinstaller pluginActions.py -F -n pluginActions --distpath ../ --workpath ../ --specpath ../ --add-data ./dll:.
@REM rmdir /s /q ..\executables\pluginActions
del ..\pluginActions.spec
cd ..
cd ..