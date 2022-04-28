@echo off
chcp 65001
Setlocal enabledelayedexpansion

for /f %%a in ('REG QUERY "hklm\SOFTWARE\Autodesk\Maya"') do (
    for /f "tokens=1,2,* " %%i in ('REG QUERY %%a\Setup\InstallPath /v MAYA_INSTALL_LOCATION ^| find /i "MAYA_INSTALL_LOCATION"') do (
        if not "%%k" == "" ( 
            echo cmd /k ""%%kbin\mayapy.exe" -m pip install --user pymel"
        )       
    )
)
msg %username% /time:10 "Installs Successful!"