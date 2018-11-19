#! /home/techstar/anaconda3/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import os
import signal
import time
 
receive_times = 0
 
def handler(signalnum, frame):
    global receive_times
    print ("收到信号", signalnum, frame, receive_times)
    receive_times += 1
    if receive_times > 3:
        exit(0) # 自己走
 
def main():
    print ("pid:", os.getpid())
    signal.signal(signal.SIGINT, handler)
    while True:
        pass
 
if __name__ == '__main__':
    main()
