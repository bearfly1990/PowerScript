-- # Write your MySQL query statement below
-- # select name, population, area from World where population>25000000 or area>3000000

select name, population, area from World where population>25000000 
union
select name, population, area from World where area>3000000