# -*- coding: utf-8 -*-

import config as cfg
import pyodbc

"""
Fill in closest Police Stations within 10 miles

Latitude/Longitude distance coefficients:
--Miles 3958.75
--Kilometers 6367.45 
--Feet 20890584 
--Meters 6367450 
"""
def calculate_distance(bankID, lat, lng):
    query = """
        DECLARE @latitude float, @longitude float
        SELECT @latitude = ?, @longitude = ?
        
        SELECT 
        	[StationID]
        	,[Name]
        	, [Address1]
        	, [City]
        	, [State]
            , Distance
            FROM
            (
            SELECT
        	[StationID]
        	,[Name]
        	, [Address1]
        	, [City]
        	, [State]
            , ( 3959 * acos( cos( radians(@latitude) ) * cos( radians( Lat ) ) * cos( radians( Lng )
            - radians(@longitude) ) + sin( radians(@latitude) ) * sin( radians( Lat ) ) ) ) AS Distance 
        	FROM PoliceStation
        ) as x   
        WHERE Distance <= 10   
        ORDER BY Distance;
    """
    
    cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                          + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
    cursor = cnxn.cursor()
    
    params = [lat, lng]
    rows = cursor.execute(query, params)
    
    #Calculate
    psCount = 0
    totdist = 0
    closestStationID = None
    for row in rows:
        totdist = totdist + float(row.Distance)
        if(psCount == 0):
            print(bankID, row.StationID, row.Name, row.City, row.Distance)
            closestStationID = row.StationID
            closestPSDistance = float(row.Distance)
        psCount = psCount + 1
        
    meanPSDistance = totdist / psCount if psCount else None
    
    # Save back into table
    query2 = """
        UPDATE Bank
        SET 
        ClosestStationID = ?
        , ClosestPSDistance = ?
        , MeanPSDistance = ?
        , PSCount = ?
        WHERE BankID = ?
        ;
    """
    
    if not closestStationID: #no closest station in 10 miles
        closestStationID = None
        closestPSDistance = None
        meanPSDistance = None
        psCount = 0
        
    params2 = [closestStationID, closestPSDistance, meanPSDistance, psCount, bankID] 
    cursor.execute(query2, params2)
    cnxn.commit()
    
    
#----------------------------------------------
# Calculate distance for all rows
cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
cursor = cnxn.cursor()

query = "SELECT bankID, lat, lng FROM Bank;"
rows = cursor.execute(query)

for row in rows:
    calculate_distance(row.bankID, row.lat, row.lng)
    

