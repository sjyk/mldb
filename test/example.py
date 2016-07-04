#!/usr/bin/env python

import numpy as np
from mldb.verification.pipelineinference import *
from mldb.verification.codegen import *
from mldb.mldb import mldb



m = mldb()

def g():
	@pipeline_stage(m)
	def f(x,y=np.array([1,1]),z=4):
		#datain: 0
		return ['a', 'a', 'b', 'c']

	a = f(1,np.array([1,1]))

	@pipeline_stage(m)
	def h(x,y,z=4):
		#datain: 1
		return ['a', 'a', 'b', 'c']

	h(1,a,2)

	print codegen(m)

g()