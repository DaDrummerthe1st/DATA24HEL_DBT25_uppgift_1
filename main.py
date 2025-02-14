import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
import pandas as pd
import qrcode

st.header("Att beställa")

# Read files and insert into a dataframe
pd_products = pd.read_csv('data/northwind/products.csv')
pd_suppliers = pd.read_json('data/northwind/suppliers.json')

# create dataframes
df_products = pd.DataFrame(pd_products)
df_suppliers = pd.DataFrame(pd_suppliers)


# För att förklara slicing som sökmetod
df_suppliers[df_suppliers["SupplierID"] == 1]

# Add supplier detail on each document (row)
df_products['SupplierDescription'] = \
    df_products.apply(lambda row: json.loads(
        # df_suppliers.query(f"SupplierID == {row.SupplierID}") # alternative method for searching
    df_suppliers[df_suppliers['SupplierID'] == row.SupplierID]
        .to_json(orient='records')
    ), axis=1) # bygger fortfarande en lista...

# transpose df to JSON
products_data = json.loads(df_products.to_json(orient='records'))

# connect to MongoDB-database
with open('pwd_mongo.txt') as f:
    pwd_mongo = f.read().strip()

uri = f'mongodb+srv://cpu_access:{pwd_mongo}@cluster0.ec2ax.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
# creating connection peripherials
database = client["Northwind"]
collection = database["Products"]

# insert into database (first deleting the existing content)
collection.delete_many({})
collection.insert_many(products_data)

# fetching documents with ReorderLevel > (UnitsInStock + UnitsOnOrder)
query = [
    {
        '$match': {
            '$expr': {
                '$lt': [
                    {
                        '$add': [
                            '$UnitsInStock', '$UnitsOnOrder'
                        ]
                    }, '$ReorderLevel'
                ],
                
            }
        }
    }
]
results = collection.aggregate(query)

json_normalised = pd.json_normalize(
    results,
    meta=['_id','ProductName'],
    record_path=['SupplierDescription'])

df_orderneeds = \
    pd.DataFrame(json_normalised,
                 columns=[
                    '_id',
                    'ProductName',
                    'ContactName',
                    'Phone'
                 ])

st.dataframe(df_orderneeds)

qr_field, product = st.columns(2)

for product in df_orderneeds.items():
    with qr_field:
        qrcode.make(product['Phone'])
    with product:
        st.write(product['ProductName'])


# creating a table
# product, qr = st.columns(2)

# with product:
#     st.subheader('Produkt')

# with qr:
#     st.write('Scanna eller klicka på qr-koden')
# check out the resulting documents (should be 6)
# for result in results:
    # with product:
    #     st.write(result['ProductName'])
    
    # with qr:
    #     st.write('hej')
    # for data in json.loads(result):
    #     st.write(data)

# for i in range(0,10):

#     st.snow()
