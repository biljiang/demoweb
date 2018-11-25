import socket, time
import threading
import json
import pandas as pd

df = pd.read_csv('/home/techstar/demoweb/static/shdky/powerplant.csv',index_col=0)
J = {S: list(df[S].values) for S in df}
J_str = json.dumps(J)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('127.0.0.1', 9999))

s.listen(5)
print('Waiting for connection...')


def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')
    data = sock.recv(1024)
    sock.sendall(J_str.encode('utf-8'))
    '''
    i=0
    while True:
        data = sock.recv(1024)
        #time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.sendall(J_str.encode('utf-8'))
        sock.send(b'')
        i+=1
    '''
    sock.close()
    print(data.decode())
    print('Connection from %s:%s closed.' % addr)



while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()



