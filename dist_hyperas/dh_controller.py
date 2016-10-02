#!/usr/bin/env python
import worker,controller
import dh_worker
import json,pprint,time,uuid,os,zmq
import hopt

class ControllerDH(controller.Controller):
    def __init__(self, fn):
        self.cfg = json.load(open("target.json"))
        pprint.pprint(self.cfg)

        self.tasks = {
            "active":{},
            "finished":{}
            }
            
        # launch proceses and go into event loop
        controller.Controller.__init__(self, self.cfg, dh_worker.Worker, self.cfg["devices"])

    def on_start(self):
        open(os.getenv("HOME") + "/.dh_uri","w").write(self.uri)
    
    def on_available(self, identity, args):
        if(len( self.tasks["active"].values() )>0 and len(self.tasks["active"].values()[0]["work"])>0):
            tid = self.tasks["active"].keys()[0]
            work = self.tasks["active"][tid]["work"].pop()
            (info,dataset,model) = work
            info["tid"] = tid
            print "sending work from tid",tid
            self.send_json(identity, ("run_model",work) )
        else:
            pass

    def on_model_failure(self, identity, info):
        self.shutdown()

    def on_dataset_failure(self, identity, info):
        self.shutdown()

    def on_model_success(self, identity, info, results):
        print time.time(), "Model returned results:", info, results
        tid = info["tid"]
        task = self.tasks["active"][tid]
        task["work_finished"].append( (info,results) )
        self.send_json(task["owner"], ("subtask_finished", info,  results) )
        if(len(task["work_finished"])==task["n_subtask"]):
            print "Task finsihed: ",tid
            self.tasks["active"].pop(tid)
            owner = task.pop("owner")
            self.tasks["finished"] = task
            self.send_json( owner, ("task_finished",task) )

    def on_submit_task(self, identity, work_list):
        tid = str(uuid.uuid1())
        task = {
            "owner":identity,
            "work":work_list,
            "work_finished":[],
            "n_subtask":len(work_list)
            }
        self.tasks["active"][tid] = task
        self.send_json(identity,("task_queued", tid))

    def on_shutdown(self, identity):
        self.shutdown()

    
if __name__ == "__main__":
    ControllerDH("target.json")


