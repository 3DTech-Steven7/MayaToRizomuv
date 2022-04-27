@echo off
chcp 65001
@echo off
cd /d "%~dp0"
cacls.exe "%SystemDrive%\System Volume Information" >nul 2>nul
if %errorlevel%==0 goto Admin
if exist "%temp%\getadmin.vbs" del /f /q "%temp%\getadmin.vbs"
echo Set RequestUAC = CreateObject^("Shell.Application"^)>"%temp%\getadmin.vbs"
echo RequestUAC.ShellExecute "%~s0","","","runas",1 >>"%temp%\getadmin.vbs"
echo WScript.Quit >>"%temp%\getadmin.vbs"
"%temp%\getadmin.vbs" /f
if exist "%temp%\getadmin.vbs" del /f /q "%temp%\getadmin.vbs"
exit
:Admin

powershell -Command "[Environment]::GetFolderPath('MyDocuments') | Out-File 'docspath.tmp' -Encoding ascii"
set /p DOCSPATH=< docspath.tmp
del docspath.tmp

if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
set loacl_mod_folder=%cd%\modules
set loacl_mod=%loacl_mod_folder%\MayaToRizomUV.mod
set modules_folder=%DOCSPATH%\maya\modules
set user_mod=%modules_folder%\MayaToRizomUV.mod

if not exist %loacl_mod_folder% ( md %loacl_mod_folder%)
if not exist %modules_folder% ( md %modules_folder%)

echo + MayaToRizomUV 2.2.0 %cd% > %loacl_mod%
copy /Y %loacl_mod% %user_mod%

msg %username% /time:10 "Installs Successful!"