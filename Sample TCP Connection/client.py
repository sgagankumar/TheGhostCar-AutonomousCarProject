import socket
import time

HOST = "192.168.43.2"
PORT = 5555

time.sleep(0)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
	data = s.recv(1024)
	print('Received', repr(data))
	time.sleep(.5)

s.close()