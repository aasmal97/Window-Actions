cd %~dp0
cd ..
cd ..
cd ./app/windowsScripts
py -m venv virtual
cd %~dp0
cd ..
cd ..
.\\app\\windowsScripts\\virtual\\Scripts\\activate
py .\\app\\batFiles\\install.py