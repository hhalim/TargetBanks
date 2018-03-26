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
        # Police Response 
        # Mean of officers/1000 is 2
        # Equation: y = -10 + 40x
        # Percent: y% = -0.1 + 0.4x
        pPoliceResp = -0.1 + (0.4 * officersRate)
        if pPoliceResp > 1:
            pPoliceResp = 1 #always 100% response rate if over 1
            
        # if high crime rate, then pPoliceResp is lower by 50% when it doubles of avg
        query = "SELECT AVG(Total1000) as avg FROM CrimeRate WHERE [State] = ?;"
        res = cursor.execute(query, state).fetchone()
        avgCrimeRate = res.avg if res.avg else 0
        if(crimeRate and crimeRate >= avgCrimeRate):
            cfCrime = ((crimeRate/avgCrimeRate) - 1) * 0.5 #double the crime rate, then 50% reduction in pPoliceResp
            pPoliceResp = pPoliceResp * (1 - cfCrime)
        if pPoliceResp < 0:
            pPoliceResp = 0
            
        # Armed Response from citizen 
        # fflCount within 5 miles of the bank indicates probability of well armed citizen
        # AVG FFLCount 18: 26 in TX and 7 in NY, need entire USA data for better accuracy
        # y = -0.4444 + 2.06x
        # y% = -0.004444 + 0.0206x
        pArmed = -0.004444 + 0.0206 * fflCount
        if pArmed > 1:
            pArmed = 1 
    
        #Factor of success: pDistance and pPoliceResp is 75%, pArmed is 25% factor
        # pDistance weight is 80% and pPoliceResp is 20% => must still equal to 1 when added
        # pSuccess max: 1 and min: 0
        pSuccess = 1 - (pDistance*0.8 + pPoliceResp*0.20)*0.75  - (pArmed*0.25)
        
        if take >= 5000.0 and 1 >= pSuccess and pSuccess >= 0.9 :
            target = 1
        elif take >= 15000.0 and 0.9 > pSuccess and pSuccess >= 0.8 :
            target = 2
        elif take >= 25000.0 and 0.8 > pSuccess and pSuccess >= 0.7 :
            target = 3
        elif take >= 35000.0 and 0.7 > pSuccess and pSuccess >= 0.6 :
            target = 4
        elif take >= 45000.0 and 0.6 > pSuccess and pSuccess >= 0.5 :
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

query = "SELECT BankID, [State], [Take], PDistance, [Officers1000], FFLCount, [Population], CrimeRate1000 FROM BankSampleView;"
rows = cursor.execute(query)

for row in rows:
    target_select(row.BankID, row.State, row.Take, row.PDistance, row.Officers1000, row.FFLCount, row.Population, row.CrimeRate1000)
