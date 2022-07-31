from network import LoRa
import socket
import time
import ubinascii
from lib.TMP275 import TMP275
from lib.FDC2112 import FDC2112
import pycom
import struct

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

app_eui = ubinascii.unhexlify('FF55AA2211E56000')
app_key = ubinascii.unhexlify('F37B8FA84633B20F78A37A9383B1FC42')
dev_eui = ubinascii.unhexlify('70B3D5499AA34571')

temp_sensor = TMP275()
soil_sensor = FDC2112()

lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)
while not lora.has_joined():
    time.sleep(2.5)
    print("Not yet joined...")
print("Joined")
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

while 1:
    temperature = "{t:.1f}".format(t=temp_sensor.temp())
    frequency = "{freq:.1e}".format(freq=soil_sensor.readFrequencySensor(0))
    capacitance = "{cap:.1e}".format(cap=soil_sensor.getCSensor())

    print("Temperature read:\n%sC" %temperature)
    print("Frequency read:\n%sHz" %frequency)
    print("Capacitance measured:\n%sF" %capacitance)

    if temp_sensor.temperature > 30:
        pycom.rgbled(0xFF0000)  # Red
    else:
        if temp_sensor.temperature > 20:
            pycom.rgbled(0x00FF00)  # Green
        else:
            pycom.rgbled(0x0000FF)  # Blue

    msg = bytearray(temperature,"ascii")
    print(msg)

    s.setblocking(True)

    s.send(msg)

    s.setblocking(False)

    time.sleep(5)
