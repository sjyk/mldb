"""
This class provides the function decorators to
infer what type of an operation is happening.
"""
import sys
import inspect

def pipeline_stage(mldb, breakpoint=False):
	"""
	This decorator defines a pipeline stage
	and infers what type of an operation it
	is.

	Takes in an mldb object
	"""

	def pipeline_wrapper(func):

		"""
		Higher order function to wrap this into an
		easy interface.
		"""

		def func_wrapper(*args):

			#catch all exceptions
			try:
				output = func(*args)
				e = ""
			except:
				output = [None]
				e = sys.exc_info()[0]

			mldb.addPipelineStage(func, args, output, e)

			#launch interpeter if break point
			if breakpoint:
				interpreter = mldb.embed(func)
				interpreter()

			return mldb.getOutput(func)

		return func_wrapper

	return pipeline_wrapper



