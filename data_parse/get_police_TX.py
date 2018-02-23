# -*- coding: utf-8 -*-
"""
Gather Police Stations Data
"""
from helpers import helpers
import config as cfg

from time import sleep
import pyodbc
import urllib3
import lxml.html as lh
from lxml.cssselect import CSSSelector
from re import sub

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url_root = 'https://www.policeone.com'
http = urllib3.PoolManager()

def parse_single(str_value, ps_info):
    sel = CSSSelector('div.dep-block-info p')
    root = lh.fromstring(str_value)
    
    for ele in sel(root):
        content = ele.text_content().strip()
        split = content.split(':')
        if(len(split) >= 2):
            ps_info[split[0].strip()] = split[1].strip()
        
    #print (ps_info) #DEBUG
    return ps_info

def parse_list(str_value, ps_list):
    sel = CSSSelector('div#search-results td.left a')
    root = lh.fromstring(str_value)
    
    for ele in sel(root):
        print (ele.get('href'))
        ps_info = {}
        ps_info['url'] = ele.get('href').strip()
        ps_info['name'] = ele.text_content().strip()
        
        #Call single dept
        r = http.request('GET', url_root + ps_info['url'])
        
        if(r.status == 200):
            ps_list.append(parse_single(r.data, ps_info))
        else:
            print ('ERROR: ', r.status)

        sleep(0.25)
        
    #print (ps_list) #DEBUG
    return ps_list
            
def save_db(ps_list):
    #SAVE ps_list into DB
    cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                          + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
    cursor = cnxn.cursor()
    
    query = """
        INSERT INTO [PoliceStation]
               (
               [URL]
               ,[Name]
               ,[Address1]
               ,[Address2]
               ,[City]
               ,[State]
               ,[Zip]
               ,[Population]
               ,[Officers]
               )
         VALUES
               ( ?, ?, ?, ?, ?, ?, ?, ?, ? )
        """
    
    for item in ps_list:
        #check URL exists already or not
        row = cursor.execute("select COUNT(StationID) as count from PoliceStation WHERE URL = ?", item['url']).fetchone()
        if row and (row.count > 0):
            continue
        
        #save into db if not exists
        pop_served = int(sub(r'[^\d.]', '', item.get('Population Served') )) if item.get('Population Served') else 0
        num_officers = int(sub(r'[^\d.]', '', item.get('Number of Officers') )) if item.get('Number of Officers') else 0

        params = [item.get('url'), item.get('name'), item.get('Address 1'), item.get('Address 2'), 
                  item.get('City'), item.get('State'), item.get('Zip Code'), pop_served, num_officers ]
        cursor.execute(query, params)
        cnxn.commit()
        

#START Parsing list
ps_list = []

url='https://www.policeone.com/law-enforcement-directory/Texas-Agencies/Police-Departments/'
print(url)
r = http.request('GET', url)
if(r.status == 200):
    parse_list(r.data, ps_list)
else:
    print ('ERROR: ', r.status)

# Save
save_db(ps_list)

# Get pages 2 - ##
#url='https://www.policeone.com/law-enforcement-directory/Texas-Agencies/Police-Departments/page-2/'
page_start = 2
page_end = 27
for i in range(page_start, page_end+1):
    ps_list = []

    url='https://www.policeone.com/law-enforcement-directory/Texas-Agencies/Police-Departments/page-' + str(i) + '/'
    print(url)
    r = http.request('GET', url)
    if(r.status == 200):
        parse_list(r.data, ps_list)
    else:
        print ('ERROR: ', r.status)
    
    # Save
    save_db(ps_list)
    
    sleep(1)
