# -*- coding: utf-8 -*-
"""
P(Caught by Distance) 
y = 70 - 10x
y% = 0.7 - (x/10)
    x = time to get to bank from station (assuming 60mph 1mile/1min)
    y = P(caught by distance)
    
Assume: 60mph
"""
import config as cfg
import pyodbc

mileMinute = 1 #60 mph

def fill_pdistance(bankID, closestDistance):
    print(row.BankID)

    if (not closestDistance):
        pDistance = 0
    else:
        pDistance = 0.7 - (float(closestDistance * mileMinute) / 10.0)
    
    if(pDistance < 0):
        pDistance = 0
        
    cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
    cursor = cnxn.cursor()
    # Save back into table
    query = """
        UPDATE Bank
        SET 
        [PDistance] = ?
        WHERE [BankID] = ?
        ;
    """

    params = [pDistance, row.BankID] 
    cursor.execute(query, params)
    cnxn.commit()


#-------------------------------------------------
# All rows
cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
cursor = cnxn.cursor()

query = "SELECT BankID, ClosestPSDistance FROM Bank WHERE [PDistance] IS NULL;"
rows = cursor.execute(query)

for row in rows:
    fill_pdistance(row.BankID, row.ClosestPSDistance)