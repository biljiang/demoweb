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
import multiprocessing
    
MG= multiprocessing.Manager()
pg_dict=MG.dict()   #主进程与子进程共享这个字典
pg_list=MG.list(range(5)) 
lock = multiprocessing.Lock()

consumer = KafkaConsumer("PGsimulation",bootstrap_servers='m3:9092,m4:9092',group_id = 'PG_simu_con_1')
received_msg_counter = multiprocessing.Value("d",0)


def handler(signalnum, frame):
    global consumer, received_msg_counter
    print ("\nTotal",received_msg_counter.value,"messages processed.")
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
 
def pg_consumer(pg_dict, pg_list, received_msg_counter):
    
    global consumer#,received_msg_counter
    print ("pg_consumer_pid:", os.getpid())
    print ("Connected to kafka Topic PGsimultion...") 
    for msg in consumer:
        print(datetime.fromtimestamp(msg.timestamp/1000))
        #print(msg.value.decode())
        J = json.loads(msg.value.decode())
        #lock.acquire()
        for k in J:
            pg_dict[k]=J[k]
        #lock.release()
        received_msg_counter.value +=1
        
        
        
def pg_tcp_service(pg_dict): 
    print ("pg_tcpservice_pid:", os.getpid())    
    while True:
        time.sleep(3)
        print("nothing")

if __name__ == '__main__':
    #main()   # uncomment this line and delete following will serve pg_ajax with file
    print ("main_pid:", os.getpid())
    signal.signal(signal.SIGINT, handler)
 
    
  
    p1=multiprocessing.Process(target=pg_consumer,args=(pg_dict,pg_list,received_msg_counter))
    p1.start()
    #p1.join()
    
    #print("Process 2 starting")
    
    
    while True:
        time.sleep(2)
        print(pg_dict.values())    
        
    # always raise error p2=multiprocessing.Process(target=pg_tcp_service,args=(pg_dict))
    # always raise error p2.start()

        




