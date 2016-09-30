#!/usr/bin/env python
import worker
import os,json

class Worker(worker.Worker):
    def __init__(self, *args, **kwargs):
        worker.Worker.__init__(self,*args,**kwargs)
        self.busy = False

    def on_start(self):
        os.environ["KERAS_BACKEND"] = "theano"
        os.environ["THEANO_FLAGS"]  = "device=%s"%(self.args)
        import theano

    def on_ping(self):
        if not self.busy:
            self.socket.send_json( ("available",) )

    def on_run_model(self,mdl):
        print "test model", mdl
        
        
