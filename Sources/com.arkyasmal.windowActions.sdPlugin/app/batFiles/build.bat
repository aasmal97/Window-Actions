cd %~dp0
set pluginName=com.arkyasmal.windowactions
set extension=sdPlugin
call npm run install
cd %~dp0
call npm run copy
cd %~dp0
cd ..
cd ..
cd ..
cd ..
cd  "Build/%pluginName%.%extension%"
@REM call npx nexe app/index.js -i app/index.js -t x64-14.15.3 -o run.exe
cd %~dp0
cd ..
cd ..
cd .. 
cd ..
::copy everything but compiled app directiory
Xcopy ".\\Sources\\%pluginName%.%extension%" ".\\Build\\%pluginName%.%extension%" /E /I /Y /EXCLUDE:.\Sources\com.arkyasmal.windowActions.sdPlugin\exclusions.txt
:: For testing on streamdeck
set appPath=%appdata%\\Elgato\\StreamDeck\\Plugins\\%pluginName%.%extension%
call Xcopy /E /I /Y ".\\Build\\%pluginName%.%extension%" "%appPath%"
:: For distribution
set buildPath="%cd%\Build\%pluginName%.%extension%"
set releasePath="%cd%\Release"
cd "./Release"
::remove any previous files
del %releasePath%\%pluginName%.streamDeckPlugin
call DistributionTool.exe -b -i %buildPath% -o %releasePath%

