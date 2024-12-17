@echo off

setlocal EnableDelayedExpansion

set "action=%~1"
set "arguments="

for %%i in (%*) do (
    if not "%%i"=="%~1" (
        set "arguments=!arguments! %%i"
    )
)

if /I "%action%"=="-info" (
    echo This is the documentation for the k_launcher.
    echo.
    echo Usage:
    echo    rez env k_launcher -- wrapper args*
    echo.
    echo arg:
    echo    config : name of the config you working on.
    echo.
    echo args*:
    echo    -package : package you are working on.
    echo    -launch : launch the dcc with his default packages.
    echo    -add : add packages.
    echo    -save : save the context.
    echo    -load : load the context.
    echo    -info : listing of the options
    echo.
    echo launch command:
    echo    rez env k_launcher -- run config ...
    echo    rez env k_launcher -- run config value -pa package -add packages -save
    echo    rez env k_launcher -- run config value -load value
    echo    rez env k_launcher -- run config value -launch value
    echo.
    echo config structur:
    echo    config : package : context/path/file.rxt
) else (
    if not "%arguments%"=="" (
        echo.
        echo Performing launch with additional arguments: %arguments%
        echo.
        py C:/pipeline/PROD/k_launcher/1.0.0/k_launcher/k_launcher_wrapper.py %arguments%
    )
)



