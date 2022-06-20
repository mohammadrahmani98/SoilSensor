from lib.TMP275 import TMP275
import pycom
import time

pycom.heartbeat(False)

temp_sensor = TMP275()

while True:
    time.sleep(1)
    print("Temperature read:")
    print("{:.1f}°C".format(temp_sensor.temp()))
    if temp_sensor.temperature > 30:
        pycom.rgbled(0xFF0000)  # Red
    else:
        if temp_sensor.temperature > 20:
            pycom.rgbled(0x00FF00)  # Green
        else:
            pycom.rgbled(0x0000FF)  # Blue
    time.sleep(1)