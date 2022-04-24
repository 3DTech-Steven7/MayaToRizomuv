@echo off
chcp 65001
set loacl_mod_folder=%cd%\modules
set loacl_mod=%loacl_mod_folder%\MayaToRizomUV.mod
set modules_folder=%USERPROFILE%\Documents\maya\modules
set user_mod=%modules_folder%\MayaToRizomUV.mod

if not exist %loacl_mod_folder% ( md %loacl_mod_folder%)
if not exist %modules_folder% ( md %modules_folder%)

echo + MayaToRizomUV 2.0.1 %cd% > %loacl_mod%
copy /Y %loacl_mod% %user_mod%

msg %username% /time:10 "Installs Successful!"