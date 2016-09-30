#!/usr/bin/env python
import worker,controller
import dh_worker
import json,pprint

class ControllerDH(controller.Controller):
    def __init__(self, fn, model, dataset):
        self.cfg = json.load(open("target.json"))
        pprint.pprint(self.cfg)

        self.cmds = {
            "available":self.on_available_worker,
            }

        # load model and dataset
        self.dataset = open(dataset,'r').read()
        self.model = open(model, 'r').read()

        # launch proceses and go into event loop
        controller.Controller.__init__(self, self.cfg, dh_worker.Worker, self.cfg["devices"])
        self.start()


    def on_start(self):
        pass
    
    def on_rcv(self, stream, msg):
        msg = json.loads(msg[0])
        op = msg[0]
        if op not in self.cmds.keys():
            print "Controller received invalid command: ", msg
        else:
            self.cmds[op](*msg[1:])

    def on_available_worker(self):
        self.stream.send_json( ("run_model","foo") )
    
if __name__ == "__main__":
    ControllerDH("target.json")


