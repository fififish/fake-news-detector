#coding:utf-8
# receive msg results from reviewers
#import parsingconfig
from jpype import *
#from ..threshenc.tdh2 import encrypt,decrypt
import socket
import random
import BFTReviewer

def connect_to_channel(hostname,port,id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #print 'socket created'
    newport = int(port)+int(id)
    #sock.bind(("localhost", newport))
    sock.connect((hostname, newport))
    return sock

# message dealt with and return results from reviewers
def result (msg,RN):
    fn = (RN-1)/3
    msg_lst = []  #directly return back the result
    for j in range(RN):
            #print(j)   #randomly select 4 reviewers from 0-15        
        #   设置IP和端口
        id = random.randint(0,1000) # get one reviewer from 0-15 #set the same 4 reviewers, later should use PRF to select 4 
        tag = True
        while tag:  
            print msg,'comes from reviewer request'          
        #   接收客户端连接
            review_result = BFTReviewer.reviewer(msg,id) 
            print 'result from reviewer',j,'is',review_result 
            msg_lst.append(review_result)
            tag = False
    for x in msg_lst: 
        if msg_lst.count(x)>fn+1: 
            #print 'The ',news_label,'result for news verification of ', msg_content, 'is',x
            return x
            break
if __name__ == '__main__':
        
    result('I am a good student, how about you?',4)    


   

