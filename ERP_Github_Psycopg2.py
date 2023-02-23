import pandas as pd
import random
import string

import sys
sys.path.append('optional if your libraries are centralized')

import psycopg2

import faker
from faker import Faker


# create an empty DataFrame
data_customer = pd.DataFrame(columns=['customerNumber', 'customerName', 'contactLastName', 'contactFirstName',
                             'phone', 'addressLine', 'city', 'state', 'postalCode', 'country',
                             'salesRepEmployeeNumber'])

f = Faker()

num_of_new_rows_customer = 10000

last_customer_number = 0

for i in range(num_of_new_rows_customer):
    new_customer_number = last_customer_number + 1
    random_row = {'customerNumber': new_customer_number, 
                  'customerName': f.company(),
                  'contactLastName': f.last_name() + " " + str(f.last_name()),
                  'contactFirstName': f.first_name(),
                  'phone': '{}-{}-{}'.format(''.join(random.choices(string.digits, k=3)),
                                            ''.join(random.choices(string.digits, k=3)),
                                            ''.join(random.choices(string.digits, k=4))),
                  'addressLine': f.street_name() + " " + str(f.building_number()),
                  'city': f.city(),
                  'state': f.state(),
                  'postalCode': ''.join(random.choices(string.digits, k=5)),
                  'country': "United States of America",
                  'salesRepEmployeeNumber': random.randint(1, 1000)
                 }
    data_customer = data_customer.append(random_row, ignore_index=True)
    last_customer_number = new_customer_number

# save the DataFrame to a CSV file
data_customer.to_csv("the path where you want it to be saved", index=False)

print(data_customer)




# create an empty DataFrame
data_products = pd.DataFrame(columns=['productCode', 'productName', 'productLine', 'productScale', 'productVendor', 'productDescription', 'quantityInStock', 'buyPrice' ,'MSRP'])


num_of_new_rows_products = 10000

last_product_code = 0

product_options = {
'Home Comfort': ['Ultimate Soft Pillow', 'Comfortable Yoga Mat', 'Stylish Bluetooth Headphones', 'Powerful Blender Set', 'Premium Bamboo Cutting Board'],
'Technology': ['Smart LED TV', 'High-Performance Laptop', 'Stylish Sunglasses', 'Multifunctional Fitness Tracker', 'Smart Thermostat'],
'Fashion Accessories': ['Elegant Diamond Watch', 'Premium Leather Wallet', 'Stylish Sneakers', 'Elegant Ballpoint Pen', 'Stylish Handbag'],
'Outdoor Gear': ['Deluxe Reusable Water Bottle', 'Portable Solar Charger', 'Durable Hiking Backpack', 'Durable Snowboard', 'Top-Rated Vacuum Cleaner'],
'Kitchen Appliances': ['Gourmet Coffee Maker', 'Stainless Steel Kitchen Knife Set', 'Energy-Efficient Dishwasher', 'Compact Electric Kettle', 'Durable Hard Drive']
}

for i in range(num_of_new_rows_products):
    new_product_code = last_product_code + 1
    product_line = random.choice(list(product_options.keys()))
    buy_price = round(random.uniform(0, 1000), 2)
    msrp = max(round(random.uniform(0, 1000), 2), buy_price)
    random_row = {'productCode': new_product_code,
                  'productLine': product_line, 
                  'productName': random.choice(product_options[product_line]),
                  'productScale': '{}:{}'.format(''.join(random.choices(string.digits, k=1)),
                                                 ''.join(random.choices(string.digits, k=2))),
                  'productVendor': f.company(),
                  'productDescription': random.choice(['black', 'white', 'grey', 'dark blue', 'red', 'green', 'yellow', 'multi color']),
                  'quantityInStock': round(random.uniform(0, 100), 0),
                  'buyPrice': buy_price,
                  'MSRP': msrp
                 }
    data_products = data_products.append(random_row, ignore_index=True)
    last_product_code = new_product_code

# save the DataFrame to a CSV file
data_products.to_csv("the path where you want it to be saved", index=False)

print(data_products)



data_orderdetails = pd.DataFrame(columns=['orderNumber', 'productCode', 'quantityOrdered', 'priceEach', 'orderLineNumber'])

num_of_new_rows_orderdetails = 10000

product_codes = data_products['productCode'].unique()

last_ordernumber = 0

