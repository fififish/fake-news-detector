#coding:utf-8
#import parsingconfig
from jpype import *
#from ..threshenc.tdh2 import encrypt,decrypt
from socket import *
import Server
import socket
from io import BytesIO

def connect_to_channel(hostname,port,id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #print 'socket created'
    newport = int(port)+int(id)*10
    #sock.bind(("localhost", newport))

    sock.bind((hostname, newport))  #James.  Replaced localhost with parameter passed in.
    
    sock.listen(1)
    return sock


if __name__ == '__main__':

    #Server.serverpart()

    if len(sys.argv[1:])<3:
        print "Use: python BFTClient.py <process id> <increment> <number of operations>"
        exit()

    processID = sys.argv[1]
    increment = sys.argv[2]
    nops = sys.argv[3]
    num = nops.split(';')
    print(processID,increment,len(num),type(nops))
    #print(num[0],num[1])
    #(n,f,host,baseport) = parsingconfig.readconfig()
    #print (n,f,host,baseport)

    classpath = "lib/commons-codec-1.5.jar:lib/core-0.1.4.jar:lib/netty-all-4.1.9.Final.jar:lib/slf4j-api-1.5.8.jar:lib/slf4j-jdk14-1.5.8.jar:bft-smart/bin/BFT-SMaRt.jar"
    startJVM(getDefaultJVMPath(),"-Djava.class.path=%s"%classpath)

    # you can then access to the basic java functions
    #java.lang.System.out.println("hello world")

    KVClientClass = JPackage("bftsmart.demo.keyvalue")
    KVClientClass.KVClient.test()
    KVClientClass.KVClient.passArg((processID,increment,str(len(num))))


    for i in range(len(num)):
        KVClientClass.KVClient.sendRequest(num[i].decode('utf-8').strip()) #+'//:'+processID

        #accept from servers, need to record server
         # receive and read from server
        
        for j in range(4):
            print(j)     
            
        #   设置IP和端口
            host = socket.gethostname()
            mySocket = connect_to_channel(host,3333,j)
            mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tag = True
            while tag:            
        #   接收客户端连接
                print("Waiting for connecting....")
                
                try:
                    client, address = mySocket.accept()
                except: 
                    client, address = mySocket.accept()
                print(client)
                msg = client.recv(1024)                
                print 'receive from server',j,':', msg.decode('utf-8')
                mySocket.close()
                tag = False
    shutdownJVM()


   

