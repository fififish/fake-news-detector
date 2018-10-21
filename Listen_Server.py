import parsingconfig
from jpype import *
import sys
import socket
import socks
from gevent import Greenlet
from gevent.server import StreamServer
from gevent.queue import *


def listen_to_channel(hostname,port,id):
    newport = int(port)+int(id)
    print('Preparing thread to listen on %d...' % newport)
    q = Queue()
    def _handle(socket, address):
        f = socket.makefile()
        while True:
            print "---message received"
    server = StreamServer(('localhost', newport), _handle)
    server.start()
    return q
    
if __name__ == '__main__':
    
    if len(sys.argv[1:])<1:
        print "Use: python BFTServer.py <ReplicaID>"
        exit()

    replicaID = sys.argv[1]
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print 'socket created'
    port = 5000
    newport = int(port)+int(replicaID)
    sock.bind(("localhost", newport))
    
    sock.listen(10)
    while 1:
        conn,addr = sock.accept()
        print "connected..."
   