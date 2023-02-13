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