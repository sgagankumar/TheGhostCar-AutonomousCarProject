import socket
import time
HOST = "192.168.43.2"
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()
print('Connected by', addr)
while True:
    data = bytes('123',"utf-8")
    conn.sendall(data)
    time.sleep(0.5)
s.close()