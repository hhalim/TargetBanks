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
cursor.execute('SELECT [StationID], [address1], [city], [state], [zip], [lat], [lng] FROM PoliceStation;')

geoloc = geocoders.GoogleV3(api_key=cfg.google_geocode_api)

count = 0
for row in cursor.fetchall():
    if( not(row.lat is None or row.lng is None) ):
        continue
    
    addr = ' '.join([ str(row.address1), str(row.city), str(row.state), str(row.zip) ])
    loc = geoloc.geocode(addr, timeout=10)
    #print(loc.raw) #Debug

    if(loc is None):
        continue

    print(loc.address, 'lat:',loc.latitude, 'lng:', loc.longitude)

    upd_qry = "UPDATE [PoliceStation] SET [Lat] = ?, [Lng] = ? WHERE [StationID] = ? ;"
    cursor.execute(upd_qry, [loc.latitude, loc.longitude, row.StationID])

    count += 1
    if(count >= 5):
        count = 0
        cnxn.commit()

    sleep(0.50)
        
cnxn.commit() #commit anyway if count doesn't reach 5
cnxn.close();