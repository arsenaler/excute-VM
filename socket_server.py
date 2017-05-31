#!/usr/bin/python
import socket
import commands
import threading
host = "10.8.43.155"
port = 8081

def join(client, address):
    try:
        client.settimeout(300)
        buf = client.recv(2048)
        client.send(buf)
    except socket.timeout:
        print "time out"
    client.close

t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
t.bind((host, port))
t.listen(60)


while 1:
    client, address = t.accpt()
    print "connected by ", address
    thread = threading.Thread(target=join, args=(client, address))
    thread.start()


