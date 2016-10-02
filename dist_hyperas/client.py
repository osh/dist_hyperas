#!/usr/bin/env python
import os,json,sys,traceback
import zmq,multiprocessing,time,tornado,json,copy
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
import numpy as np
import hopt

class Client:
    def __init__(self, uri):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.connect (uri)
        #self.stream = ZMQStream(self.socket)

    def add_task(self, ds, mdl):
        ds = open(ds,'r').read()
        src = open(mdl,"r").read()
        src,info = hopt.extract_hopts(src)
        ss_size = np.product( map(lambda x: len(x["options"]), info.values() ) )
        print "Search space size: ", ss_size
        w = []
        for i in range(0,ss_size):
            info_i,src_i = hopt.produce_variant(src,copy.deepcopy(info),i)
            info_i["subtask"] = i
            w.append( (info_i,ds,src_i) )

        print "submitting task..."
        rv = self.socket.send_json(("submit_task", w))
        print rv

    def wait(self):
        while True:
            msg = self.socket.recv()
            print msg

