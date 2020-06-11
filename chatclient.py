#!/usr/bin/python3
import socket
import sys
import threading
x=socket.socket()
#hostName=input(str('Enter the host name of this server:'))
port=8080
x.connect(('massimo-pc',port))
print('You are connected to the chat server!',x.getpeername(),'from',x.getsockname())

def receive():
   while 1:
      recv_msg=x.recv(1024)
      recv_msg=recv_msg.decode()
      print("\nOther Person: ", recv_msg)
      
recv_thread = threading.Thread(target=receive)
recv_thread.start()

while 1:
   send_msg= input(str("\nYou: "))
   send_msg=send_msg.encode()
   x.send(send_msg)
   print("Your message has been sent...")
