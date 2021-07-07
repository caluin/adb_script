adb wait-for-device && adb root && adb remount 
@REM adb shell mfg_tool mcu raw set dev
adb shell mfg_tool mcu raw set w ConfigHallInactiveOverride 1
adb shell mfg_tool mcu reset
adb shell mfg_tool mcu raw captouch force-streaming
adb shell mfg_tool mcu raw loglevel capt trace
adb logcat -c
adb logcat -s mcuservice