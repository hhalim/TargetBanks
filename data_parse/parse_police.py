# -*- coding: utf-8 -*-
"""
Gather Police Stations Data
"""
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

def parse_single(strValue, psInfo):
    sel = CSSSelector('div.dep-block-info p')
    root = lh.fromstring(strValue)
    
    for ele in sel(root):
        content = ele.text_content().strip()
        split = content.split(':')
        if(len(split) >= 2):
            psInfo[split[0].strip()] = split[1].strip()
        
    #print (psInfo) #DEBUG
    return psInfo

def parse_list(strValue, psList):
    sel = CSSSelector('div#search-results td.left a')
    root = lh.fromstring(strValue)
    
    for ele in sel(root):
        print (ele.get('href'))
        psInfo = {}
        psInfo['url'] = ele.get('href').strip()
        psInfo['name'] = ele.text_content().strip()
        
        #Call single dept
        r = http.request('GET', url_root + psInfo['url'])
        
        if(r.status == 200):
            psList.append(parse_single(r.data, psInfo))
        else:
            print ('ERROR: ', r.status)

        sleep(0.25)
        
    #print (psList) #DEBUG
    return psList
            
def save_db(psList):
    #SAVE psList into DB
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
    
    for item in psList:
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
        

def parse_and_insert(url, pageStart, pageEnd):
    print(url)
    
    #START Parsing list
    psList = []
    
    r = http.request('GET', url)
    if(r.status == 200):
        parse_list(r.data, psList)
    else:
        print ('ERROR: ', r.status)
    
    # Save
    save_db(psList)
    
    # Get pages 2 - ##
    for i in range(pageStart, pageEnd+1):
        psList = []
    
        urlPage = url + 'page-' + str(i) + '/'
        print(urlPage)
        
        r = http.request('GET', urlPage)
        if(r.status == 200):
            parse_list(r.data, psList)
        else:
            print ('ERROR: ', r.status)
        
        # Save
        save_db(psList)
        
        sleep(1)
