import parsingconfig
from jpype import *
import socket
from io import BytesIO
import struct
#from threshenc.tdh2 import encrypt,decrypt, serialize, serialize1, deserialize, deserialize0, deserialize1, TDHPublicKey, TDHPrivateKey, group
import cPickle as pickle
import threading
import time
from Crypto.Hash import SHA256
import base64
from Enc import initiateThresholdEnc,serializeEnc,deserializeEnc,prepareEnc,deserializeShare,verify_cshare,combine_share


class ReplyTracker(object):
    def __init__(self,Response,ResponseCt,ResponseSeq,Done,ciphertext,result):
        self.Response = Response
        self.ResponseCt = ResponseCt
        self.ResponseSeq = ResponseSeq
        self.Done = Done
        self.ciphertext = ciphertext
        self.result = result
    
    def increaseCt(self,i):
        try:
            self.ResponseCt[i]+=1
        except:
            self.ResponseCt[i]=1
            self.Done[i] = 0

    def complete(self,i):
        try:
            return self.Done[i]
        except:
            self.Done[i] = 0
            return self.Done[i]

    def appendNew(self,i,content):
        try:
            self.Response[i].append(content)
        except:
            self.Response[i] = []
            self.Response[i].append(content)
    
    def putcipherText(self,i,ciphertext):
        self.ciphertext[i] = ciphertext

    def storeResult(self,result):
        self.result = result
    
    def getResult(self,i):
        try:
            return i,result[i]
        except:
            return ""

def connect_to_channel(hostname,port,id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    newport = int(port)+int(id)
    sock.bind((hostname, newport))
    sock.listen(1)
    return sock

def listen_to_channel(sock):
    while 1:
        conn,addr = sock.accept()
        buf = conn.recv(8092)
        #print "**Received a reply"
        if buf == "You cannot view any data in the system":
            print buf
        elif buf == "You don't have access to view any data in the system":
            print buf
        else:
            replicaID,result = deepDecode(buf)

            for i,encrypted,j,k in result:
                
                if replyTracker.complete(i):
                    pass
                else:
                    if encrypted == 1:
                        
                        share = deserializeShare(j)
                        if not verify_cshare(replicaID,share,k):
                            break
                        replyTracker.increaseCt(i)
                        replyTracker.appendNew(i,(int(replicaID),share))
                        replyTracker.putcipherText(i,k)
                        if replyTracker.ResponseCt[i] > f:
                            #print replyTracker.Done[i]
                            if replyTracker.Done[i]!=0:
                                break
                            #print "ok we are ready to combine the shares", i
                            try:
                                m = combine_share(replyTracker.ciphertext[i],replyTracker.Response[i])
                                print "----[READ ENCRYPTED RESPONSE] Seq: %s, Message: %s"%(i,m)
                                replyTracker.Done[i] = 1
                            except:
                                "something is wrong..."
                            
                    else:
                        print "----[READ PLAIN RESPONSE] Seq: %s, Message: %s"%(i,j)
                        replyTracker.Done[i] = 1
                    

def deepDecode(m):
    buf = BytesIO(m)
    replicaID,num =  struct.unpack('<ii', buf.read(8))
    result = []
    for i in range(num):
        seq,encrypted = struct.unpack('<ii', buf.read(8))
        if encrypted == 1:
            slength,clength = struct.unpack('<ii', buf.read(8))
            content = buf.read(slength)
            ciphertext = buf.read(clength)
            result.append((seq,encrypted,content,ciphertext))
        else:
            length, = struct.unpack('<i', buf.read(4))
            content = buf.read(length)
            result.append((seq,encrypted,content,"NULL"))
    return replicaID,result


if __name__ == '__main__':

    if len(sys.argv[1:])<4:
        print "Use for write request: python BFTClient.py <process id> 1 <number of operations> <encrypt>"
        print "Use for read request: python BFTClient.py <process id> 0 <ReadRequestID> <ReadRequestID>"
        exit()

    processID = sys.argv[1]
    increment = sys.argv[2]
    nops = requestID = sys.argv[3]
    encrypted = sys.argv[4]

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-l", "--label", dest="label",
                      help="Access control list, divided by comma", metavar="L", type="string")
    (options, args) = parser.parse_args()

    label = processID #By default, label contains the node itself since everyone should be able to read his own messages

    if(options.label):
        label = options.label

    replyTracker = ReplyTracker({},{},{},{},{},{})
    global f
    Response = {}
    ResponseCt = {}
    (n,f,host,baseport) = parsingconfig.readconfig()
    #print (n,f,host,baseport)

    thresencs = "./config/thenc4_1.keys" 
    #TODO: For fixed file names and n and f. Need to be enhanced to be included from input and consistent with bft-smart configs.
    initiateThresholdEnc(open(thresencs, 'r').read())

    
    prepareEnc(label)
    
    sock = connect_to_channel("localhost",15000,processID)
    
    classpath = "lib/commons-codec-1.5.jar:lib/core-0.1.4.jar:lib/netty-all-4.1.9.Final.jar:lib/slf4j-api-1.5.8.jar:lib/slf4j-jdk14-1.5.8.jar:bft-smart/bin/BFT-SMaRt.jar"
    startJVM(getDefaultJVMPath(),"-Djava.class.path=%s"%classpath)

    # you can then access to the basic java functions
    # java.lang.System.out.println("hello world")

    KVClientClass = JPackage("bftsmart.demo.keyvalue")
    #KVClientClass.KVClient.test()
    KVClientClass.KVClient.passArg((processID,increment,nops))

    time1 = time.time()
    
    if increment=="0":
        KVClientClass.KVClient.sendRequest(0,requestID,"0","")
        listen_to_channel(sock)
        
    else:
        for i in range(int(nops)):
            if encrypted == "1":
                request = prepareEnc(label)
            else: 
                request = "Dummy Test Request"
            KVClientClass.KVClient.sendRequest(int(increment),request,encrypted,label)
    time2 = time.time()
    print "done with %s requests in %lfs."%(nops,time2-time1)

    # and you have to shutdown the VM at the end
    shutdownJVM()
