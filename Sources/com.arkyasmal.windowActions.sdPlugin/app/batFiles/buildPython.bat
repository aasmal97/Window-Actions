cd %~dp0
cd ../windowsScripts
pip install -r requirements.txt
@REM pyinstaller pluginActions.py -F -n pluginActions --distpath ../executables --workpath ../executables --specpath ../executables --add-data ../dll:.
pyinstaller connection.py -F -n run --distpath ../../ --workpath ../../ --specpath ../../ --add-data ./app/dll:.
@REM rmdir /s /q ..\executables\pluginActions
rmdir /s /q ..\..\run
@REM del ..\pluginActions.spec
del ..\..\run.spec
cd ..
cd ..