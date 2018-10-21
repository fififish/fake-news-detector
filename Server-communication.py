import socket
print("Program starts")
#   创建套接字
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#   设置IP和端口
host = socket.gethostname()
port = 3333
#   bind绑定该端口
mySocket.bind((host, port))
#   监听
mySocket.listen(10)

while True:
    #   接收客户端连接
    #print("Waiting for connecting....")
    client, address = mySocket.accept()
    #print("New connnection")
    #print("IP is %s" % address[0])
    #print("port is %d\n" % address[1])

    while True:
        #   发送消息
        msg = input("----------------------Server sends:")
        client.send(msg.encode())
        #print("发送完成")
        if msg == "EOF":
            break
        if msg == "Bye":
            client.close()
            mySocket.close()
            print("Program is over\n")
            exit()
        #   读取消息
        msg = client.recv(1024)
        print("----------------------Client sends:", msg.decode('utf-8'))
        #print("读取完成")
        if msg == b"EOF":
            break
        if msg == b"Bye":
            client.close()
            mySocket.close()
            print("Program is over\n")
            exit()


