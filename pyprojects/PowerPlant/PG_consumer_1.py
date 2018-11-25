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
import threading

consumer = KafkaConsumer("PGsimulation",bootstrap_servers='m3:9092,m4:9092',group_id = 'PG_simu_con_1')
received_msg_counter = 0
J = dict()

def handler(signalnum, frame):
    global consumer, received_msg_counter
    print ("\nTotal",received_msg_counter,"messages processed.")
    print ("Received SIGINT",signalnum,"close Consumer and exit!")
    consumer.close()
    exit(0) # 自己走
 
def main():   

    '''
    this is the main function for file sharing version. simplely 
    substitude the code under "if __name__ = 'main': " with this 
    function will provide a totally functional service for pg_ajax.    
    '''

    global consumer,received_msg_counter
    print ("pid:", os.getpid())
    print ("Connected to kafka Topic PGsimultion...")
    df = pd.DataFrame()
    signal.signal(signal.SIGINT, handler)
    for msg in consumer:
        #print(datetime.fromtimestamp(msg.timestamp/1000))
        #print(msg.value.decode())
        s=pd.read_json(msg.value.decode(),typ='series')
        s.name= datetime.fromtimestamp(msg.timestamp/1000)
        #print (s)
        df = df.append(s)
        df = df[-100:]
        if (received_msg_counter % 100)==0:
            print ("message#",received_msg_counter)
        df.to_csv('/home/techstar/demoweb/static/shdky/powerplant.csv')
        received_msg_counter +=1
 
def pg_consumer():
    
    global consumer,received_msg_counter, J
    print ("pg_consumer_pid:", os.getpid())
    print ("Connected to kafka Topic PGsimultion...") 
    for msg in consumer:
        #print(datetime.fromtimestamp(msg.timestamp/1000))
        #print(msg.value.decode())
        J = json.loads(msg.value.decode())
        #print (J)
        received_msg_counter +=1
        
        
        
def pg_tcp_service(): 
    print ("pg_tcpservice_pid:", os.getpid())    
    while True:
        time.sleep(3)
        print(J)

if __name__ == '__main__':
    #main()   # uncomment this line and delete following will serve pg_ajax with file
    print ("main_pid:", os.getpid())
    signal.signal(signal.SIGINT, handler)
 
    try:
        t1 = threading.Thread(target=pg_consumer, args=())
        t1.start()
    except:
        pass
    time.sleep(1)
    
    try:
        t2 = threading.Thread(target=pg_tcp_service, args=())
        t2.start()    
    except:
        pass

        




