import socket
print("Program starts")
#   创建套接字
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#   设置ip和端口
host = socket.gethostname()
port = 3333
#   连接到服务器
mySocket.connect((host, port))
#print("Connect to other end")

while True:

    #   接收消息
    print("----------------------Server sends:", end="")
    msg = mySocket.recv(1024)
    print("%s" % msg.decode('utf-8'))
    #print("Read complete")
    if msg == b"EOF":
        break
    if msg == "Bye":
        mySocket.close()
        print("Program is over\n")
        exit()

    #   发送消息
    msg = input("----------------------Client sends:")
    mySocket.send(msg.encode())
    #print("Answer")
    if msg == "EOF":
        break
    if msg == "Bye":
        mySocket.close()
        print("Program is over\n")
        exit()
print("Program is over\n")
