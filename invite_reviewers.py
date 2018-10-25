#coding:utf-8
# receive msg results from reviewers
#import parsingconfig
from jpype import *
#from ..threshenc.tdh2 import encrypt,decrypt
import socket

def connect_to_channel(hostname,port,id,replicaID):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #print 'socket created'
    newport = int(port)+int(id)*10 + replicaID
    #sock.bind(("localhost", newport))

    sock.bind((hostname, newport))  #James.  Replaced localhost with parameter passed in.
    
    sock.listen(1)
    return sock

# message dealt with and return results from reviewers
def result (RN,replicaID):
    fn = (RN-1)/3
    msg_lst = []  #directly return back the result
    #msg_content = ''
    #msg_label = ''  
    for j in range(RN):
            #print(j)           
        #   设置IP和端口
        host = socket.gethostname()
        mySocket = connect_to_channel(host,4333,j,replicaID)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tag = True
        while tag:            
        #   接收客户端连接
            #print("Waiting for connecting....")
            try:
                client, address = mySocket.accept()
            except: 
                client, address = mySocket.accept()
                #print(client)
            review_result = client.recv(1024)  
            #print(msg)  
            #receive_msg = msg.split(';')
            msg_lst.append(review_result)
            #msg_content = receive_msg[0]
            #msg_label = receive_msg[1]
            #print 'receive from server',j,':', msg.decode('utf-8')
            mySocket.close()
            tag = False
    #if  msg_label == '1': news_label = 'final'
    #else: news_label = 'temporary'
    for x in msg_lst: 
        if msg_lst.count(x)>fn+1: 
            #print 'The ',news_label,'result for news verification of ', msg_content, 'is',x
            return x
            break
def msg_send(msg,replicaID):
    RN = 4 # total four reviewers for every server
    classpath = "lib/commons-codec-1.5.jar:lib/core-0.1.4.jar:lib/netty-all-4.1.9.Final.jar:lib/slf4j-api-1.5.8.jar:lib/slf4j-jdk14-1.5.8.jar:bft-smart/bin/BFT-SMaRt.jar"
    startJVM(getDefaultJVMPath(),"-Djava.class.path=%s"%classpath)

    # you can then access to the basic java functions
    #java.lang.System.out.println("hello world")

    KVClientClass = JPackage("bftsmart.demo.keyvalue")
    #KVClientClass.KVClient.test()
    KVClientClass.KVClient.passArg((replicaID,1,str(1))
    
    KVClientClass.KVClient.sendRequest(msg.decode('utf-8').strip()) #+'//:'+processID

    print(result(RN,replicaID))
if __name__ == '__main__':
        
    msg_send('I am a good student',0)    
    shutdownJVM()


   

