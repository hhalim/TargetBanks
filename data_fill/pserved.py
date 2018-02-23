# -*- coding: utf-8 -*-
"""
P(Caught by PopulationServed)
y = (Police/PopServed) * 1000 * 5%
Number of police/pop served per 1000, higher means higher risk P(police/Population Served)
Number of police within 10 miles near bank, higher means higher risk P(Count)

"""
import config as cfg
import pyodbc

def fill_pserved(bankID, lat, lng):
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
        WHERE Distance <= 10   
        ORDER BY Distance;
    """

    cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
    cursor = cnxn.cursor()

    params = [lat, lng]
    rows = cursor.execute(query, params)
    
    totPopulation = 0
    totOfficers = 0
    for row in rows:
        totPopulation = totPopulation + float(row.Population if row.Population else 0)
        totOfficers = totOfficers + float(row.Officers if row.Officers else 0)

    if(totPopulation == 0):
        totPopulation = 1
    pServed = totOfficers/totPopulation * 1000.0 * 0.05

    print(bankID, totOfficers, totPopulation, pServed)
    
    # Save back into table
    query2 = """
        UPDATE Bank
        SET 
        [PServed] = ?
        WHERE [BankID] = ?
        ;
    """

    params2 = [pServed, bankID] 
    cursor.execute(query2, params2)
    cnxn.commit()

#-------------------------------------------------
# All rows
cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
cursor = cnxn.cursor()

query = "SELECT BankID, lat, lng FROM Bank;"
rows = cursor.execute(query)

for row in rows:
    fill_pserved(row.BankID, row.lat, row.lng)
