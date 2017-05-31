import socket

host = '10.8.43.155'
port = 8081
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
while 1:
    cmd = raw_input("please input cmd:")
    s.sendall(cmd)
    data = s.recv(1024)
    print data
s.close()
