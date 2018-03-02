# -*- coding: utf-8 -*-
"""
Take = 0.05% * Deposit
"""

import config as cfg
import pyodbc

cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
cursor = cnxn.cursor()

query = "SELECT BankID, Deposit FROM Bank WHERE Take IS NULL;"
rows = cursor.execute(query)

cnxn2 = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
cursor2 = cnxn2.cursor()
for row in rows:
    print(row.BankID, row.Deposit)
    
    query2 = """
        UPDATE Bank
        SET 
        [Take] = ?
        WHERE [BankID] = ?
        ;
    """

    deposit = float(row.Deposit) if row.Deposit else 0
    take = 0.0005 * deposit
    
    params2 = [take, row.BankID] 
    cursor2.execute(query2, params2)
    cursor2.commit()
