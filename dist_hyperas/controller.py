#!/usr/bin/env python
import json,pprint,zmq,time,sys,os,multiprocessing
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream

#  cfg: is a dict with port_min/port_max defined
#  args: is a listof args to pass to each child
#  target: is the function to fork
class Controller:
    def __init__(self, cfg, target=None, args=[]):
        (self.target,self.args) = (target,args)

        # Set up server socket
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.ROUTER)
        self.port = self.socket.bind_to_random_port('tcp://*', min_port=cfg["port_min"], max_port=cfg["port_max"], max_tries=100)
        self.uri = "tcp://127.0.0.1:%d"%(self.port)
        print "Controller listening on %s"%(self.uri)

        self.start()

    def send_json(self, identity, obj):
        self.stream.send( identity, zmq.SNDMORE )
        self.stream.send_json(obj)

    def start(self):
        # Launch worker subprocesses
        self.processes = dict(zip(self.args, map(lambda x: self.target(x,self.uri), self.args)))
        for d,p in self.processes.iteritems():
            print "Launching Worker: ", d
            p.start()

        # Start IOLoop
        self.stream = ZMQStream(self.socket)
        self.ioloop = ioloop.IOLoop.instance()
        self.ioloop.call_later(1.0, self.on_start)
        self.stream.on_recv_stream(self.on_rcv)
        try:
            self.ioloop.start()
        except KeyboardInterrupt:
            print " ** Got keyboard interrupt (^C) shutting down cleanly ... ** "
            self.shutdown()
        self.ioloop.close()
        for d,p in self.processes.iteritems():
            p.join()

    def on_start(self):
        print "Controller: start doing stuff"

    def on_rcv(self, stream, msg):
        [identity,msg] = msg
        #print identity,msg
        msg = json.loads(msg)
        op = msg[0]
        if(hasattr(self,"on_"+op)):
            f = getattr(self, "on_"+op)
            args = [identity]+msg[1:]
            f(*args)
        else:
            print "Controller received invalid command: ", msg

    def shutdown(self):
        #self.socket.send_json( ("shutdown",) )
        self.ioloop.stop()

if __name__ == "__main__":
    import worker
    conf = json.load(open("target.json"))
    Controller(conf, target=worker.Worker, args=conf["devices"])



