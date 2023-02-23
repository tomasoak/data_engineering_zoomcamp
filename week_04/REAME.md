<h1 align="center"> Instructions for Week 04 </h1>

<h2 align="center">Notes from the forth week of the Data Engineering ZoomCamp</h2>

<br>
<br>
<br>

### Starting a dbt project
Install `dbt-core` and (for local project) `dbt-postgres` and (for cloud) `dbt-bigquery`
```bash
python3 -m pip install dbt-core dbt-postgres dbt-bigquery
```

Start dbt
```bash
dbt init
```

Running first model
```bash
dbt run --model models/example/my_first_dbt_model.sql
```