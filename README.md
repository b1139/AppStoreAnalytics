# AppStoreAnalytics
Django client API which exposes Mobile Application's stats in PlayStore/iStore

App Store Analytics API Client - Efficiently exposes the DATA

# API Client supports limited functionalities of SQL

1. Filter by all variables eg. date, date_from, date_to, countries=CA,US country=CA

2. Groups by all variables

3. Sort by all variables, DESC -> with "-" symbol e.g -date, ASC-> date

4. Supports multiple combination of the API

# Common API use-cases:

1. Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order.
http://localhost:8000/store?group_by=channel,country&order_by=-clicks&stats=impressions,clicks&date_to=2017-06-01

2. Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order. 
http://localhost:8000/store?group_by=date&order_by=date&stats=installs&date_from=2017-05-01&date_to=2017-05-31&os=ios

3. Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order
http://localhost:8000/store?group_by=os&order_by=-revenue&stats=revenue&date=2017-06-01&country=US


4. Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order. Please think carefully which is an appropriate aggregate function for CPI.
CPI (cost per install) which is calculated as cpi = spend / installs
http://localhost:8000/store?group_by=channel&order_by=-cpi&stats=cpi,spend,channel&country=CA

# Data Source 
https://gist.github.com/kotik/3baa5f53997cce85cc0336cb1256ba8b/


# Steps to test this application

1. create virtual env 
2. Install python3
3. Install python modules from requirements.txt
4. python manage.py runserver 8000
5. https://localhost:8000/store  -> You will get to see the usages and sample API examples

