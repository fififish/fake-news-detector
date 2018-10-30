import parsingconfig
from jpype import *
import sys
import socket
from io import BytesIO
import struct
import vector
import logistic_regression
import SVM
import csv
import leveldb
import invite_reviewers

def db_exist(db,key):
    try:
        db.Get(key)
        return True
    except KeyError:
        return False

#Since we deliver message from java module to python module, 
#I think it is ok to just use this socket function to directly
#deliver and process the message
#Need to figure out whether it is true. 
# connecting to the client
def connect_to_channel2(hostname,port,id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #print 'socket created'
    newport = int(port)+int(id)*10
    #sock.bind(("localhost", newport))
    sock.connect((hostname, newport))
    return sock

def connect_to_channel(host,port,id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print 'socket created'
    newport = int(port)+int(id)
    sock.bind((host, newport))
    sock.listen(1)
    return sock

def listen_to_channel(sock):
    message = ''
    while 1:
        conn,addr = sock.accept()
        #print 'let us do it'
        print "got a message..."
        try:
            buf = conn.recv(1024)
            #print(addr)
            #print buf
            tmp = BytesIO(buf)
            sequence,cid,length = struct.unpack('>iii', tmp.read(12))
            msg = tmp.read(length)
            #msg = msg.split('//:')
            print(msg)
            #message.append(msg)
            hash_msg = str(hash(msg))
            if db_exist(db_final,hash_msg): reuslt = '1' + ';' + db_final.Get(hash_msg)
            elif db_exist(db_temp,hash_msg): 
                result = '0' + ';' + db_temp.Get(hash_msg)
                #adopt reviewers to make temp be forever
                final_label = invite_reviewers.result(msg,4) # adopt 4 reviewers to make the result final
                db_final.put(hash_msg,final_label)
                db_temp.Delete(hash_msg)
            else:
                filename = vector.vector(msg)
            #print logistic_regression.result(filename)
                result = logistic_regression.result(filename)
                db_temp.Put(hash_msg, result)
                db_news.Put(msg, result)
                result = '0' + ';' + result
            #print result
            message = str(msg) + ';'+ str(result)
            print(message)
            # send back
            # send to client
                #   set ip and port
            host = '127.0.0.1' # client host name
            #host = '130.85.90.21' # ALi server ip
            #host = socket.gethostname()
            tag_conn = True
            while tag_conn:
                try:
                    mySocket = connect_to_channel2(host,3333,replicaID)
                    tag_conn = False
                except: continue
            #print(11111)
                mySocket.send(message.encode())
                #mySocket.close()
            #client.clientpart(msg, result)
            #resultset.append(msg+'\n'+result)
            #print "We have assigned sequence number ", sequence, " for client ", cid, " and request ", msg
            #if msg=="Dummy Test Request":
             #   print "good."
              #  print "We have assigned sequence number ",sequence," for client ",cid, " and request ",msg
        
            # invite reviewers to review 
            

        except:
            print "may have got a not well-formatted message" 
            #TODO: Need to figure out why sometimes there are empty or not well-formatted messages
            pass
        #return result

if __name__ == '__main__':

    if len(sys.argv[1:])<1:
        print "Use: python BFTServer.py <ReplicaID>"
        exit()

    replicaID = sys.argv[1]

    #TODO: Nedd to handle configuration file to avoid hard-coded host name and port number
    configFile = "config.ini"  #Set variable to the name of the config file.
    (n,f,host,baseport) = parsingconfig.readconfig(configFile)   #Read in the config number of replicas, failures, host, and port number.
    #host = '10.0.2.15'
    sock = connect_to_channel(host,baseport,replicaID)
    db_final = leveldb.LevelDB('./finalresult{}'.format(replicaID)) # hash(msg) + result
    db_temp = leveldb.LevelDB('./tempdata{}'.format(replicaID))
    db_news = leveldb.LevelDB('./newsdata{}'.format(replicaID))

    classpath = "lib/commons-codec-1.5.jar:lib/core-0.1.4.jar:lib/netty-all-4.1.9.Final.jar:lib/slf4j-api-1.5.8.jar:lib/slf4j-jdk14-1.5.8.jar:bft-smart/bin/BFT-SMaRt.jar"
    startJVM(getDefaultJVMPath(),"-Djava.class.path=%s"%classpath)

    KVServerClass = JPackage("bftsmart.demo.keyvalue")
    KVServerClass.KVServer.passArgs((replicaID,"1"))
    
    #listen_to_channel(sock)
    #print(len(message),len(me_result))

    listen_to_channel(sock)
    #sock.send(message.encode('utf-8'))  # send back



    #sock.send(result)
    #print("news verification result of replica", replicaID, "is", result)
   # print(resultset)
    #sock.send(resultset[0])

    # and you have to shutdown the VM at the end
    shutdownJVM()
