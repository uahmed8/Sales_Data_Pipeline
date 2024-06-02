create schema retail_info;


CREATE TABLE if not exists retail_info.sales_data (
  order_id int NOT NULL, 
  customer_id int NOT NULL, 
  product_id int NOT NULL, 
  quantity int NOT NULL, 
  price float NOT NULL, 
  order_date date NOT NULL,
  PRIMARY key (order_id,customer_id,order_date)
);

CREATE TABLE if not exists retail_info.user_data (
  id int PRIMARY KEY, 
  name varchar(255) NOT NULL, 
  username varchar(55) NOT NULL, 
  email varchar(55) NOT NULL, 
  phone varchar(75) NOT NULL, 
  website varchar(75) NOT NULL,
  street_address varchar(255) NOT NULL, 
  suite_address varchar(255) NOT NULL, 
  city_address varchar(55) NOT NULL, 
  zipcode_address varchar(55) NULL, 
  geo_lng_address decimal(8,2) NOT NULL, 
  geo_lat_address decimal(8,2) NOT NULL,  
  company_name varchar(75) NOT NULL, 
  company_catchPhrase varchar(255) NOT NULL, 
  company_bs varchar(255) NOT NULL 
);

CREATE TABLE if not exists retail_info.weather_data (
  customer_id int PRIMARY KEY, 
  weather_condition varchar(255) NOT NULL, 
  weather_description varchar(255) NOT NULL, 
  temperature decimal(8,2) NOT NULL, 
  min_temperature decimal(8,2) NOT NULL, 
  max_temperature decimal(8,2) NOT NULL,
  pressure int NOT NULL, 
  humidity int NOT NULL, 
  wind_speed decimal(8,2) NOT NULL
);


CREATE TABLE if not exists retail_info.sales_per_customer (
  customer_id int PRIMARY KEY, 
  total_sales_amount float NOT NULL
);

CREATE TABLE if not exists retail_info.products_avg_sales_quantity (
  product_id int PRIMARY KEY, 
  avg_sales_quantity decimal(8,2) NOT NULL
);

CREATE TABLE if not exists retail_info.top_selling_customers (
  customer_id int PRIMARY KEY, 
  total_sales decimal(8,2) NOT NULL
);

CREATE TABLE if not exists retail_info.top_selling_products (
  product_id int PRIMARY KEY, 
  total_sales decimal(8,2) NOT NULL
);

CREATE TABLE if not exists retail_info.sales_in_weather (
  weather_condition varchar(55) PRIMARY KEY, 
  average_sales decimal(8,2) NOT NULL
);

CREATE TABLE if not exists retail_info.avg_sales_per_city (
  city varchar(55) PRIMARY KEY, 
  avg_sales_value decimal(8,2) NOT NULL
);

CREATE TABLE if not exists retail_info.sales_per_website (
  website varchar(155) PRIMARY KEY, 
  total_sales int NOT NULL
);

CREATE TABLE if not exists retail_info.monthly_sales (
  year_month varchar(155) PRIMARY KEY, 
  total_sales int NOT NULL
);

CREATE TABLE if not exists retail_info.quarterly_sales (
  year_quarter varchar(155) PRIMARY KEY, 
  total_sales int NOT NULL
);
