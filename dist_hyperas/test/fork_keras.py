#!/usr/bin/env python
import os
a = os.fork()
gpuid = 1 if a ==0 else 2
os.environ["KERAS_BACKEND"] = "theano"
os.environ["THEANO_FLAGS"]  = "device=gpu%d"%(gpuid)
import keras
