cd %~dp0
set pluginName=com.arkyasmal.windowActions.sdPlugin
call npm run install
cd %~dp0
call npm run copy
cd %~dp0
cd ..
cd ..
cd ..
cd ..
call nexe Build/%pluginName%/app/index.js --i app/index.js -t x64-14.15.3 -o Build/%pluginName%/run.exe
cd %~dp0
cd ..
cd ..
cd .. 
cd ..
::Xcopy .\\Sources\\%pluginName%\\app\\manifest.json .\\Build\\%pluginName%\\manifest.json
::copy everything but compiled app directiory
Xcopy ".\\Sources\\%pluginName%" ".\\Build\\%pluginName%" /E /I /Y /EXCLUDE:.\Sources\com.arkyasmal.windowActions.sdPlugin\exclusions.txt
:: For testing on streamdeck
set appPath=%appdata%\\Elgato\\StreamDeck\\Plugins\\%pluginName%
::call Xcopy /E /I /Y ".\\Build\\%pluginName%" "%appPath%"