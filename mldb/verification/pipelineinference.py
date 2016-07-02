"""
This class provides the function decorators to
infer what type of an operation is happening.
"""
from IPython import embed; 

def pipeline_stage(mldb):
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

			output = func(*args)

			#embed()
			
			mldb.addPipelineStage(func, args, output)

			return output

		return func_wrapper

	return pipeline_wrapper



