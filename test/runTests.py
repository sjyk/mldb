#!/usr/bin/env python

import numpy as np
from mldb.verification.pipelineinference import *
from mldb.verification.codegen import *
from mldb.mldb import mldb
import unittest



class TestMLDB(unittest.TestCase):

	#tests to see if the decorators add
	#stages to the pipeline correctly
	def test_pipeline_add(self):
		m = mldb()

		@pipeline_stage(m)
		def f(x):
			#datain: 0
			return np.zeros((4,5))

		self.assertTrue(m.pipeline == [])

		f([1])

		self.assertFalse(m.pipeline == [])

	#tests pipeline stage inference
	def test_pipeline_inf(self):
		m = mldb()

		@pipeline_stage(m)
		def f(x):
			#datain: 0
			return np.zeros((4,5))

		f([1])
		argin, inputtype, outputtype = m.pipeline[0].getHints()
		self.assertTrue(argin == 0)

		@pipeline_stage(m)
		def g(x,y):
			#datain: 1
			return np.zeros((4,5))

		g([1], [2])
		argin, inputtype, outputtype = m.pipeline[1].getHints()

		self.assertTrue(argin == 1)
		self.assertTrue(m.pipeline[1].stagetype()[0] == m.FEATURIZER)
		self.assertTrue(m.pipeline[1].stagetype()[1] == (1,1))
		self.assertTrue(m.pipeline[1].stagetype()[2] == (4,5))

		@pipeline_stage(m)
		def h(x):
			#datain: 0
			return [['a','a'],['b', 'b']]

		h(['a', 'b'])

		self.assertTrue(m.pipeline[2].stagetype()[0] == m.EXTRACTOR)
		self.assertTrue(m.pipeline[2].stagetype()[1] == (2,1))
		self.assertTrue(m.pipeline[2].stagetype()[2] == (2,2))

	def test_verification(self):
		m = mldb()

		self.assertTrue(verify(m))

		@pipeline_stage(m, False)
		def f(x):
			#datain: 0
			return ['a', 'a', 'b', 'c']

		a = f(1)

		self.assertTrue(verify(m))

		@pipeline_stage(m, False)
		def g(x):
			#datain: 0
			return ['1', '1', '1', '1']

		g(a)

		self.assertTrue(verify(m))

		@pipeline_stage(m, False)
		def h(x):
			#datain: 0
			return ['1', '1', '1', '1']

		h(1)

		self.assertFalse(verify(m))

if __name__ == '__main__':
    unittest.main()