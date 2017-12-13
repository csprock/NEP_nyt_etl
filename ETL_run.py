import datetime
import time
import random
import math
import psycopg2
import re
import requests



###### DO NOT CHANGE UNLESS RESETTING VALUES AFTER SUCCESSFUL RUN
API_KEYS = {'<api key>':True,
            '<api key>':True}
#################################################################
# kwargs for article search API
# q
# fq
# page
# begin_date
# end_date

ETL = newyorktimesETL(API_KEYS)



# RUN:
ETL.runAPIquery(begin_date = 20060512, end_date = 20060517, start_page = 192,  fq = {'document_type':'article'})
ETL.writeResults('db_name', 'password', 'username')
ETL.reset()



