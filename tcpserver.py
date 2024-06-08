import socket
import threading


def agree_message():
    Type = 2
    # agree报文格式
    message = Type.to_bytes(2,'big')
    return message


def reverseAnswer_message(msg):
    Type = 4
    length = int.from_bytes(msg[2:6],'big')
    Data = msg[6:].decode('utf-8')
    # 使用切片操作将字符串反转
    reverseData = Data[::-1]
    # reverseAnswer报文格式
    message = Type.to_bytes(2,'big')+length.to_bytes(4,'big')+reverseData.encode('utf-8')
    return message


def server_to_client(clientsoket, clientaddress):
    while True:
        msg = clientsoket.recv(2048)
        if not msg:
            break
        msg_type = int.from_bytes(msg[:2],'big')  # 字节类型转换
        if msg_type == 1:  # initialization报文
            clientsoket.send(agree_message())
        elif msg_type == 3:  # reverseRequest报文
            clientsoket.send(reverseAnswer_message(msg))
    clientsoket.close()
    print(f"client:{clientaddress[0]},{clientaddress[1]}已关闭")


server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1',8888))
server_socket.listen()

while True:
    client_socket, address = server_socket.accept()
    # 创建新线程
    print(f"服务器正在监听client: {address[0]},{address[1]}")
    client = threading.Thread(target=server_to_client,args=(client_socket,address))
    client.start()


