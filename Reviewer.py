# coding: utf-8
# the function of reviewers to listen news from servers and review them (ML or HI),the result 
#is used to maintain the final news result table and the server will make them consensus
# No need BFT-Smart for review side, just sending back result to servers

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

def connect_to_channel(host,port,id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print 'reviewer created'
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
            #tmp = BytesIO(buf)
            #sequence,cid,length = struct.unpack('>iii', tmp.read(12))
            #msg = tmp.read(length)
            msg  = buf.decode()
            #msg = msg.split('//:')
            #print(msg)
            #message.append(msg)
            hash_msg = str(hash(msg))
            #print(hash_msg)
            if db_exist(db_mem,hash_msg): 
                #print(22222,hash_msg)
                reuslt = db_mem.Get(hash_msg)
                #print 'get wrong'
                result = db_mem.Get(hash_msg)
                #print(result)
            else:
                #print(111)
                filename = vector.vector(msg)
                result = logistic_regression.result(filename)
                db_mem.Put(hash_msg, str(result))
                #print result
                
            tag_conn = True
            while tag_conn:
                try:
                    #print(result)
                    conn.send(result.encode())
                   
                    tag_conn = False
                except: continue

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
    port = int(baseport) + 555 # port = 5555
    sock = connect_to_channel(host,port,replicaID) # at first, start 15 reviewers for listening
    db_mem = leveldb.LevelDB('./reviewmemeory{}'.format(replicaID)) 
    # hash(msg) + result, record reviewers memory

    listen_to_channel(sock)
  
