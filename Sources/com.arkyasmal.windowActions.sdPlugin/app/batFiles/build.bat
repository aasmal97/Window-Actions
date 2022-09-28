cd %~dp0
set pluginName=com.arkyasmal.windowactions.sdPlugin
call npm run install
cd %~dp0
call npm run copy
cd %~dp0
cd ..
cd ..
cd ..
cd ..
cd  Build/%pluginName%
call nexe app/index.js -i app/index.js -t x64-14.15.3 -o run.exe
cd %~dp0
cd ..
cd ..
cd .. 
cd ..
::copy everything but compiled app directiory
Xcopy ".\\Sources\\%pluginName%" ".\\Build\\%pluginName%" /E /I /Y /EXCLUDE:.\Sources\com.arkyasmal.windowActions.sdPlugin\exclusions.txt
:: For testing on streamdeck
set appPath=%appdata%\\Elgato\\StreamDeck\\Plugins\\%pluginName%
call Xcopy /E /I /Y ".\\Build\\%pluginName%" "%appPath%"
:: For distribution
set buildPath="%cd%\Build\%pluginName%"
set releasePath="%cd%\Release"
cd "./Release"
call DistributionTool.exe -b -i %buildPath% -o %releasePath%

