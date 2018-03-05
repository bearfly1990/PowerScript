CREATE LOGIN DBName WITH PASSWORD = 'password', CHECK_POLICY = OFF
GO

Use DBName;
GO
IF NOT EXISTS(SELECT * FROM sys.database_principals WHERE name = N'Pub52_QA')
BEGIN
    CREATE USER [DBName] FOR LOGIN [DBName]
    EXEC sp_addrolemember N'db_owner', N'DBName'
END;

CREATE LOGIN [NJ\xiche] FROM WINDOWS
GO
EXEC master..sp_addsrvrolemember @loginname = N'NJ\xiche', @rolename = N'sysadmin'
