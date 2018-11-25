#! /home/techstar/anaconda3/bin/python
# -*- coding: utf-8 -*-
import os,sys
from kafka import KafkaProducer,KafkaConsumer
import json
import pandas as pd
import time
import signal
import daemon
from datetime import datetime
import threading,socket

consumer = KafkaConsumer("PGsimulation",bootstrap_servers='m3:9092,m4:9092',group_id = 'PG_simu_con_1')
received_msg_counter = 0
lock = threading.Lock()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 9999))
s.listen(5)

df = pd.DataFrame()

def handler(signalnum, frame):
    global consumer, received_msg_counter
    print ("\nTotal",received_msg_counter,"messages processed.")
    print ("Received SIGINT",signalnum,"close Consumer and exit!")
    consumer.close()
    sys.exit() # 自己走


def pg_tcp_service(sock, addr):
    global df
    #print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')
    data = sock.recv(1024)
    #print(data.decode())# receive client acknowledgement and print
    if lock.acquire():
        df['time'] = df.index/1.0
        #df['time'] = df['time'].apply(str)
        J = {S: list(df[S].values) for S in df}
        lock.release()
    J_str = json.dumps(J)    
    sock.sendall(J_str.encode('utf-8'))
    #print(J_str)
    sock.close()
    #print('Connection from %s:%s closed.' % addr)    
    
    
 
def pg_consumer():
    
    global consumer,received_msg_counter, df
    print ("pg_consumer_pid:", os.getpid())
    print ("Connected to kafka Topic PGsimultion...") 
    for msg in consumer:
        #print(datetime.fromtimestamp(msg.timestamp/1000))
        #print(msg.value.decode())
        s=pd.read_json(msg.value.decode(),typ='series')
        s.name= msg.timestamp
        #print (s)
        df = df.append(s)
        df = df[-100:]
        if (received_msg_counter % 1000)==0:
            print(datetime.fromtimestamp(msg.timestamp/1000))
            print ("message#",received_msg_counter)
        received_msg_counter +=1
        
        
        

if __name__ == '__main__':
    #main()   # uncomment this line and delete following will serve pg_ajax with file
    print ("main_pid:", os.getpid())
    signal.signal(signal.SIGINT, handler)
 
    try:
        t1 = threading.Thread(target=pg_consumer, args=())
        t1.start()
    except:
        pass
    time.sleep(10)
    
    
    while True:
        # 接受一个新连接:
        sock, addr = s.accept()
        # 创建新线程来处理TCP连接:
        t2 = threading.Thread(target=pg_tcp_service, args=(sock, addr))
        t2.start()




