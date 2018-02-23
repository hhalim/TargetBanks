# -*- coding: utf-8 -*-
"""
0.05% of Deposit
Take/Reward = 0.0005 * Deposit 

P(Success) = 1 - P(Caught) 
P(Caught) = P(Caught by Distance) + P(Caught by PopulationServed) 

P(Caught by Distance) 
y = 100 - 10x
y% = 1 - (x/10)
    x = time to get to bank from station (assuming 60mph 1mile/1min)
    y = P(caught)

P(Caught by PopulationServed)
y = (Police/PopServed) * 1000 * 10%
Number of police/pop served per 1000, higher means higher risk P(police/Population Served)
Number of police within 10 miles near bank, higher means higher risk P(Count)

"""

import config as cfg
import pyodbc

def fill_psuccess(bankID, pDistance, pServed):
    pSuccess = 1.0 - (pDistance + pServed)
    if(pSuccess < 0):
        pSuccess = 0

    print (bankID, pDistance, pServed, pSuccess)
        
    query = """
        UPDATE Bank
        SET 
        [PSuccess] = ?
        WHERE [BankID] = ?
        ;
    """

    cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
    cursor = cnxn.cursor()

    params = [pSuccess, bankID] 
    cursor.execute(query, params)
    cnxn.commit()

#-------------------------------------------------
# All rows
cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
cursor = cnxn.cursor()

query = "SELECT BankID, PDistance, PServed FROM Bank;"
rows = cursor.execute(query)

for row in rows:
    fill_psuccess(row.BankID, row.PDistance, row.PServed)