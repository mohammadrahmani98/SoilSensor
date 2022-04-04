from network import Sigfox
import socket

# RCZ1 = EUROPE RCZ2 = USA RCZ3 = Japan RCZ4 = Australia
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)

s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

s.setblocking(True)

s.setsockopt(socket.SOL_SIGFOX, socket.S0_RX, False)

s.send('Hello !')
