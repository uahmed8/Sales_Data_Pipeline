# Sales_Data_Pipeline
Intructions for Data Pipeline execution:

Create a folder:

`mkdir Sales_Data_Pipeline`
`cd Sales_Data_Pipeline`

clone the project in this folder
`git clone git@github.com:](https://github.com/uahmed8/Sales_Data_Pipeline.git`
`cd Sales_Data_Pipeline`

You should have all files inside this folder, here is description about each file:
#Dockerfiles


Execution commands step:

`docker-compose up`

This command will build the images having the dependencies.

This execution will take a few minutes. Once the execution is done then as per the python code the transformed and aggregated data should be stored into the database. There will be some png files (average_order_quantity_per_product, Average_Order_Value_per_City, Monthly_Sales_trend, Quarterly sales trend etc...) made inside current repository folders. These are aggregated data visualization in pictures png format.

Steps to visualize the stored transformed and aggregated data in tables inside Postgresql Database:
Step one: Open browser and type `https:localhost:5000`
There will occur a gui of pgAdmin - give credentials mentioned below:
userrname: `admin@admin.com`
password: `admin`

Then give