for i in range(num_of_new_rows_orderdetails):
    new_ordernumber = last_ordernumber + 1
    product_codes = data_products['productCode'].tolist()
    product_code = random.choice(product_codes)
    quantity_ordered = round(random.uniform(1,10),0)
    price_each = round(random.uniform(1,5000), 2)
    order_lineamount = quantity_ordered * price_each
    random_row={'orderNumber': new_ordernumber,
                'productCode': product_code,
                'quantityOrdered': quantity_ordered,
                'priceEach': price_each,
                'orderLineNumber': order_lineamount
                }

    data_orderdetails = data_orderdetails.append(random_row, ignore_index=True)
    last_ordernumber = new_ordernumber

data_orderdetails['orderNumber'] = data_orderdetails['orderNumber'].astype(int)
data_orderdetails['productCode'] = data_orderdetails['productCode'].astype(int)
data_orderdetails['quantityOrdered'] = data_orderdetails['quantityOrdered'].astype(int)

data_orderdetails.to_csv("the path where you want it to be saved", index=False)  
print(data_orderdetails)


data_orders = pd.DataFrame(columns=['orderNumber', 'orderDate', 'requiredDate', 'shippedDate', 'status', 'comments', 'customerNumber'])

num_of_new_rows_orders = 10000

order_numbers = list(data_orderdetails['orderNumber'].unique())
customer_numbers = list(data_customer['customerNumber'].unique())

selected_customer_numbers = random.sample(customer_numbers, num_of_new_rows_orders)
selected_order_numbers = []

for customer_number in selected_customer_numbers:
    order_number = random.choice(order_numbers)
    while order_number in selected_order_numbers:
        order_number = random.choice(order_numbers)
    selected_order_numbers.append(order_number)
    order_date = f.date_between(start_date="-5y", end_date="today")
    required_date = f.date_between(start_date=order_date, end_date="+5y")
    shipped_date = f.date_between(start_date=order_date, end_date=required_date)
    status = random.choice(['shipped', 'pending', 'cancelled'])
    comments = random.choice(['tier1', 'tier2', 'tier3', 'other tier'])
    random_row={'orderNumber': order_number,
                'orderDate': order_date,
                'requiredDate': required_date,
                'shippedDate': shipped_date,
                'status': status,
                'comments': comments,
                'customerNumber': customer_number
                }

    data_orders = data_orders.append(random_row, ignore_index=True)

data_orders.to_csv("the path where you want it to be saved", index=False)  
print(data_orders)


data_payments = pd.DataFrame(columns=['customerNumber', 'paymentDate', 'amount'])

num_of_new_rows_payments = 10000

customer_numbers_payment = data_customer['customerNumber'].unique()
amounts_payment = data_orderdetails['orderLineNumber'].unique()
payment_dates = data_orders['orderDate'].unique()

for i in range (num_of_new_rows_payments):
    customer_numbers_payment = data_customer['customerNumber'].tolist()
    customer_number1 = random.choice(customer_numbers_payment)
    amounts_payment = data_orderdetails['orderLineNumber'].tolist()
    amount_payment = random.choice(amounts_payment)
    payment_dates = data_orders['orderDate'].tolist()
    payment_date = random.choice(payment_dates)
    random_row={'customerNumber': customer_number1,
                'paymentDate': payment_date,
                'amount': amount_payment
                }

    data_payments = data_payments.append(random_row, ignore_index=True)

data_payments.to_csv("the path where you want it to be saved", index=False)  
print(data_payments)




df = pd.read_csv("the path where you saved the csv file")


conn = psycopg2.connect(
    host="your local host",
    port="it has 4 figures, hint hint",
    database="the name of your data base",
    user="the username you assigned",
)

# Create the table "customers_final" with the specified columns
with conn.cursor() as cur:
    cur.execute("DROP TABLE IF EXISTS customers_final")
    cur.execute("""
    CREATE TABLE customers_final (
        customerNumber INTEGER PRIMARY KEY,
        customerName VARCHAR(255),
        contactLastName VARCHAR(255),
        contactFirstName VARCHAR(255),
        phone VARCHAR(255),
        addressLine VARCHAR(255),
        city VARCHAR(255),
        state VARCHAR(255),
        postalCode VARCHAR(255),
        country VARCHAR(255),
        salesRepEmployeeNumber INTEGER
    );
    """)

# Insert the data from the dataframe into the table
for index, row in df.iterrows():
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO customers_final (customerNumber, customerName, contactLastName, contactFirstName, phone, addressLine, city, state, postalCode, country, salesRepEmployeeNumber)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (row["customerNumber"], row["customerName"], row["contactLastName"], row["contactFirstName"], row["phone"], row["addressLine"], row["city"], row["state"], row["postalCode"], row["country"], row["salesRepEmployeeNumber"]))

