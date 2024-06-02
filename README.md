# Sales_Data_Pipeline 
Intructions for Data Pipeline execution:

Create a folder:
```
mkdir Sales_Data_Pipeline
cd Sales_Data_Pipeline
```

clone the project in this folder
```
git clone https://github.com/uahmed8/Sales_Data_Pipeline.git
cd Sales_Data_Pipeline
```

You should have all files inside this folder, here is description about each file:

* 1- Dockerfile : It has all docker commands to prep all pre-req(dependencies) for python environment. This file is actually making image for python
* 2- code_python.py: It has all the code which is consist of multiple functions for transformation, aggregations and loading transformed/aggregaed data to database
* 3- docker-compose.yaml: This file I am using to pull and run the images
* 4- sales_data.csv: sales data using as source file
* 5-schemasql.sql: having all the requried transformed and aggregated create tables and create schema queries that will be executed the container for postgresql gets up
* DB_Diagram: This is Diagram of database schema, used to store the transformed and aggregated data.

### python code description has been made inside code_python.py file in comments.

command to run the whole project and have the data inserted in database in the end of code execution:

```
docker-compose up
```

This command will build the image having the dependencies based prepared environment.

This execution will take a few minutes. Once the execution is done then as per the python code the transformed and aggregated data should be stored into the database. There will be some png files (average_order_quantity_per_product, Average_Order_Value_per_City, Monthly_Sales_trend, Quarterly sales trend etc...) made inside current repository folders. These are aggregated data visualization in pictures png format.

Steps to visualize the stored transformed and aggregated data in tables inside Postgresql Database:
## Step one: Open browser and type 
```
http:localhost:5000
```
There will occur a gui of pgAdmin as below - give login credentials mentioned below:
![pgdmin_login_View](https://github.com/uahmed8/Sales_Data_Pipeline/assets/34869772/dcac6ceb-0934-412e-bfa7-c1a7b73261fa)

```
userrname: `admin@admin.com`
password: `pgadmin`
```
## step two: after crentendials
This view will occur and click on add new server as seen in below picture
![pgadming_view](https://github.com/uahmed8/Sales_Data_Pipeline/assets/34869772/0deabe52-5ec0-4edd-b7a7-2824f3354911)

## step three: connections part
first select name of in general part you can give it any name as seend below then give connections as it is with password: `postgresql` and click on `save`
![general](https://github.com/uahmed8/Sales_Data_Pipeline/assets/34869772/1dbf06c7-d6bc-4476-a11f-817692c01242)
![connection_creds](https://github.com/uahmed8/Sales_Data_Pipeline/assets/34869772/3d2035e8-2211-44cf-9a5e-c7677b697787)

## step four: DB Schema view with tables
as per seen in pictures there will be schema as given `retail_info` with transformed and aggregated tables.
![db_view](https://github.com/uahmed8/Sales_Data_Pipeline/assets/34869772/a720736c-0088-4e0c-97f5-1e28cdf12a19)
![schema_tables](https://github.com/uahmed8/Sales_Data_Pipeline/assets/34869772/b989fd79-cfbf-4db1-822a-08dca798ec8f)


# last step to close the docker services after full review

```
docker-compose down
```








