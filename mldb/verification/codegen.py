"""
This class provides the function decorators to
infer what type of an operation is happening.
"""
import sys
import inspect

def verify(mldb):
	"""
	This function verifies whether the input-> output chain
	of pipeline steps is consistent, i.e., there is nothing
	outside of the pipeline that affects results
	"""
	#base-case return true
	if len(mldb.pipeline) <= 1:
		return True
	else:
		output = mldb.pipeline[0].output
		for i in range(1, len(mldb.pipeline)):
			argin, inputtype, outputtype = mldb.pipeline[i].getHints()
			inputn = mldb.pipeline[i].args[argin]
			if output != inputn:
				return False
		return True


def codeGen(mldb):
	"""
	Given an mldb pipeline this function generates python code to
	execute the pipeline.
	"""
	importString = __extractAllImports(mldb)

	for p in mldb.pipeline:
		importString = importString + ''.join(inspect.getsourcelines(p.func)[0])

	return importString


def __process_lines(lines):
	"""
	This function processes the lines by stripping output
	mldb meta data and extra tabs.
	"""
	


def __extractAllImports(mldb):
	"""
	This function extracts all imports required to run the mldb
	pipeline.
	"""
	all_lines = []
	for p in mldb.pipeline:
		filename = inspect.getsourcefile(p.func)
		f = open(filename, 'rb')
		all_lines.extend(f.readlines())

	import_lines = list(set([l for l in all_lines if 'import' in l]))
	return ''.join(import_lines)

