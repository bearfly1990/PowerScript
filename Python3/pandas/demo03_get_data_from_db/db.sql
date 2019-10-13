create table Test_Output(
	id int,
	UserName varchar(30),
	Age int,
	Country varchar(30),
	Status varchar(30)
)

insert into Test_Output values(1, 'cx', 29, 'China', 'Success')
insert into Test_Output values(2, 'xm', 27, 'China', 'Success')
insert into Test_Output values(3, 'll', 30, 'China', 'Failed')
insert into Test_Output values(4, 'zz', 20, 'China', 'Pending')

select * from Test_Output;
