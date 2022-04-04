from network import Sigfox
import socket
import ubinascii

# RCZ1 = EUROPE RCZ2 = USA RCZ3 = Japan RCZ4 = Australia
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
print(ubinascii.hexlify(sigfox.mac()))
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

s.setblocking(True)

s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

s.send('Hello !')
