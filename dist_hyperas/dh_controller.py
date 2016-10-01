#!/usr/bin/env python
import worker,controller
import dh_worker
import json,pprint,time,uuid

class ControllerDH(controller.Controller):
    def __init__(self, fn):
        self.cfg = json.load(open("target.json"))
        pprint.pprint(self.cfg)

        self.tasks = {
            "active":{},
            "finished":{}
            }
            
#        # load model and dataset
#        self.dataset = open(dataset,'r').read()
#        self.model = open(model, 'r').read()

        # launch proceses and go into event loop
        controller.Controller.__init__(self, self.cfg, dh_worker.Worker, self.cfg["devices"])

    def on_start(self):
        pass
    
    def on_available(self, stream, args):
        print "worker available",args
        if(len( self.tasks["active"].values() )>0):
            tid = self.tasks["active"].keys()[0]
            work = self.tasks["active"][tid]["work"].pop()
            (dataset,model) = work
            print "sending work from tid",tid
            self.stream.send_json( ("run_model",tid,dataset,model) )
        else:
            print "no work available"

    def on_model_failure(self, stream, ds_hash, model_hash):
        self.shutdown()

    def on_dataset_failure(self, stream, ds_hash, model_hash):
        self.shutdown()

    def on_model_success(self, stream, args, ds_hash, model_hash, results):
        print time.time(), "Model returned results:", args, ds_hash, model_hash, results


    def on_submit_task(self, stream, task, work_list):
        tid = str(uuid.uuid1())
        task = {
            "owner":stream,
            "work":work_list
            }
        self.tasks["active"][tid] = task
        return tid


    
if __name__ == "__main__":
    ControllerDH("target.json")


