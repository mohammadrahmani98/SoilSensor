from lib.TMP275 import TMP275
import pycom
import time
import TMP275

pycom.heartbeat(False)

temp_sensor = TMP275()

while True:
    pycom.rgbled(0xFF0000)  # Red
    time.sleep(1)
    print("Temperature read:")
    print(temp_sensor.temp())
    pycom.rgbled(0x00FF00)  # Green
    time.sleep(1)
    pycom.rgbled(0x0000FF)  # Blue
    time.sleep(1)