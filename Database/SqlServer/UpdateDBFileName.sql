ALTER DATABASE DBName SET OFFLINE;

ALTER database DBName MODIFY FILE ( NAME pubqa40, filename='${Sql Server DATA Path}\DBName.mdf');
ALTER database DBName MODIFY FILE ( NAME ***, filename='***');
ALTER database DBName MODIFY FILE ( NAME ***, filename='***');

ALTER DATABASE DBName SET ONLINE;