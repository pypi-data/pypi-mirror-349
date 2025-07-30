# Remote Sensing hub toolbox (RShub)
This is Python based toolbox to run model, check status, and retrieve model results

# Supported functions
## Function 1: Run a model
```
from rstool import submit_jobs
data1 = {
    'scenario_flag': scenario_flag,
    'output_var': output_var,
    'fGHz': fGHz,
    'algorithm':algorithm,
    'scatters': scatters1,
    'project_name':project_name,
    'task_name':task_name1,
    'token': token,
    'level_required':1
}
result1=submit_jobs.run(data1)
```

## Function 2: Check Job Status
```
from rstool import submit_jobs
result=submit_jobs.check_completion(token, project_name, task_name)
print(result)
```

## Function 3: Retrieve error messages from failed jobs (if any)
```
from rstool.load_file import load_file
data = load_file(token, project_name, task_name, fGHz)
message = data.load_error_message()
```

## Function 4: Retrieve Results
```
from rshub.load_file import load_file
data1 = load_file(token, project_name, task_name1, fGHz, scenario_flag,output_var)
data_multi = data1.load_outputs()
# Using vegetation model as an example, 
# Brightness temperature and incident angles are stored in "data"
TU_all = data_multi['TU_all'] # Brightness temperature
theta_obs = data_multi['theta_obs'] # IncidentAngles
```