# -*- coding: utf-8 -*-
import config as cfg
import pyodbc
import urllib
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()

# GET ratings from Google
def get_ratings(bankID, name, lat, lng):
    urlPlaceID = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?' \
    + 'key=' + cfg.google_geocode_api \
    + '&location=' + str(lat) + ',' + str(lng) \
    + '&radius=100&rankby=prominence&keyword=' + urllib.parse.quote(name)

    r = http.request('GET', urlPlaceID)
    if(r.status == 200):
        res = json.loads(r.data)
    else:
        print ('ERROR: ', r.status)

    if not res['results']:
        return
    
    urlDetail = 'https://maps.googleapis.com/maps/api/place/details/json?placeid=' + res['results'][0]['place_id'] + '&key=' + cfg.google_geocode_api
    r = http.request('GET', urlDetail)
    if(r.status == 200):
        res = json.loads(r.data)
    else:
        print ('ERROR: ', r.status)

    print ('BankID:', bankID, '; Name:', res['result']['name'])

    #Fill reviews and ratings
    cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                          + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
    cursor = cnxn.cursor()
    
    #Insert into Review table
    query = """
        INSERT INTO Review ([BankID], [Rating], [Text], [Author_Name], [Author_Url])
        VALUES (?, ?, ?, ?, ?) 
    """
    reviews = res['result'].get('reviews')
    if not reviews:
        return
    
    for rev in reviews:
        rating = rev.get('rating', 0)
        text = rev.get('text')
        author_name = rev.get('author_name')
        author_url = rev.get('author_url')
        
        row = cursor.execute("select COUNT(ReviewID) as count from Review WHERE [BankID] = ? AND [Author_Name] = ?", bankID, author_name).fetchone()
        if row and (row.count > 0):
            continue
        
        print ('author_name:', rev['author_name']) 

        params = [ bankID, rating, text, author_name, author_url ]
        cursor.execute(query, params)
        cursor.commit()

    #Update BANK AvgRating
    query = """
        UPDATE Bank
        SET 
        [AvgRating] = ?
        WHERE BankID = ?
    """
    
    rating = res['result'].get('rating')
    if rating:
        params = [ rating, bankID ]
        cursor.execute(query, params)
        cursor.commit()    
        
#----------------------------------------------
# Get ratings for all rows
cnxn = pyodbc.connect( 'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + cfg.mssql['server'] + ';DATABASE=' 
                      + cfg.mssql['database'] + ';UID=' + cfg.mssql['username'] + ';PWD=' + cfg.mssql['password'] )
cursor = cnxn.cursor()

query = "SELECT BankID, Name, Lat, Lng FROM Bank WHERE AvgRating IS NULL;"
rows = cursor.execute(query)

for row in rows:
    get_ratings(row.BankID, row.Name, row.Lat, row.Lng)