# Commit the changes and close the connection
conn.commit()
conn.close()



conn = psycopg2.connect(
    host="your local host",
    port="it has 4 figures, hint hint",
    database="the name of your data base",
    user="the username you assigned",
)

# Load the "products_final.csv" file into a pandas dataframe
df1 = pd.read_csv("the path where you saved the csv file")

# Drop the table "products_final" if it already exists
with conn.cursor() as cur:
    cur.execute("DROP TABLE IF EXISTS products_final;")

# Create the table "products_final" with the specified columns
with conn.cursor() as cur:
    cur.execute("""
    CREATE TABLE products_final (
        productCode VARCHAR(255) PRIMARY KEY,
        productLine VARCHAR(255),
        productName VARCHAR(255),
        productScale VARCHAR(255),
        productVendor VARCHAR(255),
        productDescription VARCHAR(255),
        quantityInStock INTEGER,
        buyPrice REAL,
        MSRP REAL
    );
    """)

# Insert the data from the dataframe into the table
for index, row in df1.iterrows():
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO products_final (productCode, productLine, productName, productScale, productVendor, productDescription, quantityInStock, buyPrice, MSRP)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (row["productCode"], row["productLine"], row["productName"], row["productScale"], row["productVendor"], row["productDescription"], row["quantityInStock"], row["buyPrice"], row["MSRP"]))

# Commit the changes and close the connection
conn.commit()
conn.close()

import psycopg2
import pandas as pd

# Connect to the database
conn = psycopg2.connect(
    host="your local host",
    port="it has 4 figures, hint hint",
    database="the name of your data base",
    user="the username you assigned",
)

# Load the data from the csv file into a pandas dataframe
df2 = pd.read_csv("the path where you saved the csv file")

# Drop the table if it already exists
with conn.cursor() as cur:
    cur.execute("DROP TABLE IF EXISTS orderdetails_final;")

# Create the table "orderdetails_final" with the specified columns
with conn.cursor() as cur:
    cur.execute("""
    CREATE TABLE orderdetails_final (
        orderNumber INTEGER,
        productCode VARCHAR(255),
        quantityOrdered INTEGER,
        priceEach FLOAT,
        orderLineNumber INTEGER
    );
    """)

# Insert the data from the dataframe into the table
for index, row in df2.iterrows():
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO orderdetails_final (orderNumber, productCode, quantityOrdered, priceEach, orderLineNumber)
        VALUES (%s, %s, %s, %s, %s);
        """, (row["orderNumber"], row["productCode"], row["quantityOrdered"], row["priceEach"], row["orderLineNumber"]))

# Commit the changes and close the connection
conn.commit()
conn.close()



df3 = pd.read_csv("the path where you saved the csv file")

conn = psycopg2.connect(
    host="your local host",
    port="it has 4 figures, hint hint",
    database="the name of your data base",
    user="the username you assigned",
)

with conn.cursor() as cur:
    cur.execute("DROP TABLE IF EXISTS orders_final;")
    cur.execute("""
    CREATE TABLE orders_final (
        orderNumber INTEGER PRIMARY KEY,
        orderDate DATE,
        requiredDate DATE,
        shippedDate DATE,
        status VARCHAR(255),
        comments VARCHAR(255),
        customerNumber INTEGER
    );
    """)

for index, row in df3.iterrows():
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO orders_final (orderNumber, orderDate, requiredDate, shippedDate, status, comments, customerNumber)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (row["orderNumber"], row["orderDate"], row["requiredDate"], row["shippedDate"], row["status"], row["comments"], row["customerNumber"]))

conn.commit()
conn.close()


df4 = pd.read_csv("the path where you saved the csv file")

conn = psycopg2.connect(
    host="your local host",
    port="it has 4 figures, hint hint",
    database="the name of your data base",
    user="the username you assigned",
)

with conn.cursor() as cur:
    cur.execute("DROP TABLE IF EXISTS payments_final;")
    cur.execute("""
    CREATE TABLE payments_final (
        customerNumber INTEGER,
        paymentDate DATE,
        amount FLOAT
    );
    """)

for index, row in df4.iterrows():
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO payments_final (customerNumber, paymentDate, amount)
        VALUES (%s, %s, %s);
        """, (row["customerNumber"], row["paymentDate"], row["amount"]))

conn.commit()
conn.close()
