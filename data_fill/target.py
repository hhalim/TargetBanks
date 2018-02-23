"""
Select target class based on Reward and P(Success)
Target class: 
1 Take >= 10000 and 100% >= P(success) >= 90%
2 Take >= 20000 and 90% > P(success) >= 80%
3 Take >= 30000 and 80% > P(success) >= 70%
4 Take >= 40000 and 70% > P(success) >= 60%
5 Take >= 50000 and 60% > P(success) >= 50%

"""
import config as cfg
import pyodbc

def target_select(bankID, take, pSuccess):
    target = 0
    if take >= 10000.0 and 1 >= pSuccess and pSuccess >= 0.9 :
        target = 1
    elif take >= 20000.0 and 0.9 > pSuccess and pSuccess >= 0.8 :
        target = 2
    elif take >= 30000.0 and 0.8 > pSuccess and pSuccess >= 0.7 :
        target = 3
    elif take >= 40000.0 and 0.7 > pSuccess and pSuccess >= 0.6 :
        target = 4
    elif take >= 50000.0 and 0.6 > pSuccess and pSuccess >= 0.5 :
        target = 5
    else : 
        target = 0

    query = """
        UPDATE BankSample
        SET 
        [Target] = ?
        WHERE [BankID] = ?
        ;
    """

    cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
    cursor = cnxn.cursor()

    params = [target, bankID] 
    cursor.execute(query, params)
    cnxn.commit()

#-------------------------------------------------
# All rows

cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
cursor = cnxn.cursor()

query = "SELECT BankID, [Take], [PSuccess] FROM BankSample;"
rows = cursor.execute(query)

for row in rows:
    target_select(row.BankID, row.Take, row.PSuccess)
