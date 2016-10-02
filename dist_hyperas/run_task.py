#!/usr/bin/env python
import os,json,sys
import time,json,copy,cPickle
import numpy as np
import hopt,client
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-m", "--model", dest="model",
                  help="which model python file to use",
                  default="models/mnist_cnn_h.py")
parser.add_option("-d", "--dataset", dest="dataset",
                  help="which dataset python file to use",
                  default="datasets/mnist.py")
parser.add_option("-u", "--uri", dest="uri",
                  help="controller URI", 
                  default= open(os.getenv("HOME") + "/.dh_uri","r").read() )
(options, args) = parser.parse_args()

a = time.time()
c = client.Client(options.uri)
print options.dataset, options.model
c.add_task(options.dataset, options.model)
results = c.wait_task_finish()
fn = "results_%s.pkl"%(str(time.time()))
cPickle.dump(results, open(fn, "wb"))
print "Finished in %ds, wrote results to %s"%(time.time()-a,fn)
        

