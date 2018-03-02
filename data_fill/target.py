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

def target_select(bankID, state, take, pDistance, officersRate, fflCount, population, crimeRate):
    cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
    cursor = cnxn.cursor()
    
    target = 0
    if(pDistance == 0 and officersRate == 0 and not population and not crimeRate):
        target = 0
    else:
        # Probability success decrease with higher officers rate per 1000 population
        pServed = officersRate * 0.1
        
        # if high crime rate, then pServed is lower by 50% when it doubles of avg
        query = "SELECT AVG(Total1000) as avg FROM CrimeRate WHERE [State] = ?;"
        res = cursor.execute(query, state).fetchone()
        avgCrimeRate = res.avg if res.avg else 0
        if(crimeRate and crimeRate >= avgCrimeRate):
            cfCrime = ((crimeRate/avgCrimeRate) - 1) * 0.5 #double the crime rate, then 50% reduction in pServed
            pServed = pServed * (1 - cfCrime)
            
        # fflCount within 5 miles of the bank indicates probability of well armed population
        # straight conversion into percentage
        pArmed = (fflCount / 100.0)
    
        #Factor of success: pDistance and pServed is 75%, pArmed is 25% factor
        pSuccess = 1 - (pDistance + pServed)*0.75  - (pArmed*0.25)
        
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

    params = [target, bankID] 
    cursor.execute(query, params)
    cnxn.commit()

    print (bankID, "; target:", target)
#-------------------------------------------------
# All rows

cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
cursor = cnxn.cursor()

query = "SELECT BankID, [State], [Take], PDistance, [Officers1000], FFLCount, [Population], CrimeTotal1000 FROM BankSampleView;"
rows = cursor.execute(query)

for row in rows:
    target_select(row.BankID, row.State, row.Take, row.PDistance, row.Officers1000, row.FFLCount, row.Population, row.CrimeTotal1000)
