import socket
import random
import sys
import time


def initialization_message(total_num):
    message_type=1
    message=message_type.to_bytes(2,'big')+total_num.to_bytes(4,'big')
    return message


def reverseRequest_message(string):
    message_type=3
    string_length=len(string)
    byte_string=string.encode('utf-8')
    message=message_type.to_bytes(2,'big')+string_length.to_bytes(4,'big')+byte_string
    return message



server_ip=sys.argv[1]
server_port=int(sys.argv[2])
path=sys.argv[3]
lmin=int(sys.argv[4])
lmax=int(sys.argv[5])
string_list=[]
reverse_list=[]

client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((server_ip,server_port))

# 随机确定长度和块数
with open(path,"r") as f:
    while True:
        length=random.randint(lmin,lmax)
        content=f.read(length)
        if not content:
            break
        string_list.append(content)
total=len(string_list)

# 建立连接
client_socket.send(initialization_message(total))
response=client_socket.recv(2048)
response_type=int.from_bytes(response[:2])

# 发送reverse request
if response_type==2:
    for i in range(total):
        client_socket.send(reverseRequest_message(string_list[i]))
        receive=client_socket.recv(2048)
        receive_type=int.from_bytes(receive[:2])
        if receive_type==4:
            reverseAnswer=receive[6:].decode('utf-8')
            reverse_list.append(reverseAnswer)
            print(f"第{i+1}块：{reverseAnswer}")
            time.sleep(3)

client_socket.close()

# 将反转后的写入文件
reverseData="".join(reverse_list[::-1])
with open('reverse.txt','w') as rf:
    rf.write(reverseData)







