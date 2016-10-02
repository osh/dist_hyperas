#!/usr/bin/env python
import os,json,sys,traceback
import zmq,multiprocessing,time,tornado,json,copy
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
import numpy as np
import hopt,client

if __name__ == "__main__":
    uri = open(os.getenv("HOME") + "/.dh_uri","r").read()
    c = client.Client(uri)
    c.add_task("datasets/mnist.py","models/mnist_cnn_h.py")
    c.wait()
