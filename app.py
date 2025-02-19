"""Not a real module. Provides for a Streamlit-app"""
import json
import os
import io

# from PIL import Image
import qrcode.image.svg
import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import numpy as np

# # qrcode aliases
import qrcode
import qrcode.constants
from qrcode.image.pure import PyPNGImage
# import segno


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
    ), axis=1)  # bygger fortfarande en lista...

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
    meta=['_id', 'ProductName', 'UnitsInStock',
          'UnitsOnOrder', 'ReorderLevel'],
    record_path=['SupplierDescription'])

# calculating the least amount to order
least_order_amount = \
    json_normalised['ReorderLevel'] \
    - json_normalised['UnitsOnOrder'] \
    + json_normalised['UnitsInStock']

least_order_amount.name = "least_order_amount"

# create the final df
df_orderneeds = \
    pd.DataFrame(json_normalised,
                 columns=[
                     '_id',
                     'ProductName',
                     'ContactName',
                     'Phone',
                 ])
# append order_amount
df_orderneeds = df_orderneeds.join(least_order_amount)

swedish_column_names = {
    '_id': 'Artikelnummer',
    'ProductName': 'Produkt',
    'ContactName': 'Kontaktperson',
    'Phone': 'Telefonnummer',
    'least_order_amount': 'Saknad mängd'
}

st.dataframe(df_orderneeds,
             hide_index=True,
             column_config=swedish_column_names,
             use_container_width=True,
)

product, contact_name, qr_code_list = st.columns([3, 3, 3])

with product:
    st.subheader('Produkt')
with contact_name:
    st.subheader('Kontaktperson')
with qr_code_list:
    st.subheader('Telefonnummer')
# QR - code
qr = qrcode.QRCode(
    version=None,
)

for _, j in df_orderneeds.iterrows():
    # create the new row
    product, contact_name, qr_code_list = st.columns([3, 3, 3])
    product.write(j.ProductName)
    contact_name.write(j.ContactName)

    qr.add_data(f"tel: {j.Phone}")
    qr.make(fit=True)
    phone_qr = qr.make_image(fill_color="white", back_color="black")
    
    phone_qr_as_np = np.array(phone_qr)
    qr_code_list.image(phone_qr_as_np)