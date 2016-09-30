#!/usr/bin/env python
import worker
import os,json,sys,traceback

class Worker(worker.Worker):
    def __init__(self, *args, **kwargs):
        worker.Worker.__init__(self,*args,**kwargs)
        self.busy = False
        self.datasets = {}

    def on_start(self):
        os.environ["KERAS_BACKEND"] = "theano"
        os.environ["THEANO_FLAGS"]  = "device=%s"%(self.args)
        import theano,keras

    def on_ping(self):
        if not self.busy:
            self.socket.send_json( ("available",) )

    def on_shutdown(self):
        self.shutdown()

    def on_run_model(self,dataset,model):
        self.busy = True
        ds_hash = hash(dataset)
        model_hash = hash(model)
        if not self.datasets.has_key(ds_hash):
            print "loading new dataset: ", ds_hash
            try:
                exec dataset
                self.datasets[ds_hash] = locals()["train_model"]
            except Exception,err:
                print " ********************************* "
                traceback.print_exc()
                print " *** Dataset Python is Broken! *** "
                self.socket.send_json( ("dataset_failure", ds_hash, model_hash ) )
                self.shutdown()
                return
    
        try:
            exec model
            model_factory = locals()["build_model"]
            model = model_factory()
            self.datasets[ds_hash](model)
        except Exception,err:
            print " ********************************* "
            traceback.print_exc()
            print " *** Model Python is Broken! *** "
            self.socket.send_json( ("model_failure", ds_hash, model_hash ) )
            self.shutdown()
            return
        
        self.busy = False
        self.socket.send_json( ("model_success", ds_hash, model_hash ) )
