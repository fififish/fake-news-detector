# import parsingconfig
from jpype import *
import sys
import socket
from io import BytesIO
import struct
import vector
import logistic_regression
import SVM
import csv
import client
import leveldb


def db_exist(db, key):
    try:
        db.Get(key)
        return True
    except KeyError:
        return False


def handle_client_connection(sock):
    buf = sock.recv(1024)
    # reply = decode(buf)
    sock.send(buf.encode('utf-8'))


# db.Put('foo','hahhah') #put in
# print db.Get('foo')    #get back

# Since we deliver message from java module to python module,
# I think it is ok to just use this socket function to directly
# deliver and process the message
# Need to figure out whether it is true.
def connect_to_channel(hostname, port, id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print
    'socket created'
    newport = int(port) + int(id)
    sock.bind(("localhost", newport))
    sock.listen(1)
    return sock


def listen_to_channel(sock):
    message = ''
    while 1:
        conn, addr = sock.accept()
        # print 'let us do it'
        print
        "got a message..."
        try:
            buf = conn.recv(1024)
            print(addr)
            # print buf
            tmp = BytesIO(buf)
            sequence, cid, length = struct.unpack('>iii', tmp.read(12))
            msg = tmp.read(length)
            # msg = msg.split('//:')
            print(msg)
            # message.append(msg)
            hash_msg = str(hash(msg))
            if db_exist(db_temp, hash_msg):
                result = db_temp.Get(hash_msg)
            else:
                filename = vector.vector(msg)
                # print logistic_regression.result(filename)
                result = logistic_regression.result(filename)
                db_temp.Put(hash_msg, result)
                db_news.Put(msg, result)
            print result
            message = str(msg) + ';' + str(result)
            print(message)
            # send back

            # client.clientpart(msg, result)
            # resultset.append(msg+'\n'+result)
            # print "We have assigned sequence number ", sequence, " for client ", cid, " and request ", msg
            # if msg=="Dummy Test Request":
            #   print "good."
            #  print "We have assigned sequence number ",sequence," for client ",cid, " and request ",msg
        except:
            print
            "may have got a not well-formatted message"
            # TODO: Need to figure out why sometimes there are empty or not well-formatted messages
            pass
        # return result


if __name__ == '__main__':

    if len(sys.argv[1:]) < 1:
        print
        "Use: python BFTServer.py <ReplicaID>"
        exit()

    replicaID = sys.argv[1]

    # TODO: Nedd to handle configuration file to avoid hard-coded host name and port number
    # (n,f,host,baseport) = parsingconfig.readconfig()
    print(replicaID)
    sock = connect_to_channel("localhost", 5000, replicaID)
    db_temp = leveldb.LevelDB('./tempdata{}'.format(replicaID))
    db_news = leveldb.LevelDB('./newsdata{}'.format(replicaID))

    classpath = "lib/commons-codec-1.5.jar:lib/core-0.1.4.jar:lib/netty-all-4.1.9.Final.jar:lib/slf4j-api-1.5.8.jar:lib/slf4j-jdk14-1.5.8.jar:bft-smart/bin/BFT-SMaRt.jar"
    startJVM(getDefaultJVMPath(), "-Djava.class.path=%s" % classpath)

    KVServerClass = JPackage("bftsmart.demo.keyvalue")
    KVServerClass.KVServer.passArgs((replicaID, "1"))

    # listen_to_channel(sock)
    # print(len(message),len(me_result))

    listen_to_channel(sock)
    # sock.send(message.encode('utf-8'))  # send back

    # sock.send(result)
    # print("news verification result of replica", replicaID, "is", result)
    # print(resultset)
    # sock.send(resultset[0])

    # and you have to shutdown the VM at the end
    shutdownJVM()
