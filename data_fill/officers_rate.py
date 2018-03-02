# -*- coding: utf-8 -*-
"""
Officers1000
y = (Police/PopServed) * 1000
Number of police/pop served per 1000, higher means higher risk 
Police # is within 5 miles of the bank
Population is by city
"""
import config as cfg
import pyodbc

def fill_officersRate(bankID, lat, lng):
    query = """
        DECLARE @latitude float, @longitude float
        SELECT @latitude = ?, @longitude = ?
        
        SELECT 
            [StationID]
            , [Name]
            , [Address1]
            , [City]
            , [State]
            , [Officers]
            , [Population]
            , Distance
        FROM
            (
            SELECT
                [StationID]
                , [Name]
                , [Address1]
                , [City]
                , [State]
                , [Officers]
                , [Population]
                , ( 3959 * acos( cos( radians(@latitude) ) * cos( radians( Lat ) ) * cos( radians( Lng )
            - radians(@longitude) ) + sin( radians(@latitude) ) * sin( radians( Lat ) ) ) ) AS Distance 
            	FROM PoliceStation
            ) as x   
        WHERE Distance <= 5   
        ORDER BY Distance;
    """

    cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
    cursor = cnxn.cursor()

    params = [lat, lng]
    rows = cursor.execute(query, params)
    
    totOfficers = 0
    totPopulation = 0
    for row in rows:
        totPopulation = totPopulation + float(row.Population if row.Population else 0)
        totOfficers = totOfficers + float(row.Officers if row.Officers else 0)

    totPopulation = totPopulation if totPopulation else 1; #avoid divide by zero
    
    officersRate = 0
    if(totOfficers <= totPopulation):
        officersRate = (totOfficers/totPopulation) * 1000.0

    print(bankID, totOfficers, totPopulation, officersRate)
    
    # Save back into table
    query2 = """
        UPDATE Bank
        SET 
        [Officers1000] = ?
        WHERE [BankID] = ?
        ;
    """

    params2 = [officersRate, bankID] 
    cursor.execute(query2, params2)
    cnxn.commit()

#-------------------------------------------------
# All rows
cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
cursor = cnxn.cursor()

query = "SELECT BankID, Lat, Lng FROM Bank;"
rows = cursor.execute(query)

for row in rows:
    fill_officersRate(row.BankID, row.Lat, row.Lng)
