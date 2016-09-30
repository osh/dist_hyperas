#!/usr/bin/env python
import zmq,multiprocessing,time,tornado,json
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream

def j(x):
    return json.dumps(x)

class Worker(multiprocessing.Process):
    def __init__(self, args, controller_uri):
        multiprocessing.Process.__init__(self)
        (self.args, self.controller_uri) = (args, controller_uri)

    def run(self):
        print "Worker init."
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.connect (self.controller_uri)
        self.stream = ZMQStream(self.socket)
        self.stream.on_recv(self.on_rcv)
        self.ioloop = ioloop.IOLoop.instance()
        self.ioloop.add_callback(self.on_start)
        tornado.ioloop.PeriodicCallback(self.on_ping, 1000).start()

        print "Worker entering eventloop."
        self.ioloop.start()

    def on_rcv(self, msg):
        msg = json.loads(msg[0])
        op = msg[0]
        if(hasattr(self,"on_"+op)):
            f = getattr(self, "on_"+op)
            f(*msg[1:])
        else:
            print "Controller received invalid command: ", msg

    def on_start(self):
        print "Worker started"

    def on_ping(self):
        print "Ping running"
        self.socket.send("test")



