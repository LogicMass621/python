#!/usr/bin/python3
import socket
import sys
import threading

x = socket.socket()
x.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
hostName = socket.gethostname()
print("The server will start on host:", hostName)
port=8080
x.bind((hostName, port))
print('The server is done binding to host and port.')
x.listen(1)
connection,address = x.accept()
print(address, 'has connected to the server.')

def receive():
   while 1:
      recv_msg=connection.recv(1024)
      recv_msg=recv_msg.decode()
      print("Client:", recv_msg)
   
recv_thread = threading.Thread(target=receive)
recv_thread.start()

while 1:
   send_msg= input(str("Type here: "))
   send_msg=send_msg.encode()
   connection.send(send_msg)

