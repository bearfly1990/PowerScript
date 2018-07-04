--Backup DB
BACKUP DATABASE MyDatabase
TO DISK = 'D:\\SQLBackup\\****.bak'
WITH INIT --overwrite existing

BACKUP DATABASE AdventureWorks TO DISK = 'C:\AdventureWorks.BAK'

BACKUP LOG AdventureWorks TO DISK = 'C:\AdventureWorks.TRN'

BACKUP DATABASE AdventureWorks TO DISK = 'C:\AdventureWorks.DIF' WITH DIFFERENTIAL

BACKUP DATABASE TestBackup FILE = 'TestBackup' 
TO DISK = 'C:\TestBackup_TestBackup.FIL'

BACKUP DATABASE TestBackup FILE = 'TestBackup2' 
TO DISK = 'C:\TestBackup_TestBackup2.FIL'

BACKUP DATABASE TestBackup FILEGROUP = 'ReadOnly' 
TO DISK = 'C:\TestBackup_ReadOnly.FLG'

BACKUP DATABASE TestBackup READ_WRITE_FILEGROUPS
TO DISK = 'C:\TestBackup_Partial.BAK'

BACKUP DATABASE TestBackup READ_WRITE_FILEGROUPS
TO DISK = 'C:\TestBackup_Partial.DIF'
WITH DIFFERENTIAL

--Restore db
USE [master]
RESTORE DATABASE [DBName] FROM  DISK = N'*/DBName.bak' WITH  FILE = 1,  NOUNLOAD,  STATS = 5
GO

dbcc detachdb(METPDI)
RESTORE DATABASE METAPDI FROM DISK = 'D:\\SQLBackup\\****.bak'
WITH REPLACE, RECOVERY

RESTORE LOG MyAdvWorks
FROM MyAdvWorks_log2
WITH RECOVERY

-- Assume the database is lost, and restore full database, 
-- specifying the original full database backup and NORECOVERY, 
-- which allows subsequent restore operations to proceed.
RESTORE DATABASE MyAdvWorks
   FROM MyAdvWorks_1
   WITH NORECOVERY
GO
-- Now restore the differential database backup, the second backup on 
-- the MyAdvWorks_1 backup device.
RESTORE DATABASE MyAdvWorks
   FROM MyAdvWorks_1
   WITH FILE = 2,
   RECOVERY
GO
