# -*- coding: utf-8 -*-
# Parse FDIC data

from helpers import helpers
import config as cfg

import pyodbc
import lxml.html as lh
from re import sub

def parse_FDIC(filename):
    file = open(filename).read()
    root = lh.fromstring(file)
    
    banks = []
    office = {}
    for ele in root.getiterator():
        if ele.tag == "td" and ele.get('headers') == 'hdr_inst_name' and not helpers.is_empty(ele.text_content()):
            print (ele.text_content())
            inst_name = ele.text_content().strip()
        if ele.tag == "td" and ele.get('headers') == 'hdr_address' and not helpers.is_empty(ele.text_content()): #new branch found!
            if bool(office):
                banks.append(office) #stuff into array
                office = {} #re init
            addr_ele = ele.find('font') #sub element
            office['name'] = inst_name
            office['address'] = addr_ele.text_content().strip()
        if ele.tag == "td" and ele.get('headers') == 'hdr_city' and not helpers.is_empty(ele.text_content()):
            office['city'] = ele.text_content().strip()
        if ele.tag == "td" and ele.get('headers') == 'hdr_zip' and not helpers.is_empty(ele.text_content()):
            office['zip'] = ele.text_content().strip()
        if ele.tag == "td" and ele.get('headers') == 'hdr_deposit' and not helpers.is_empty(ele.text_content()):
            office['deposit'] = float(sub(r'[^\d.]', '', ele.text_content().strip())) * 1000
        if ele.tag == "td" and ele.get('headers') == 'hdr_uninumbr' and not helpers.is_empty(ele.text_content()):
            office['id'] = int(ele.text_content().strip())
    
    #last bank need to append into array too!!!
    if bool(office):
        banks.append(office) #stuff into array
        office = {} #re init

    #print(banks) #DEBUG
    return banks

def insert_db(banks, state):
    # Insert into SQL
    cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                          + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
    cursor = cnxn.cursor()
    
    query = """
        INSERT INTO [Bank]
               (
               [UniqueNum]
               ,[Name]
               ,[Address1]
               ,[Address2]
               ,[City]
               ,[Zip]
               ,[State]
               ,[Deposit]
               )
         VALUES
               ( ?, ?, ?, ?, ?, ?, ?, ? )
        """
    for row in banks:
        params = [row['id'], row['name'], row['address'], '', row['city'], row['zip'], state, row['deposit']]
        cursor.execute(query, params)
        cnxn.commit()
    
def parse_and_insert(filename, state):
    banks = parse_FDIC(filename)
    insert_db(banks, state)
    