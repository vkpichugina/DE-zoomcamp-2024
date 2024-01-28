select * from green_taxi_data
limit 20;

select * from zones
limit 20;

/*Question 3. Count records
How many taxi trips were totally made on September 18th 2019?
Tip: started and finished on 2019-09-18.
Remember that lpep_pickup_datetime and lpep_dropoff_datetime columns are in the format timestamp (date and hour+min+sec) and not in date.
*/
select count(*) from green_taxi_data
where cast(lpep_pickup_datetime as date)=date'2019-09-18'
or cast(lpep_dropoff_datetime as date)=date'2019-09-18';

/*Question 4. Largest trip for each day
Which was the pick up day with the largest trip distance Use the pick up time for your calculations.
*/
select cast(lpep_pickup_datetime as date) from green_taxi_data
where trip_distance=(select max(trip_distance) 
					 from green_taxi_data);

/*Question 5. Three biggest pick up Boroughs
Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown
Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
*/
select z."Borough", round(sum(total_amount)) as sm 
from green_taxi_data gt
join zones z on gt."PULocationID" =z."LocationID" 
where cast(lpep_pickup_datetime as date)=date'2019-09-18'
and z."Borough"<>'Unknown'
group by z."Borough"
having sum(total_amount)>50000
order by sm desc;

/*Question 6. Largest tip
For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip? We want the name of the zone, not the id.
Note: it's not a typo, it's tip , not trip
*/
select zdo."Zone", max(tip_amount) as mta
from green_taxi_data gt
join zones zpu on gt."PULocationID" =zpu."LocationID" 
join zones zdo on gt."DOLocationID" =zdo."LocationID" 
where extract(month from lpep_pickup_datetime)=9
and extract(year from lpep_pickup_datetime)=2019
and zpu."Zone"='Astoria'
group by zdo."Zone"
order by mta desc
limit 1



