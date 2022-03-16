@echo off
set milliseconds=%time:~9,2%
echo %milliseconds%
set /A wait_milliseconds=(100-%milliseconds%)*10
echo %wait_milliseconds%

set /A new_second=%time:~6,2% + 1
set timestamp=%date:~4,2%%date:~7,2%%time:~0,2%%time:~3,2%%date:~10,4%.%time:~6,2%
@REM set timestamp=%date:~4,2%%date:~7,2%%time:~0,2%%time:~3,2%%date:~10,4%.%new_second%

@REM ping -n 1 -w %wait_milliseconds% 127.0.0.1 > null

echo "%timestamp%"
adb root
adb shell date "%timestamp%"
adb shell date
echo %timestamp%

@REM $timestamp = Get-Date -Format "MMddHHmm.ss.ffff"
@REM echo $timestamp
@REM adb shell date $timestamp
@REM adb shell date
