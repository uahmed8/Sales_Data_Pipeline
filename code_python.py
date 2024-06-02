import requests
import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import psycopg2
import psycopg2.extras as extras 

#function for extracting data from sales_data.csv
def sales_extraction_transformation():
    sales_data = pd.read_csv('sales_data.csv')
    return sales_data

#function for extracting data from user API
def user_extractions_transformations():
    response1 = requests.get('https://jsonplaceholder.typicode.com/users')
    #Extract relevant fields such as id, name, username, email, lat and lng from the API response.
    users_data = response1.json()
    #changing json to panda datframe format
    user_df = pd.json_normalize(users_data)
    
    return user_df
#function for extracting data from weather API
def weather_extractions_transformations():
    # extracing users/customers information for getting geo lat and lng coords info
    user_df = user_extractions_transformations()
    #base url that will be same till this part
    base_url = 'https://api.openweathermap.org/data/2.5/weather?lat='
    #this default API I created from weather web and placed here
    api_key = '99911eb7701246efcde442b4c660763f'
    # this empty list is being created for having all pulled weather information in dictionary format for each customer
    row_list = []
    # some necessary columns name creation
    weather_columns = ['customer_id','weather_condition', 'weather_description','temperature','min_temperature','max_temperature','pressure','humidity','wind_speed']
    # creating empty dataframe with just names
    weather_df = pd.DataFrame(columns=weather_columns)
    for index, row in user_df.iterrows():
        #calling over all users for their geolocation coords to be used with weathermap base url
        url = base_url + row['address.geo.lat']+'&lon='+row['address.geo.lng'] +'&appid='+ api_key
        response2 = requests.get(url)
        response2_json = response2.json()
        # in response getting json format data and from json fetching each information value to be used in dictionary format with column name as key
        dict1 = {'customer_id': row['id'], 'weather_condition': response2_json["weather"][0]["main"],
                'weather_description':response2_json["weather"][0]["description"],'temperature':response2_json["main"]["temp"],
                 'min_temperature':response2_json["main"]["temp_min"],'max_temperature':response2_json["main"]["temp_max"],
                 'pressure':response2_json["main"]["pressure"],'humidity':response2_json["main"]["humidity"],
                'wind_speed':response2_json["wind"]["speed"]} 
        # having list of dictionary (weather columns with values pulled from weather web)
        row_list.append(dict1)
    # changing to dataframe for better tranformation and anaylsis run
    user_weather_df= pd.DataFrame(row_list)
    
    return user_weather_df
    


def final_dataset_transformation():
    # returngin all informations as dataframes and then merging them with eachother to have a final_dataset and to use that dataset dataframe aggregation
    # it is not necessary to have a final_Dataset on top of these three dataframe, it depends upon requirement if needed information can be done with either of these
    # dataframes seperately then that seems more reasonable approach
    sales_data = sales_extraction_transformation()
    user_df = user_extractions_transformations()
    user_weather_df = weather_extractions_transformations()
    sales_users_df = pd.merge(sales_data, user_df, how="inner", left_on=['customer_id'], right_on=['id'])
    # dropping one columns id as we already have same information column with name customer_id
    sales_users_df = sales_users_df.drop(columns=['id'])    
    final_dataset = pd.merge(sales_users_df, user_weather_df, how="left", on=['customer_id'])
    return final_dataset,user_df,sales_data,user_weather_df

