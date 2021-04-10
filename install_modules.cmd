@echo off
chcp 65001
set mod_name=MayaToRizomUV.mod
set loacl_mod=%cd%\modules
set user_mod=%USERPROFILE%\Documents\maya\modules
if exist %loacl_mod% == 0(
   md %loacl_mod%
)
echo + MayaToRizomUV 1.0.1 %cd% > %loacl_mod%\%mod_name%
if exist %user_mod% == 0(
   md %user_mod%
)
copy /Y %loacl_mod%\%mod_name% %user_mod%\%mod_name%

msg %username% /time:10 "Installs Successful!"