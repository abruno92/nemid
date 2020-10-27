import pandas as pd
import random as rand
import numpy as np
import json
import os
import requests
import xml.etree.ElementTree as ET

from pathlib import Path
from pip._vendor import msgpack

from string import Template

symbol = ('-') 
file = 'people.csv'
dir = path = Path(os.path.dirname(__file__))
path = Path(os.path.dirname(__file__))/f"{file}"
headers = {'Content-Type': 'text/xml', 'Accept':'application/xml'}
esb_serivce_address = 'http://127.0.0.1:8080'
esb_serivce_endpoint = 'nemID'


# Read columns specified in csv files and then turn data into dataframe
def read_data(file, list):
    data = pd.read_csv(file, usecols=col_list)
    return data

# Create 4 digit random number for the length of rows in the df and then cast to string
# Then populate new CprNumber column with values from DateofBirth, replace the symbol 
# with no space and then add new symbol followed by the random numbers generated
def create_cpr(df, symbol):
    number = np.random.randint(1111, 9999, size=len(df)).astype(str)
    df['CprNumber'] = df['DateOfBirth'].str.replace('-', '') + symbol + number
    return df

# Create xml with specific elements from df
def create_xml(firstname, lastname, email, cpr):
    person = ET.Element('Person')
    ET.SubElement(person, 'FirstName').text = firstname
    ET.SubElement(person, 'LastName').text = lastname
    ET.SubElement(person, 'Email').text = email
    ET.SubElement(person, 'CprNumber').text = cpr
    return ET.tostring(person)

if __name__ == "__main__":
    col_list = ['FirstName', 'LastName', 'DateOfBirth', 'Email', 'Phone', 'Address', 'Country']

    df = create_cpr(read_data(f'{path}', col_list), symbol)

    for person in df.values.tolist():
        firstname = person[0] 
        lastname = person[1]
        email = person[2] 
        cpr  = person[7]

    person_xml = create_xml(firstname, lastname, email, cpr)
    
    response = requests.post(f"{esb_serivce_address}/{esb_serivce_endpoint}", data=person_xml, headers=headers)
    
    nemID = json.loads(response.text)["nemID"]

    with open(f'{dir}/{cpr}.msgpack', "wb") as outfile:
           packed = msgpack.packb(person)
           outfile.write(packed)
