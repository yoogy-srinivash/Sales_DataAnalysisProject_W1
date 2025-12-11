import pandas as pd
import numpy as np

#Load
cust = pd.read_csv("CUST.csv")
sales = pd.read_csv("SALES.csv")

#Normalize column names
cust.columns = cust.columns.str.strip().str.lower()
sales.columns = sales.columns.str.strip().str.lower()

#Clean
cust.drop_duplicates(inplace=True)
sales.drop_duplicates(inplace=True)

cust.fillna({'description': 'Unknown'}, inplace=True)
sales.fillna({'description': 'Unknown'}, inplace=True)

sales['invoicedate'] = pd.to_datetime(sales['invoicedate'], errors='coerce')

sales['amount'] = np.multiply(sales['quantity'], sales['unitprice'])

#Merge
merged = pd.merge(sales, cust, on='customerid', how='inner')

#Key Metrics
customer_count = cust['customerid'].nunique()
revenue_per_country = merged.groupby('country')['amount'].sum().sort_values(ascending=False)
orders_per_customer = merged.groupby('customerid')['invoiceno'].nunique()

#Results
print("DATA SUMMARY\n")
print(f"Total unique customers: {customer_count}")
print("\nRevenue per Country (Top 5):\n", revenue_per_country.head())
print("\nOrders per Customer (Sample):\n", orders_per_customer.head())
print("\nSample of Cleaned + Merged Data:\n", merged.head())