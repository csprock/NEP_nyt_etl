import datetime
import time
import random
import math
import psycopg2
import re
import requests



###### DO NOT CHANGE UNLESS RESETTING VALUES AFTER SUCCESSFUL RUN
API_KEYS = {'d7117d6c63404420b03ee92aa4ec9806':True,
            'df78a493cb294712b65b510b0ba136d9':True,
            '0426aee2d0204bba80aa4eff82913f1a':True,
            '315cc0084ab44abc90aa62eed6551eb6':True,
            '101c8c70cff842db97801adef91e9cab':True}
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
ETL.writeResults('nyt_articles', 'redalert', 'postgres')
ETL.reset()



# missed collection of start_date = 20080719, end_date = 20080725, start_page = 38