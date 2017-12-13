# NEP_nyt_etl
News Inequality Project, classes for NYT's article API ETL pipeline

This repo contains classes for the ETL pipeline for the New York Times article API. The ETL_class.py file contains a class called newyorktimesETL
for pulling data from the New York Times' article API, processing it and loading it to a SQL database. The schema for the database can be found in 
the create_database.sql file. The ETL_run.py file contains a demonstration of how to use the ETL class. 

The newyorktimesETL is essentially a wrapper for the NYTArticleSearchAPI package found here: https://github.com/MattDMo/NYTimesArticleAPI. The articleAPI.py 
file that contains the main articleAPI class must have lines 76 and 77 commented out for Python 3 compatability. Once this class has been 
modified and loaded, you can proceed to use the newyorktimesETL class. 

The newyorktimesETL is initialized with a dictionary of keys with boolean values set to true. The script automatically pulls all articles
in a given date and page range matching the keyword arguements, cycling through API keys as download limits are reached.
The keyword arguements are the same as the articleAPI class. You must have postgres installed and the database created using the create_database.sql schema in order to use the database write functionality. 
