from lib.TMP275 import TMP275
from lib.FDC2112 import FDC2112
import pycom
import time

pycom.heartbeat(False)

temp_sensor = TMP275()
soil_sensor = FDC2112()

while True:
    time.sleep(1)
    print("Temperature read:\n{temp:.1f}°C".format(temp=temp_sensor.temp()))
    print("Frequency read:\n{freq:.1e}Hz".format(freq=soil_sensor.readFrequencySensor(0)))
    print("Capacitance measured:\n{cap:.1e}F".format(cap=soil_sensor.getCSensor()))
    if temp_sensor.temperature > 30:
        pycom.rgbled(0xFF0000)  # Red
    else:
        if temp_sensor.temperature > 20:
            pycom.rgbled(0x00FF00)  # Green
        else:
            pycom.rgbled(0x0000FF)  # Blue
    time.sleep(1)