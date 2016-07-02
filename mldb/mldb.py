"""
This is a module that defines the mldb data types
used
"""

import inspect
from numpy import ndarray, matrix
from scipy.sparse import spmatrix
import collections

#here are some constants to describe the stages
EXTRACTOR = 0
CLEANER = 1
LABELER = 2
FEATURIZER = 3
TRANSFORMER = 4
HINT_IN_STRING = '#datain:'


class mldb(object):
	"""
	This is a class that defines the main mldb object that 
	gets passed around through your program.
	"""

	def __init__(self, strict=False):
		"""
		Creating an MLDB object strict means that the code will
		raise an exception for some type issues.
		"""
		self.pipeline = []
		self.strict = strict
		self.EXTRACTOR = EXTRACTOR
		self.CLEANER = CLEANER
		self.LABELER = LABELER
		self.FEATURIZER = FEATURIZER
		self.TRANSFORMER = TRANSFORMER

	def addPipelineStage(self, func, args, output):
		"""
		Adds a mldbpstage to the pipeline, assumes in order execution
		"""
		self.pipeline.append(mldbpstage(func, args, output, self.strict))

		#print mldbpstage(func, args, output, self.strict).stagetype()


class mldbpstage(object):
	"""
	This class defines the main mldb stages
	"""

	def __init__(self, func, args, output, strict):
		self.func = func
		self.args = args
		self.output = output
		self.strict = strict

	def getHints(self):
		"""
		This extracts the hints from the source code
		"""
		#iterate through the source lines
		argin = 0
		detected_in_hint = False

		#iterate through the source lines and find the hint
		for sl in inspect.getsourcelines(self.func)[0]:
			
			#search for the in hint
			if HINT_IN_STRING in sl:
				argstr = sl.split(':')[1].strip()
				try:
					argin = int(argstr)
					detected_in_hint = True
				except ValueError:
					print "Malformed Data Argument Hint"

			#optimization
			if detected_in_hint:
				break


		#enforce that the hint exists if strict is true, else assume it is the first one
		if self.strict and not detected_in_hint:
			raise ValueError("Error Data Argument Hint Not Found")

		inputtype = type(self.args[argin])
		outputtype = type(self.output)

		#more strict error checks

		if self.strict and not (isinstance(self.args[argin], collections.Iterable)):
			raise ValueError("Data Argument In Is Not Iterable")

		if self.strict and not (isinstance(self.output, collections.Iterable)):
			raise ValueError("Data Argument Out Is Not Iterable")

		#print 'in', self.args
		#print 'out',self.output

		return argin, inputtype, outputtype

	def stagetype(self):
		"""
		This infers what the type of the stage is
		"""
		argin, inputtype, outputtype = self.getHints()

		#return stage type
		if not self.isNumerical(inputtype) and self.isNumerical(outputtype):
			return (FEATURIZER, \
					self.getRelationalDim(self.args[argin]), \
					self.getNumericalDim(self.output))

		elif self.isNumerical(inputtype) and self.isNumerical(outputtype):
			return (TRANSFORMER, \
				    self.getNumericalDim(self.args[argin]), \
					self.getNumericalDim(self.output))
		else: 
			return (self.relationalInference(self.args[argin], self.output), \
					self.getRelationalDim(self.args[argin]), 
					self.getRelationalDim(self.output))

	#determines whether the type is relational or numerical
	def isNumerical(self, t):
		return (t is ndarray \
				or t is matrix \
				or t is spmatrix)

	#infer relational stages
	def relationalInference(self, t1, t2):
		if len(t1) == 0 or len(t2) == 0:
			raise ValueError("Either the input or output is trivial")
		else:
			if isinstance(t1[0], str) and  isinstance(t2[0], str):
				return CLEANER
			elif isinstance(t1[0], str) and  isinstance(t2[0], collections.Sequence):
				return EXTRACTOR
			elif isinstance(t1[0], collections.Sequence) \
				 and  isinstance(t2[0], collections.Sequence) \
				 and len(t1[0]) < len(t2[0]):
				return EXTRACTOR
			else:
				return CLEANER

	#get relational dimensionality
	def getRelationalDim(self, t):
		#print "A", t
		if len(t) == 0:
			raise ValueError("Either the input or output is trivial")
		else:
			if isinstance(t[0], str):
				return (len(t),1)
			elif isinstance(t[0], collections.Sequence):
				return (len(t),len(t[0]))
			else:
				return (len(t),1)

	#get relational dimensionality
	def getNumericalDim(self, t):
		return t.shape


	#override for pretty printing
	def __str__(self):
		s = "\n"
		s = s + "Executed Function with args " + str(self.args) + "\n"
		s = s + str(inspect.getsourcelines(self.func)) + "\n"
		s = s + "Output" + str(type(self.output)) + "\n"
		return s

	def __repr__(self):
		return self.__str__()