def manip_aggreg():
    final_dataset,user_df,sales_data,user_weather_df = final_dataset_transformation()
    final_dataset.head()
    #1-Calculate total sales amount per customer.
    sales_data['total_sales'] = sales_data['quantity'] * sales_data['price']
    total_sales_per_customer = sales_data.groupby('customer_id')['total_sales'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    plt.plot(total_sales_per_customer['customer_id'].astype(str), total_sales_per_customer['total_sales'], marker='*')
    plt.xlabel('customer_id')
    plt.ylabel('total_sales_per_customer')
    plt.title('total_sales')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.savefig("total_sales_per_customer.png")


    #2-Determine the average order quantity per product.
    average_order_quantity_per_product = final_dataset.groupby('product_id')['quantity'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    plt.plot(average_order_quantity_per_product['product_id'].astype(str), average_order_quantity_per_product['quantity'], marker='*')
    plt.xlabel('Product_id')
    plt.ylabel('average_order_quantity_per_product')
    plt.title('quantity')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.savefig("average_order_quantity_per_product.png")

    #Identify the top-selling customers.
    top_selling_customers = total_sales_per_customer.sort_values('total_sales',ascending=False)
    top_selling_customers = top_selling_customers.head(3)
    
    #Identify the top-selling products
    top_selling_products = final_dataset.groupby('product_id')['total_sales'].sum().sort_values(ascending=False).reset_index()
    top_selling_products = top_selling_products.head(3)
    
    #Analyze sales trends over time (e.g., monthly or quarterly sales).
    final_dataset['order_date'] = pd.to_datetime(final_dataset['order_date'])
    final_dataset['year_month'] = final_dataset['order_date'].dt.to_period('M')
    #Monthly sales trend

    monthly_sales = final_dataset.groupby('year_month')['total_sales'].sum().reset_index()

    plt.figure(figsize=(10, 6))
    plt.plot(monthly_sales['year_month'].astype(str), monthly_sales['total_sales'], marker='*')
    plt.xlabel('Month')
    plt.ylabel('Total Sales')
    plt.title('Monthly_Sales_Trends')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.savefig("Monthly_Sales_Trends.png")
    
    #Quarterly sales trend
    final_dataset['year_quarter'] = final_dataset['order_date'].dt.to_period('Q')
    quarterly_sales = final_dataset.groupby('year_quarter')['total_sales'].sum().reset_index()
    
    plt.figure(figsize=(10, 6))
    plt.plot(quarterly_sales['year_quarter'].astype(str), quarterly_sales['total_sales'], marker='o')
    plt.xlabel('Quarter')
    plt.ylabel('Total Sales')
    plt.title('Quarterly_Sales_Trends')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.savefig("Quarterly_Sales_Trends.png")    

    # Include any other aggregations or data manipulations that you think are relevant.
    # Calculate Average Order Value (AOV)
    average_order_value = final_dataset.groupby('order_id')['total_sales'].sum().mean()
    print('######average_order_value')
    print(average_order_value)
    
    # Identify total unique number of orders made by each website
    total_orders_per_website = final_dataset.groupby('website')['order_id'].nunique().reset_index()
    total_orders_per_website.columns = ['website', 'total_orders']

    plt.figure(figsize=(10, 6))
    plt.plot(total_orders_per_website['website'].astype(str), total_orders_per_website['total_orders'], marker='o')
    plt.xlabel('website')
    plt.ylabel('total_orders')
    plt.title('total_orders_per_website')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.savefig("total_orders_per_website.png")    
    
    #average_order_value by cities
    aov_per_city = final_dataset.groupby('address.city')['total_sales'].mean().reset_index()
    aov_per_city.columns = ['city', 'average_order_value']
    
    plt.figure(figsize=(18, 6))
    plt.scatter(aov_per_city['city'], aov_per_city['average_order_value'], color='RED')
    plt.xlabel('City')
    plt.ylabel('Average Order Value')
    plt.title('Average_Order_Value_per_City')
    plt.grid(True)
    plt.tight_layout()
    plt.show()    
    plt.savefig("Average_Order_Value_per_City.png")
    
    #average sales amount per weather condition
    average_sales_per_weather = final_dataset.groupby('weather_condition')['total_sales'].mean().reset_index()
    average_sales_per_weather.columns = ['weather_condition', 'average_sales']

    plt.figure(figsize=(10, 4))
    plt.plot(average_sales_per_weather['weather_condition'].astype(str), average_sales_per_weather['average_sales'], marker='o')
    plt.xlabel('weather_condition')
    plt.ylabel('average_sales')
    plt.title('average_sales_per_weather')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.savefig("average_sales_per_weather.png")    
    
    # correlation of sales with temperature, humidity, and wind speed
    correlation_matrix = final_dataset[['temperature', 'humidity', 'wind_speed', 'total_sales']].corr()
    sales_correlation = correlation_matrix.loc['total_sales', ['temperature', 'humidity', 'wind_speed']]
    print('#####correlation of sales with temperature, humidity, and wind speed')
    print(sales_correlation)

    # Create bins dynamically using cut() function and group them total sales happened in those ranges of temperature
    final_dataset['temp_bins'] = pd.cut(final_dataset['temperature'], bins=5)
    sales_by_temp_range = final_dataset.groupby('temp_bins')['total_sales'].sum().reset_index()
    print('#####temperary made bins and the sales made in ranges of these bins')
    print(sales_by_temp_range)

    return user_df,sales_data,user_weather_df,total_sales_per_customer ,average_order_quantity_per_product,top_selling_customers,top_selling_products,monthly_sales,quarterly_sales,total_orders_per_website,aov_per_city,average_sales_per_weather
    
def insert_data(conn, df, table): 
    # tranforming columns value in tuples format inside a list to transfer the prepared whole rows into table
    tuples = [tuple(x) for x in df.to_numpy()] 
    cols = ','.join(list(df.columns)) 
    # SQL query to execute 
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    # using truncate query to have the table empty before inserting any new data as there are keys made on tables
    truncate_query = "TRUNCATE %s" % (table) 
    cursor = conn.cursor()  
    try:

        cursor.execute(truncate_query)
        conn.commit() 
        extras.execute_values(cursor, query, tuples) 
        conn.commit() 
    except (Exception, psycopg2.DatabaseError) as error: 
        print("Error: %s" % error) 
        conn.rollback() 
        cursor.close() 
        return 1
    print("data is inserted in DB for table:",table) 
    cursor.close()
    
def loading(user_df,sales_data,user_weather_df,total_sales_per_customer ,average_order_quantity_per_product,top_selling_customers,top_selling_products,monthly_sales,quarterly_sales,total_orders_per_website,aov_per_city,average_sales_per_weather):
    #making db connection
    conn = psycopg2.connect( 
    database="retail_info", user='postgres', password='postgres', host='postgres', port='5432'
    )
    #calling insertion function with having connection as argument and dataframes and the actual name of tables that are created in DB
    insert_data(conn, sales_data, 'retail_info.sales_data')
    insert_data(conn, user_df, 'retail_info.user_data')
    insert_data(conn, user_weather_df, 'retail_info.weather_data')
    insert_data(conn, average_order_quantity_per_product, 'retail_info.products_avg_sales_quantity')
    insert_data(conn, top_selling_customers, 'retail_info.top_selling_customers')
    insert_data(conn, top_selling_products, 'retail_info.top_selling_products')
    insert_data(conn, aov_per_city, 'retail_info.avg_sales_per_city')
    insert_data(conn, total_orders_per_website, 'retail_info.sales_per_website')
    insert_data(conn, monthly_sales, 'retail_info.monthly_sales')
    insert_data(conn, quarterly_sales, 'retail_info.quarterly_sales')       
    insert_data(conn, average_sales_per_weather, 'retail_info.sales_in_weather') 

if __name__ == "__main__":
    user_df,sales_data,user_weather_df,total_sales_per_customer ,average_order_quantity_per_product,top_selling_customers,top_selling_products,monthly_sales,quarterly_sales,total_orders_per_website,aov_per_city,average_sales_per_weather = manip_aggreg()
    #aligning dataframe column names as table columns - to get rid of column not found errors:
    user_df.rename(columns = {'address.street':'street_address','address.suite':'suite_address','address.city':'city_address','address.zipcode':'zipcode_address','address.geo.lat':'geo_lat_address','address.geo.lng':'geo_lng_address','company.name':'company_name','company.catchPhrase':'company_catchPhrase','company.bs':'company_bs'}, inplace = True)
    average_order_quantity_per_product.rename(columns = {'quantity':'avg_sales_quantity'}, inplace = True)
    aov_per_city.rename(columns = {'average_order_value':'avg_sales_value'}, inplace = True)
    total_orders_per_website.rename(columns = {'total_orders':'total_sales'}, inplace = True)
    #changing datatypes of needed to align it with DB tables column datatype
    monthly_sales['year_month'] = monthly_sales['year_month'].astype(str)
    quarterly_sales['year_quarter'] = quarterly_sales['year_quarter'].astype(str)
    loading(user_df,sales_data,user_weather_df,total_sales_per_customer ,average_order_quantity_per_product,top_selling_customers,top_selling_products,monthly_sales,quarterly_sales,total_orders_per_website,aov_per_city,average_sales_per_weather)
