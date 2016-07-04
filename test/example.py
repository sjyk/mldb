#!/usr/bin/env python

import numpy as np
from mldb.verification.pipelineinference import *
from mldb.mldb import mldb



m = mldb()

@pipeline_stage(m, True)
def f(x):
	#datain: 0
	return np.random.randn(100,1)

print f([1])