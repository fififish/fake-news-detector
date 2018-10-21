#coding:utf-8
#import parsingconfig
from jpype import *
import sys
import socket
from io import BytesIO
import struct
import threading
import vector
import logistic_regression
import SVM

#Since we deliver message from java module to python module, 
#I think it is ok to just use this socket function to directly
#deliver and process the message
#Need to figure out whether it is true. 
def listen_to_channel(sock):
    message = ''
    while 1:
        conn,addr = sock.accept()
        #print 'let us do it'
        print "got a message..."
        try:
            buf = conn.recv(1024)
            print(addr)
            #print buf
            tmp = BytesIO(buf)
            sequence,cid,length = struct.unpack('>iii', tmp.read(12))
            msg = tmp.read(length)
            #msg = msg.split('//:')
            print(msg)
            # send back
            #client.clientpart(msg, result)
            #resultset.append(msg+'\n'+result)
            #print "We have assigned sequence number ", sequence, " for client ", cid, " and request ", msg
            #if msg=="Dummy Test Request":
             #   print "good."
              #  print "We have assigned sequence number ",sequence," for client ",cid, " and request ",msg
        except:
            print "may have got a not well-formatted message"
            #TODO: Need to figure out why sometimes there are empty or not well-formatted messages
            pass
        #return result

def decode(m):

    buf = BytesIO(m)

    data = buf.read()
    print(data)
    length = struct.unpack('i', data[0:4])[0]
    print length
    fmt = str(length) + 's'
    print fmt
    message = struct.unpack(fmt, data[4:])[0]
    print "We received your message \"" + str(message) + "\""

    return message


def handle_client_connection(sock):
    #client, addre = sock.accept()
    #print 'Server receives', buf.decode('utf-8')
    reply = 'hahaha'
    print(reply)
    sock.send(reply.encode('utf-8'))
    print(reply)


if __name__ == '__main__':

    if len(sys.argv[1:])<1:
        print "Use: python BFTServer.py <ReplicaID>"
        exit()

    message = []
    me_result = []
    replicaID = sys.argv[1]

    #TODO: Nedd to handle configuration file to avoid hard-coded host name and port number
    #(n,f,host,baseport) = parsingconfig.readconfig()

    classpath = "lib/commons-codec-1.5.jar:lib/core-0.1.4.jar:lib/netty-all-4.1.9.Final.jar:lib/slf4j-api-1.5.8.jar:lib/slf4j-jdk14-1.5.8.jar:bft-smart/bin/BFT-SMaRt.jar"
    startJVM(getDefaultJVMPath(),"-Djava.class.path=%s"%classpath)

    KVServerClass = JPackage("bftsmart.demo.keyvalue")
    KVServerClass.KVServer.passArgs((replicaID,"1"))
    
    #listen_to_channel(sock)
    #print(len(message),len(me_result))

    hostname = 'localhost'
    port = 5000 + int(replicaID)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((hostname, port))
    sock.listen(2)

    listen_to_channel(sock)
    # print "DEBUG Ready. Listening to socket..."

    client_sock, address = sock.accept()
        # print 'DEBUG Accepted connection from {}:{}'.format(address[0], address[1])
    handle_client_connection(client_sock)

    sock.close()



    #sock.send(result)
    #print("news verification result of replica", replicaID, "is", result)
   # print(resultset)
    #sock.send(resultset[0])

    # and you have to shutdown the VM at the end
    shutdownJVM()
