#coding:utf-8
#import parsingconfig
from jpype import *
#from ..threshenc.tdh2 import encrypt,decrypt
from socket import *
import socket
from io import BytesIO
#import leveldb
'''
def db_exist(db,key):
    try:
        db.Get(key)
        return True
    except KeyError:
        return False
'''
def connect_to_channel(hostname,port,id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #print 'socket created'
    newport = int(port)+int(id)*10
    #sock.bind(("localhost", newport))

    sock.bind((hostname, newport))  #James.  Replaced localhost with parameter passed in.
    
    sock.listen(1)
    return sock

# message dealt with and return temporary or permanent result from servers
def result (RN):
    fn = (RN-1)/3
    msg_lst = []  
    msg_content = ''
    msg_label = ''  
    for j in range(RN):
            #print(j)           
        #   设置IP和端口
        #host = socket.gethostname()
        #print(host)
        #host ='130.85.240.1' #'newsverification-VirtualBox'#
        host = '127.0.0.1'
        mySocket = connect_to_channel(host,3333,j)
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
            msg = client.recv(1024)  
            #print(msg)  
            receive_msg = msg.split(';')
            msg_lst.append(receive_msg[2])
            msg_content = receive_msg[0]
            msg_label = receive_msg[1]
            #print 'receive from server',j,':', msg.decode('utf-8')
            mySocket.close()
            tag = False
    if  msg_label == '1': news_label = 'final'
    else: news_label = 'temporary'
    for x in msg_lst: 
        if msg_lst.count(x)>fn+1: 
            print 'The ',news_label,'result for news verification of ', msg_content, 'is',x
            break

if __name__ == '__main__':

    
    #Server.serverpart()

    if len(sys.argv[1:])<3:
        print "Use: python BFTClient.py <process id> <increment> <number of operations>"
        exit()

    processID = sys.argv[1]
    increment = sys.argv[2]
    nops = sys.argv[3]
    num = nops.split(';')
    #print(processID,increment,len(num),type(nops))
    print 'Client',processID, 'requests to verify', len(num),'pieces of news'
    
    # judege whether the news is in the finalresult table
    #db_final = leveldb.LevelDB('./finalresult') # hash(msg) + result    
    #sample
    #db_final.Put(str(hash('I am a good student')),'True:0.9')
    
    classpath = "lib/commons-codec-1.5.jar:lib/core-0.1.4.jar:lib/netty-all-4.1.9.Final.jar:lib/slf4j-api-1.5.8.jar:lib/slf4j-jdk14-1.5.8.jar:bft-smart/bin/BFT-SMaRt.jar"
    startJVM(getDefaultJVMPath(),"-Djava.class.path=%s"%classpath)

    # you can then access to the basic java functions
    #java.lang.System.out.println("hello world")

    KVClientClass = JPackage("bftsmart.demo.keyvalue")
    #KVClientClass.KVClient.test()
    KVClientClass.KVClient.passArg((processID,increment,str(len(num))))


    for i in range(len(num)):
        hash_msg = str(hash(num[i]))
        # in current version, we don't care about client's memory, they can ask the the same news
        #if db_exist(db_final,hash_msg): 
         #   print 'The final result for news verification of ', str(num[i]), 'is',db_final.Get(hash_msg)
        #else:
        KVClientClass.KVClient.sendRequest(num[i].decode('utf-8').strip()) #+'//:'+processID

        #accept from servers, need to record server
         # receive and read from server
        #RN = replica numbers
        RN = 4
        result(RN)
        
    shutdownJVM()


   

