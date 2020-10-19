import pandas as pd
import random as rand
import numpy as np
import json
import os
import requests
from pathlib import Path

from pip._vendor import msgpack

# Read columns specified in csv files and then turn data into dataframe
def read_data(file, list):
    data = pd.read_csv(file, usecols=col_list)
    return data

# Create 4 digit random number for the length of rows in the df and then cast to string
# Then populate new CprNumber column with values from DateofBirth, replace the symbol 
# with no space and then add new symbol followed by the random numbers generated
def create_cpr(df, symbol):
    number = np.random.randint(1111, 9999, size=len(df)).astype(str)
    df['CprNumber'] = df.pop('DateOfBirth').str.replace('-', '') + symbol + number
    return df

# Create xml with data from df
def create_xml(df):
    shema = 'Person'
    version = "1.1"
    xml = [f'<?xml version="{version}" encoding="UTF-8"?>']
    xml.append("<{}>".format(shema))
    for data in df.index:
        xml.append(f'  <field name="{data}">{df[data]}</field>')
    xml.append(f"</{shema}>")
    return xml

if __name__ == "__main__":
    # col_list = ['FirstName', 'LastName', 'DateOfBirth', 'Email']
    col_list = ['FirstName', 'LastName', 'DateOfBirth', 'Email', 'Phone', 'Address', 'Country']
    symbol = ('-') 
    file = 'people.csv'
    path = Path(os.path.dirname(__file__))/f"{file}" 

    ESB_SERVICE_ADDRESS = 'http://127.0.0.1:8080'
    ESB_SERVICE_ENDPOINT = 'nemID'

    df = create_cpr(read_data(f'{path}', col_list), symbol)
    person = df.apply(create_xml, axis=1)

    headers = {'Content-Type': 'text/xml', 'Accept':'application/xml'}
    
    response = requests.post(f"{ESB_SERVICE_ADDRESS}/{ESB_SERVICE_ENDPOINT}", data=person, headers=headers).text
    person.nemID = json.loads(response.content)["nemID"]

    print(person.nemID)

    with open(f'{dir}/{person}.msgpack', "wb") as outfile:
          packed = msgpack.packb(person.__dict__)
          outfile.write(packed)

    print(response)