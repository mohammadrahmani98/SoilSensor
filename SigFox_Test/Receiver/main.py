from network import LoRa
import socket
import machine
import time

lora = LoRa(mode=Lora.LORA, region=LoRa.EU868)

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
i=0
while True:
   s.setblocking(True)
   s.send('Hello I m Board 2')
   s.setblocking(False)
   data = s.recv(64)
   print(data, " Recivied ",i , " times")
   i += 1
   time.sleep(machine.rng() & 0x0F)
