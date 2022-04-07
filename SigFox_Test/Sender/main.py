from network import LoRa
import socket
import machine
import time
import ubinascii

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
i = 0
while True:
   s.setblocking(True)
   ender = ' '
   val = str(i) + ender;
   s.send(val)

   s.setblocking(False)

   print("Sended! ",i," Times")

   i += 1

   time.sleep(machine.rng() & 0x0F)
