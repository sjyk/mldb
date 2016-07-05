# mldb
Machine Learning Debugger

To use:
```
from mldb.mldb import mldb
from mldb.verification.pipelineinference import *
```

Create an MLDB object
```
m = mldb()
```

Annotate functions in your code with decorators:
```
@pipeline_stage(m)
def my_func(x):
```

To set a break point:
```
@pipeline_stage(m, True)
def my_func(x):
```

You will then get an IPython prompt
```
mldb.n() #moves runs the function
mldb.s() #skips the function
mldb.samp(s=0.1) #samples the output by specified amount
args #input arguments
output #output data
mldb.scatter(x,y) #does what you expect
mldb.hist(x) #does what you expect
```

You can also turn a running mldb pipeline into working code:
```
from mldb.verification.codegen import *
assert(verify(m))
codegen(m)
```

Some components can be automatically generated:
```
m.synthFeaturizer()
```
