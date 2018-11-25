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

consumer = KafkaConsumer("PGsimulation",bootstrap_servers='m3:9092,m4:9092',group_id = 'PG_simu_con')
received_msg_counter = 0

def handler(signalnum, frame):
    global consumer, received_msg_counter
    print ("\nTotal",received_msg_counter,"messages processed.")
    print ("Received SIGINT",signalnum,"close Consumer and exit!")
    consumer.close()
    exit(0) # 自己走
 
def main():
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
 
if __name__ == '__main__':
    #with daemon.DaemonContext():
    main()


