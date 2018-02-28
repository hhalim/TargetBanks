# -*- coding: utf-8 -*-
"""
Number of FFL within 5 miles near bank, higher means higher risk of armed civilians
"""
import config as cfg
import pyodbc

def fill_ffl_count(bankID, lat, lng):
    query = """
        DECLARE @latitude float, @longitude float
        SELECT @latitude = ?, @longitude = ?
        
        SELECT 
            [FFLID]
            , [Name]
            , [Address]
            , [City]
            , [State]
            , Distance
        FROM
            (
            SELECT
                [FFLID]
                , [Name]
                , [Address]
                , [City]
                , [State]
                , ( 3959 * acos( cos( radians(@latitude) ) * cos( radians( Lat ) ) * cos( radians( Lng )
            - radians(@longitude) ) + sin( radians(@latitude) ) * sin( radians( Lat ) ) ) ) AS Distance 
            	FROM FFL
            ) as x   
        WHERE Distance <= 5   
        ORDER BY Distance;
    """

    cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
    cursor = cnxn.cursor()

    params = [lat, lng]
    rows = cursor.execute(query, params)
    
    totFFL = 0
    for row in rows:
        totFFL = totFFL + (1 if row.FFLID else 0)

    print(bankID, totFFL)
    
    # Save back into table
    query2 = """
        UPDATE Bank
        SET 
        [FFLCount] = ?
        WHERE [BankID] = ?
        ;
    """

    params2 = [totFFL, bankID] 
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
    fill_ffl_count(row.BankID, row.lat, row.lng)
