
DECLARE @before int
SELECT @before = count(*) from mhfsta  where poststatus=67 and trantype=1203 --begin = 5400 end = 59401
WAITFOR DELAY '00:01:00';
DECLARE @after int
SELECT @after = count(*) from mhfsta  where poststatus=67 and trantype=1203 --begin = 5400 end = 59401
select @after - @before


DECLARE @current int 
select @current = count(*) from mhfsta  where poststatus=67 and trantype=1203
select (@current -59400)*1.0 / 54195
