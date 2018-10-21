#Author: Sisi Duan. Information Systems. University of Maryland, Baltimore County
#Used for demonstration of socket style message transmission
#Requirement: python 2.7
#Reference for struct: https://docs.python.org/2/library/struct.html

import socket
import sys
from io import BytesIO
import struct
import threading

port = 5000
hostname = 'localhost'

def is_even(n):
    return n % 2 == 0

def decode(m):
    buf = BytesIO(m)
    (msgtype,) = struct.unpack('<i', buf.read(4)) #read the type (int format)
    if msgtype == 0:
        content = buf.read() #Read the rest of the content
    else:
        (content,) = struct.unpack('<i', buf.read(4))
    return msgtype,content 


def handle_client_connection(sock):
    buf = sock.recv(1024)
    (msgtype,content) = decode(buf)
    if msgtype == 0:
        print ("We have received a message: "+content)
        sock.send("Thank you")
    else:
        print ("We have received a number: "+str(content)+", returning whether it is an even or odd message")
        if is_even(int(content)):
            reply = "even"
        else:
            reply = "odd"
        sock.send(reply)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((hostname, port))
sock.listen(2)
print ("Ready. Listening to socket...")

while True:
    client_sock, address = sock.accept()
    print ('Accepted connection from {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)  
    )
    client_handler.start()

sock.close()
