INSERT INTO BankSample (
    	[UniqueNum]
    ,[Name]
    ,[Address1]
    ,[Address2]
    ,[City]
    ,[State]
    ,[Zip]
    ,[Deposit]
    ,[Lat]
    ,[Lng]
    ,[ClosestStationID]
    ,[ClosestPSDistance]
    ,[MeanPSDistance]
    ,[PSCount]
    ,[Take]
    ,[PDistance]
    ,Officers1000
    ,[FFLCount]
	 )
SELECT TOP 10 PERCENT 
    	[UniqueNum]
    ,[Name]
    ,[Address1]
    ,[Address2]
    ,[City]
    ,[State]
    ,[Zip]
    ,[Deposit]
    ,[Lat]
    ,[Lng]
    ,[ClosestStationID]
    ,[ClosestPSDistance]
    ,[MeanPSDistance]
    ,[PSCount]
    ,[Take]
    ,[PDistance]
    ,Officers1000
    ,[FFLCount]
FROM Bank
ORDER BY rand(checksum(*))

