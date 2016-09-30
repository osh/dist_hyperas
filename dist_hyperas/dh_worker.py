#!/usr/bin/env python
import worker
import os,json,sys

class Worker(worker.Worker):
    def __init__(self, *args, **kwargs):
        worker.Worker.__init__(self,*args,**kwargs)
        self.busy = False
        self.datasets = {}

    def on_start(self):
        os.environ["KERAS_BACKEND"] = "theano"
        os.environ["THEANO_FLAGS"]  = "device=%s"%(self.args)
        import theano,keras
        pass

    def on_ping(self):
        if not self.busy:
            self.socket.send_json( ("available",) ) or sys.exit(0)

    def on_run_model(self,dataset,model):
        print "worker run model..."
#        self.busy = True
#        ds_hash = hash(dataset)
#        model_hash = hash(model)
#        if not self.datasets.has_key(ds_hash):
#            print "loading new dataset: ", ds_hash
#            exec dataset
#            self.datasets[ds_hash] = locals()["train_model"]
#            print "dataset loaded"
    
#        try:
#            exec model
#            model_factory = locals()["build_model"]
#            self.datasets[ds_hash](model_factory)
#        except Exception as inst:
#            print "Model Failed!"
#            print inst
#            self.socket.send_json( ("model_failure", ds_hash, model_hash ) )
#            self.shutdown()
        
        self.busy = False
        self.socket.send_json( ("model_success", ds_hash, model_hash ) )
