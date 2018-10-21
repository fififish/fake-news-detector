#coding:utf-8
#import parsingconfig
from jpype import *
#from ..threshenc.tdh2 import encrypt,decrypt
import socket
import Server
import struct
from io import BytesIO

def connect_to_channel(hostname,port,id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #print 'socket created'
    server_addr = (hostname, port+id)
    sock.connect(server_addr)
    return sock

def encode(m):
    buf = BytesIO()
    fmt = 'i'+str(len(m))+'s'
    print(fmt)
    buf.write(struct.pack(fmt,len(m),str(m).encode('utf-8')))
    buf.seek(0)
    print(buf.read())
    return buf.read()


if __name__ == '__main__':

    #Server.serverpart()

    if len(sys.argv[1:])<3:
        print "Use: python BFTClient.py <process id> <increment> <number of operations>"
        exit()

    processID = sys.argv[1]
    increment = sys.argv[2]
    nops = sys.argv[3]
    #num = nops.split(';')
    print(processID,increment,nops)
    #print(num[0],num[1])
    #(n,f,host,baseport) = parsingconfig.readconfig()
    #print (n,f,host,baseport)
    classpath = "lib/commons-codec-1.5.jar:lib/core-0.1.4.jar:lib/netty-all-4.1.9.Final.jar:lib/slf4j-api-1.5.8.jar:lib/slf4j-jdk14-1.5.8.jar:bft-smart/bin/BFT-SMaRt.jar"
    startJVM(getDefaultJVMPath(),"-Djava.class.path=%s"%classpath)

    # you can then access to the basic java functions
    #java.lang.System.out.println("hello world")

    KVClientClass = JPackage("bftsmart.demo.keyvalue")
    KVClientClass.KVClient.test()
    KVClientClass.KVClient.passArg((processID,increment,str(len(nops)))) #str(len(num))

    #for i in range(len(num)):
    #m = encode(nops)
    m = nops.decode('utf-8').strip()
    KVClientClass.KVClient.sendRequest(m) #
    #receiving msg back
    for i in range(4):
            #sock = connect_to_channel("localhost", 5000, i)
        sock = connect_to_channel('localhost',5000,i)
        reply = sock.recv(1024)
        port = 5000 + i
        print "Receive message from {}/{}: {}".format('localshost',port,reply.decode('utf-8'))


    shutdownJVM()

   

