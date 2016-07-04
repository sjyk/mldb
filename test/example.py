#!/usr/bin/env python

import numpy as np
from mldb.verification.pipelineinference import *
from mldb.verification.codegen import *
from mldb.mldb import mldb



m = mldb()

@pipeline_stage(m)
def f(x):
	#datain: 0
	return ['a', 'a', 'b', 'c']

f(1)

print codeGen(m)