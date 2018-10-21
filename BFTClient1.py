# coding:utf-8
# import parsingconfig
from jpype import *
# from ..threshenc.tdh2 import encrypt,decrypt
from socket import *
import Server
import socket
from io import BytesIO

if __name__ == '__main__':

    # Server.serverpart()

    if len(sys.argv[1:]) < 3:
        print
        "Use: python BFTClient.py <process id> <increment> <number of operations>"
        exit()

    processID = sys.argv[1]
    increment = sys.argv[2]
    nops = sys.argv[3]
    num = nops.split(';')
    print(processID, increment, len(num), type(nops))
    # print(num[0],num[1])
    # (n,f,host,baseport) = parsingconfig.readconfig()
    # print (n,f,host,baseport)

    classpath = "lib/commons-codec-1.5.jar:lib/core-0.1.4.jar:lib/netty-all-4.1.9.Final.jar:lib/slf4j-api-1.5.8.jar:lib/slf4j-jdk14-1.5.8.jar:bft-smart/bin/BFT-SMaRt.jar"
    startJVM(getDefaultJVMPath(), "-Djava.class.path=%s" % classpath)

    # you can then access to the basic java functions
    # java.lang.System.out.println("hello world")

    KVClientClass = JPackage("bftsmart.demo.keyvalue")
    KVClientClass.KVClient.test()
    KVClientClass.KVClient.passArg((processID, increment, str(len(num))))

    for i in range(len(num)):
        KVClientClass.KVClient.sendRequest(num[i].decode('utf-8').strip())  # +'//:'+processID

        # accept from servers, need to record server
    shutdownJVM()




