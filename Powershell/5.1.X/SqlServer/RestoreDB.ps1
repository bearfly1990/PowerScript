$database = "xxxxxx"
$backupLocation = "D:\SQLBackup\xxxx.bak"
$dataSource = "xxxxx"
$userid = "sa"
$password ="xxxx"
# $connectionString = "Server=$dataSource;Database=$database;IntegratedSecurity=True;"
$connectionString = "Server=$dataSource;Database=$database;User Id=$userid;Password=$password;"
# $dataFileLocation = "E:\SQL2012\xxxx.mdf"
# $logFileLocation = "E:\SQL2012\xxxx.ldf"

$sql = @"

USE [master]

ALTER DATABASE [$database] 
    SET SINGLE_USER WITH ROLLBACK IMMEDIATE

RESTORE DATABASE [$database] 
FROM DISK = N'$backupLocation' 
WITH REPLACE,RECOVERY
-- MOVE N'CurrentDB' TO N'$dataFileLocation',  
--MOVE N'CurrentDB_log' TO N'$logFileLocation',  
--NOUNLOAD, REPLACE, STATS = 5

ALTER DATABASE [$database] 
    SET MULTI_USER
"@

# invoke-sqlcmd $sql

$connection = New-Object System.Data.SqlClient.SqlConnection
$connection.ConnectionString = $connectionString
$connection.Open()
$command = $connection.CreateCommand()
$command.CommandText = $sql

$result = $command.ExecuteScalar()
$result
$connection.Close()
"Restore Finished!"
