#! /home/techstar/anaconda3/bin/python
# -*- coding: utf-8 -*-
import os,sys,daemon
from kafka import KafkaProducer,KafkaConsumer
import json
import pandas as pd
import time
import signal

producer = KafkaProducer(bootstrap_servers='m3:9092,m4:9092')


def handler(signalnum, frame):
    global producer
    print ("Received SIGINT",signalnum,"close Producer and exit!")
    producer.close()
    exit(0) # 自己走
 
def main():
    global producer
    print ("pid:", os.getpid())
    T = pd.read_csv("/home/techstar/PyProjects/PowerPlant/test.csv",index_col=0,float_precision='round_trip')
    signal.signal(signal.SIGINT, handler)
    while True:
        for i in range (len(T)):
            time.sleep(5)
            s_json = T.iloc[i].to_json()
            producer.send("PGsimulation",value=s_json.encode()) 


 
if __name__ == '__main__':
    #with daemon.DaemonContext():
    main()
    


