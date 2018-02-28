# -*- coding: utf-8 -*-
"""
Lat and longitude finder

https://stackoverflow.com/questions/7167604/how-accurately-should-i-store-latitude-and-longitude
decimal  degrees    distance
places
-------------------------------  
0        1.0        111 km
1        0.1        11.1 km
2        0.01       1.11 km
3        0.001      111 m
4        0.0001     11.1 m
5        0.00001    1.11 m
6        0.000001   0.111 m
7        0.0000001  1.11 cm
8        0.00000001 1.11 mm
"""

from helpers import helpers
import config as cfg

from time import sleep
import pyodbc
from geopy import geocoders

cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
cursor = cnxn.cursor()
cursor.execute('SELECT [FFLID], [address], [city], [state], [zip], [lat], [lng] FROM FFL;')

geoloc = geocoders.GoogleV3(api_key=cfg.google_geocode_api)

count = 0
for row in cursor.fetchall():
    if( not(row.lat is None or row.lng is None) ):
        continue
    
    addr = ' '.join([ str(row.address), str(row.city), str(row.state), str(row.zip) ])
    loc = geoloc.geocode(addr, timeout=10)
    #print(loc.raw) #Debug

    if(loc is None):
        continue

    print(loc.address, 'lat:', round(loc.latitude, 4), 'lng:', round(loc.longitude, 4))

    upd_qry = "UPDATE [FFL] SET [Lat] = ?, [Lng] = ? WHERE [FFLID] = ? ;"
    cursor.execute(upd_qry, [round(loc.latitude, 4), round(loc.longitude, 4), row.FFLID])

    count += 1
    if(count >= 5):
        count = 0
        cnxn.commit()

    sleep(0.25)
        
cnxn.commit() #commit anyway if count doesn't reach 5
cnxn.close();