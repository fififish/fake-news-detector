#Author: Sisi Duan. Information Systems. University of Maryland, Baltimore County
#Used for demonstration of socket style message transmission
#Requirement: python 2.7
#Reference for struct: https://docs.python.org/2/library/struct.html

import socket
import sys
from io import BytesIO
import struct
import time

portnum = 5000
hostname = 'localhost'


def encode(m):
    (msgtype,content)=m
    buf = BytesIO()
    buf.write(struct.pack('<i',msgtype))
    if msgtype == 0: #string type, can directly write
        buf.write(content)
    else:
        buf.write(struct.pack('<i',content))
    buf.seek(0)
    return buf.read()

    

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = (hostname,portnum)
sock.connect(server_addr)

t1 = time.time()
msg = (1,100)
m = encode(msg)
print "Sending message: ", msg
sock.send(m)
reply = sock.recv(1024)
print reply
sock.close()
t2 = time.time()
print t2-t1

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = (hostname,portnum)
sock.connect(server_addr)
msg = (0,"Hello There")
m = encode(msg)
print "Sending message: ", msg
sock.send(m)
reply = sock.recv(1024)
print reply
sock.close()
t3 = time.time()
print t3-t2

print "done."

