import pandas as pd
import random as rand
import numpy as np
import json
import requests
from pathlib import Path

from pip._vendor import msgpack

def read_data(file, list):
    data = pd.read_csv(file, usecols=col_list)
    return data

def create_cpr(df, symbol):
    number = np.random.randint(1111, 9999, size=len(df)).astype(str)
    df['CprNumber'] = df['DateOfBirth'].str.replace('-', '') + symbol + number
    return df

def create_xml(df):
    shema = 'Person'
    version = "1.1"
    xml = [f'<?xml version="{version}" encoding="UTF-8"?>']
    xml.append("<{}>".format(shema))
    for data in df.index:
        xml.append(f'  <field name="{data}">{df[data]}</field>')
    xml.append(f"</{shema}>")
    return '\n'.join(xml)

if __name__ == "__main__":
    # col_list = ['FirstName', 'LastName', 'DateOfBirth', 'Email']
    col_list = ['FirstName', 'LastName', 'DateOfBirth', 'Email', 'Phone', 'Address', 'Country']
    symbol = ('-') 
    file = 'people.csv'
    path = Path.cwd().joinpath(f'{file}')

    base_url = 'http://127.0.0.1:8080'

    df = create_cpr(read_data(f'{path}', col_list), symbol)
    person = '\n'.join(df.apply(create_xml, axis=1))

    response = requests.get(base_url)

    headers = {'Content-Type': 'application/xml'}
    response = requests.post(f"{base_url}/nemId", data=person, headers=headers).text

    person = json.loads(response.content)

    with open(f'{path}/msgpack_files/{person}.msgpack', "wb") as outfile:
         packed = msgpack.packb(person.__dict__)
         outfile.write(packed)

    print(response)