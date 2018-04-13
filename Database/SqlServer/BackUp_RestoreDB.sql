--Backup DB
BACKUP DATABASE MyDatabase
TO DISK = 'D:\\SQLBackup\\****.bak'
WITH INIT --overwrite existing

--Restore db
USE [master]
RESTORE DATABASE [DBName] FROM  DISK = N'*/DBName.bak' WITH  FILE = 1,  NOUNLOAD,  STATS = 5
GO

dbcc detachdb(METPDI)
RESTORE DATABASE METAPDI FROM DISK = 'D:\\SQLBackup\\****.bak'
WITH REPLACE, RECOVERY
