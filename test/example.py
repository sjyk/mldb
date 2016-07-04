#!/usr/bin/env python

import numpy as np
from mldb.verification.pipelineinference import *
from mldb.verification.codegen import *
from mldb.mldb import mldb



m = mldb()

def g():
	@pipeline_stage(m)
	def f(x,y=1,z=4):
		#datain: 0
		return ['a', 'a', 'b', 'c']

	f(1,3)

	print codeGen(m)

g()