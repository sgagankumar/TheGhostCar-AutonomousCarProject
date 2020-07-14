import socket
import time
print('TCP Server')
HOST = "192.168.43.2"
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()
print('Connected by', addr)
while True:
	f=open('angle.txt','r')
	data = f.read()
	print(data)
	conn.sendall(bytes(data,"utf-8"))
	time.sleep(0.1)
s.close()