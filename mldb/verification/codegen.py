"""
This class provides the function decorators to
infer what type of an operation is happening.
"""
import sys
import inspect
import datetime
import pickle
import base64

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

	#collect all of the imports
	importString = __extractAllImports(mldb)
	program_code = importString + "import pickle\nimport base64\n\n" 

	#collect all of the udfs
	for p in mldb.pipeline:
		program_code = program_code + __process_lines(inspect.getsourcelines(p.func)[0])

	#generate exec function
	exec_code = "\ndef runAll(data): \n"
	for p in mldb.pipeline:
		#get the def
		fname = __get_def_line(inspect.getsourcelines(p.func)[0])

		#setup the arguments
		argin, inputtype, outputtype = p.getHints()
		for a in range(0,len(p.args)):
			if a != argin:
				pickeledString = pickle.dumps(p.args[a], protocol=0)
				varname = fname+"_"+ str(a)
				varstring = varname + ' = pickle.loads(base64.decodestring(\'' + base64.b64encode(pickeledString)+'\'))'
			else:
				varname = fname+"_"+ str(a)
				varstring = varname + ' = data'

			exec_code = exec_code + '\t' + varstring + '\n'

		argnames = ','.join([fname+"_"+ str(a) for a in range(0,len(p.args))])
		exec_code = exec_code + '\tdata = ' + fname + '(' + argnames + ")" + '\n'

	exec_code = exec_code + '\treturn data \n'

	return program_code + exec_code

def __get_def_line(lines):

	for l in lines:
		if 'def ' in l:
			fsig = l.strip().split(" ")[1]
			fname = fsig.split("(")[0]
			return fname

	return None



def __process_lines(lines):
	"""
	This function processes the lines by stripping output
	mldb meta data and extra tabs.
	"""
	first_def = True
	num_tabs = 0
	plines = []

	for l in lines:
		if '@pipeline_stage' in l:
			continue
		elif first_def and 'def ' in l:
			num_tabs = l.index('def')
			first_def = False

		plines.append(l[num_tabs:])

	return ''.join(plines)




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

