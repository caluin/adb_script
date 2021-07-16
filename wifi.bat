adb wait-for-device && adb root && adb remount
adb shell "echo manual_lock > /sys/power/wake_lock"
adb shell wifitest.sh start-softap --ssid 'softap' --psk 'FbRules123'
adb tcpip 5555
set /p input="set wifi to softap"
adb connect 192.168.43.1:5555
adb -e logcat -s mcuservice