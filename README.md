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
