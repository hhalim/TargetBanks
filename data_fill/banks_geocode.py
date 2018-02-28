# -*- coding: utf-8 -*-
"""
Lat and longitude finder
"""

from helpers import helpers
import config as cfg

from time import sleep
import pyodbc
from geopy import geocoders

cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
cursor = cnxn.cursor()
cursor.execute('SELECT bankid, address1, address2, city, state, zip, lat, lng FROM Bank;')

geoloc = geocoders.GoogleV3(api_key=cfg.google_geocode_api)

count = 0
for row in cursor.fetchall():
    if( not(row.lat is None or row.lng is None) ):
        continue
    
    addr = ' '.join([row.address1, row.address2, row.city, row.state, row.zip])
    loc = geoloc.geocode(addr, timeout=10)
    #print(loc.raw) #Debug

    if(loc is None):
        continue

    print(loc.address, 'lat:', round(loc.latitude, 4), 'lng:', round(loc.longitude, 4))

    upd_qry = "UPDATE [Bank] SET [Lat] = ?, [Lng] = ? WHERE [BankID] = ? ;"
    cursor.execute(upd_qry, [round(loc.latitude, 4), round(loc.longitude, 4), row.bankid])

    count += 1
    if(count >= 5):
        count = 0
        cnxn.commit()

    sleep(0.25)
        
cnxn.commit() #commit anyway if count doesn't reach 5
cnxn.close();