@echo off
set timestamp=%date:~4,2%%date:~7,2%%time:~0,2%%time:~3,2%.%time:~6,2%
@REM set timestamp=%date:~4,2%%date:~7,2%%time:~0,2%%time:~3,2%%time:~6,2%.%time:~9,2%
echo %timestamp%
adb shell date "%timestamp%"

@REM $timestamp = Get-Date -Format "MMddHHmm.ss.ffff"
@REM echo $timestamp
@REM adb shell date $timestamp
@REM adb shell date
