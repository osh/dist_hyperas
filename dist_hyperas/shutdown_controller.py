#!/usr/bin/env python
import os,json,sys,traceback
import zmq,multiprocessing,time,tornado,json,copy
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
import numpy as np
import hopt

uri = open(os.getenv("HOME") + "/.dh_uri","r").read()
context = zmq.Context()
socket = context.socket(zmq.DEALER)
socket.connect (uri)
socket.send_json( ("shutdown",))  
