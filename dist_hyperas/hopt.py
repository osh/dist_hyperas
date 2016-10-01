#!/usr/bin/env python
import re,copy
import numpy as np

hop_ops = {
    "choice":lambda x: eval(x),
    "maybe":lambda x: ["",x]
    }

def process_hopt(h):
    name,op,arg = h.split(",",2)
    return {
        "name":name,
        "op":op,
        "options":hop_ops[op](arg)
        }

def extract_hopts(source, hidx=0, info={}):
    o = source.split("{{",1)
    if(len(o)==2):
        before = o[0]
        h,after = o[1].split("}}",1)
        info[hidx] = h
        rpl = before+"++HOPT%d++"%(hidx)+after        
        return extract_hopts(rpl, hidx+1, info)
    else:
        print info
        for k,v in info.iteritems():
            info[k] = process_hopt(v)
        return source,info

def produce_variant(src, info, i=0):
    for k in sorted(info.keys()):
        opt_idx = i%len(info[k]["options"])
        rem_idx = i/len(info[k]["options"])
        r1 = "++HOPT%d++"%(k)
        r2 = info[k]["options"][opt_idx]
        info[k]["selected"] = opt_idx
        src = src.replace("++HOPT%d++"%(k), str(info[k]["options"][opt_idx]),1)
        i = rem_idx
    return info,src

if __name__ == "__main__":
    src = open("models/mnist_cnn_h.py","r").read()
    src,info = extract_hopts(src)
    ss_size = np.product( map(lambda x: len(x["options"]), info.values() ) )
    print "Search space size: ", ss_size

    for i in range(0,ss_size):
        info_i,src_i = produce_variant(src,copy.deepcopy(info),i)
        

 
