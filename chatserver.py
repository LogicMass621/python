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
connections=[]
x.listen()
recv_threads = []

def receive(receiver):
   connected = True
   while (connected):

      recv_msg=receiver.recv(1024)
      print('receive',receiver.getpeername())

      if recv_msg==b'':
         connected = False
         print('removed sender',receiver.getpeername())
         connections.remove(receiver)
         receiver.close()

      if recv_msg != b'':
         for i in connections:
            if receiver != i:
                  sent=i.send(recv_msg)
                  print ('sent',sent,'bytes to',i.getpeername())

while 1:
   connection,address = x.accept()
   connections.append(connection)
   print(address, 'has connected to the server.')

   recv_threads.append(threading.Thread(target=receive, args=[connection]))
   recv_threads[-1].start()


