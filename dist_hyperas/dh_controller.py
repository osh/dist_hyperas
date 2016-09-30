#!/usr/bin/env python
import worker,controller
import dh_worker
import json,pprint

class ControllerDH(controller.Controller):
    def __init__(self, fn, model, dataset):
        self.cfg = json.load(open("target.json"))
        pprint.pprint(self.cfg)

        # load model and dataset
        self.dataset = open(dataset,'r').read()
        self.model = open(model, 'r').read()

        # launch proceses and go into event loop
        controller.Controller.__init__(self, self.cfg, dh_worker.Worker, self.cfg["devices"])
        self.start()

    def on_start(self):
        pass
    
    def on_available(self, stream):
        print "launching new model to worker..."
        self.stream.send_json( ("run_model",self.dataset,self.model) )

    def on_model_failure(self, stream, ds_hash, model_hash):
        print "things broke, shutting down."
        self.shutdown()

    def on_model_success(self, stream, ds_hash, model_hash):
        print "great success"
    
if __name__ == "__main__":
    ControllerDH("target.json")


