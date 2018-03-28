## TargetBanks

### Database
Create new DB in SQL Server, name it "bkrob".
Create a new sql login for the database, username="bkrob_adm", password="bkrob_adm".
Set "bkrob_adm" user mapping to "bkrob" database.
Give "bkrob_adm" user membership as db_owner.

### SSIS Import
In the /data folder, import these data into the FFL and CrimeRate tables:
* ffl_TX_import.xlsx
* TX_Crimes_City_2016.xlsx

### DATA Gatherings
Run python code in /data_parse/:
* get_banks_TX.py #parse FDIC data TX and enter into DB
* get_ratings.py #ratings and reviews from google api
* get_police_TX.py #parse policeone.com for TX police infos

### DATA Clean Up
In the SQL table PoliceStations, replace Officers # if it seems way too high, also remove duplicates based on LAT data.

### DATA FILL
#### Geocoding
Run python code in /data_fill/:
* banks_geocode.py #fill in lat/lng from google API geocode
* police_geocode.py
* ffl_geocode.py

#### Take, Count and Probabilities 
Run python code in /data_fill/:
* take.py  #Money that's available to take
* banks_closest.py  # Closest police stations for each bank
* ffl_count.py  # Number of closest FFL for each bank
* pdistance.py  # Possibility of getting caught by distance to PoliceStations, based on a formula
* officers_rate.py  # Number of police/pop. served per 1000

### Sample Data
Create sample data from /sql/sample.sql.

### Target on Sample Data
Run python script /data_fill/target.py
