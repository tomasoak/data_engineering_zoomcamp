<h1 align="center"> Instructions for Week 02 </h1>

<h2 align="center">Notes from the second week of the Data Engineering ZoomCamp</h2>

<br>
<br>
<br>

### Introduction to Workflow orchestration 
```
python3 -m pip install prefect prefect-sqlalchemy prefect-gcp
```

### Prefect UI
```bash
prefect orion start
```

### Activate blocks
```bash
prefect block register -m prefect_gcp
```

### Deployment from Prefect
```bash
prefect deployment build <script_name.py:etl_parent_flow> -n <"name it">
```

### Apply the deployment 
```bash
prefect deployment apply etl_parent_flow-deployment.yaml
```

### After running from the UI 
```bash
prefect agent start --work-queue "default" 
```

### Create a docker image and push it to Docker hub
1. Create a `Dockerfile`
```bash
docker image build -t tomasoak/prefect:zoom .
docker image push tomasoak/prefect:zoom
```

### Running flow in Docker
1. Create a docker block through prefect UI or python see `blocks/make_docker_blocks.py`
2. Create a `docker_deploy.py` and run:
```bash
python flows/docker_deploy.py
```

### Check prefect profile and set a API URL
```bash
prefect profile ls
prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"
```


### Start agent to look for the default work queue
```bash
prefect agent start -q default
```

-p overwrites the parameters
```bash 
prefect deployment run etl-parent-flow/docker-flow -p "months=[1,2]"
```

### WSL and Prefect connection error - IPv4 x IPv6
Likely associated with how WSL handles IPv4 addresses, as in this issue: WSL by default will bind to an IPv6 address, which Prefect does not appear to handle.
1. In a WSL terminal, run the command `ip addr` to find the subsystem IP
2. While in WSL, start Prefect Orion with that IP address as host:
```bash
prefect orion start --host 172.20.115.88
```
3. While in WSL, set the Prefect API to that IP address. The exact code for this should be displayed when you start Prefect Orion in the step above.
```bash
prefect config set PREFECT_API_URL="http://172.31.211.36:4200/api"
```
