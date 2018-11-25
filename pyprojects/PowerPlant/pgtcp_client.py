import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('127.0.0.1', 9999))
# 接收欢迎消息:
print(s.recv(1024).decode('utf-8'))


s.send(b'ready to receive data')
# 接收数据:


buffer = []
while True:
    # 每次最多接收1k字节:
    d = s.recv(1024)
    if d:
        buffer.append(d)
    else:
        break
    #print(d.decode('utf-8'))
data = b''.join(buffer)

#data=s.recv(30000)
print(data.decode('utf-8'))
print(len(data))
'''


for data in [b'I am OK']:
    # 发送数据:
    s.send(data)
    #s.recv(1024).decode('utf-8')
    print(s.recv(1024).decode('utf-8'))
'''


#s.send(b'exit')
s.close()



