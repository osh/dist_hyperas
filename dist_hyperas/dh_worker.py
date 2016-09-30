#!/usr/bin/env python
import worker
import os,json

class Worker(worker.Worker):
    def __init__(self, *args, **kwargs):
        worker.Worker.__init__(self,*args,**kwargs)
        self.busy = False

        self.cmds = {
            "run_model":self.on_model,
            }
        
    def on_start(self):
        os.environ["KERAS_BACKEND"] = "theano"
        os.environ["THEANO_FLAGS"]  = "device=%s"%(self.args)
        import theano

    def on_ping(self):
        if not self.busy:
            self.socket.send_json( ("available",) )

    def on_rcv(self,msg):
        msg = json.loads(msg[0])
        op = msg[0]
        if op not in self.cmds.keys():
            print "Worked received invalid command: ", msg
        else:
            self.cmds[op](*msg[1:])

    def on_model(self,mdl):
        print "test model", mdl
        
        
