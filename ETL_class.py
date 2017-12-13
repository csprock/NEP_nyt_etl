
class newyorktimesETL:
    
    # initialize class variables
    KEYS = dict()
    returned_results = list()
               
    ###########################################################################
    def __init__(self, key_dictionary):
        
        if type(key_dictionary) == dict:
            self.KEYS = key_dictionary
            print("Instance of newyorktimesETL objected created with " + str(len(key_dictionary)) + " API keys.")
        else:
            raise TypeError("Object must be initialized with a dictionary.")
        

    def __del__(self):
        print("Instance of " + self.__class__.__name__ + " removed.")
        
    ###########################################################################
    ## create methods for checking the status of API key dictionary
    ## methods can be called by object instance
    ## methods used by getAllResults()
    
    def keyStatus(self):
        print(self.KEYS)
    
    # checks to see if any API keys are available
    def checkKeys(self):
        if True in self.KEYS.values():
            return True
        else:
            return False
    
    # returns first available API key
    def nextKey(self):
        trues = []
        for i , val in enumerate(self.KEYS.values()):
            if val is True:
                trues.append(i)
        
        if len(trues) > 0:
            return list(self.KEYS.keys())[trues[0]]
        else:
            return None
        
                
    ###########################################################################
    ########### methods for pulling data from API #############################
    ###########################################################################
    

    
    # formats data returned by API
    # called by __process_results()
    def __formatDoc(self, article): 
    
        
        # formats byline string as returned by the API
        # called by __formatDoc()
        def _extract_authors(byline):
            byline = re.sub('And |and ', ',', re.sub('By |Por ','', byline)).split(',')
            name_list = []
            for s in byline:
                if len(s) > 1:
                    name_list.append(s.strip())
                
            return name_list
    
        #################################
        document = {}
        
        document['id'] = article['_id']
        document['date'] = article['pub_date']
        document['type'] = article['document_type']
        document['url'] = article['web_url']
        document['keywords'] = article['keywords']
        
        try:
            document['headline'] = article['headline']['main']
        except KeyError:
            document['headline'] = None
        
        try:
            document['material'] = article['type_of_material']
        except KeyError:
            document['material'] = None
            
        # source
        try:
            document['source'] = article['source']
        except KeyError:
            document['source'] = None
        
        # byline
        try:
            document['original'] = _extract_authors(article['byline']['original'])
        except TypeError:
            document['original'] = None
        except KeyError:
            document['original'] = None
    
        # lead paragraph
        try:
            document['lead_paragraph'] = article['lead_paragraph']
        except KeyError:
            document['lead_paragraph'] = None
        
        # abstract
        try:
            document['abstract'] = article['abstract']
        except KeyError:
            document['abstract'] = None
                    
        # snippet
        try:
            document['snippet'] = article['snippet']
        except KeyError:
            document['snippet'] = None
                    
        # desk
        if 'news_desk' in article.keys():
            document['desk'] = article['news_desk']
        elif 'new_desk' in article.keys():
            document['desk'] = article['new_desk']
        else:
            document['desk'] = None
                    
        # page
        try:
            document['page'] = article['print_page']
        except KeyError:
            document['page'] = None
                    
        # word count        
        try:
            document['word_count'] = article['word_count']
        except KeyError:
            document['word_count'] = None
                    
        # section
        try:
            document['section'] = article['section_name']
        except KeyError:
            document['section'] = None
                    
        # subsection
        try:
            document['subsection'] = article['subsection_name']
        except KeyError:
            document['subsection'] = None
                            
        return document
    
    # executes API query, checks for error messages and format of returned data
    # called by __getAllResults()
    def __executeQuery(self, api_obj, **kwargs):

        results = api_obj.search(**kwargs)
        
        try:
    
            if results['status'] == 'ERROR':
                mssg = results['errors'][0]
                status = False
                stat_type = results['status']
                
            elif results['status'] == 'OK':
                
                if int(results['response']['meta']['hits']) == 0:
                    mssg = "No results found."
                    status = False
                    stat_type = 'EMPTY'
                    
                else:
                    mssg = results['status']
                    status = True
                    stat_type = results['status']
            else:
                mssg = results['message']
                status = False
                stat_type = "UNKNOWN"
                
                
        except KeyError:      
            status = False
            mssg = results['message']
            if mssg == 'API rate limit exceeded':
                stat_type = "LIMIT"
            else:
                stat_type = "ERROR"
            
        return {'status':status, 'status_type':stat_type, 'message':mssg, 'data':results}

    # applies __formatDoc() over list of results returned by API
    # called by __getAllResults()
    def __process_results(self, results):
        data_list = []
        for d in results['data']['response']['docs']:
            data_list.append(self.__formatDoc(d))
        return data_list


    def __getAllResults(self, start_page, stop_page, **kwargs):
        
        current_key = self.nextKey()
        api = articleAPI(current_key)
        current_page = start_page
        nextPage = True
        
        document_list = []
        
        while nextPage == True:
            
            try:
                
                results = self.__executeQuery(page = current_page, api_obj = api, **kwargs)
            
                if results['status'] == True:
                    document_list.extend(self.__process_results(results))
                    hits = results['data']['response']['meta']['hits']
                    
                    if current_page == start_page:
                        if hits // 10 > 200:
                            raise ValueError("Warning! The number of pages will exceed 200! Number of hits is " + str(hits))
                        else:
                            print("Number of results pages: " + str(hits // 10 + 1))
                    

                    mssg = "Status: OK. Current page: " + str(current_page)
                    print(mssg)
                    current_page += 1

                    time.sleep(1)
                else:
    
                    if results['status_type'] == "EMPTY":
                        raise ValueError(results['message'])
                    elif results['status_type'] == "LIMIT":
                        self.KEYS[current_key] = False
                        if self.checkKeys() == False:
                            print("All APIs have reached their limits. Current page: " + str(current_page))
                            nextPage = False
                        else:
                            print("API limit reached at page " + str(current_page) + ". Switching API key.")
                            current_key = self.nextKey()
                            api = articleAPI(current_key)
                    else:
                        raise ValueError("Warning! Error encountered: " + results['message'] + ' at page ' + str(current_page))
                
                if current_page > hits // 10:
                    nextPage = False
                elif current_page == stop_page:
                    nextPage = False
    
                
            except ValueError as err:
                print(err)
                return (document_list, current_page, hits)
                
        return (document_list, current_page, hits)

    ###########################################################################
    # methods that are called by the user to start 
    
    
    # kwargs for article search API
    # q
    # fq
    # begin_date
    # end_date
    
    # executes API query
    def runAPIquery(self, start_page = 0, stop_page = None, **kwargs):
        self.returned_results = self.__getAllResults(start_page, stop_page, **kwargs)
        
    # return results produced by __getAllResults()
    def returnResults(self):
        return self.returned_results
    
    ###########################################################################
    ########## methods for writing data to database ###########################
    ###########################################################################
    
    
    def __articleTuple(self, record):
        
        #format date  
        DATE = list(map(int, str(record['date'].split("T")[0]).split("-")))
        DATE = datetime.date(DATE[0],DATE[1],DATE[2])
        
        try:
            page = int(record['page'])
        except:
            page = None
            
        try: 
            word_count = int(record['word_count'])
        except:
            word_count = None
            
        ID = str(record['id'])
        headline = record['headline']        
        lead_paragraph = record['lead_paragraph']
        url = record['url']
        section = record['section']
        subsection = record['subsection']
        desk = record['desk']
        material = record['type']
        abstract = record['abstract']
        snippet = record['snippet']
        source = record['source']
    
        return (ID, headline, lead_paragraph, DATE, page, word_count, url, section, subsection, desk, material, abstract, snippet, source)
        
    
    def __keywordTuples(self, record):    
        ID = str(record['id'])
        keywords = []
        
        for kywd in record['keywords']:
            if len(kywd['value']) <= 100:
                keywords.append((ID, kywd['name'], kywd['value']))
            else:
                pass
            
        return keywords
    
    
    def __bylineTuples(self, record):
        ID = str(record['id'])
        
        if record['original'] == None:
            return [(ID, None)]
        else:
            bylines = []
            for b in record['original']:
                if len(b) <= 75:
                    bylines.append((ID, b))
            return bylines
    
    # opens database connection (requires psycopg2)
    # called by writeResults()
    def __connectToDatabase(self, db_name, psswrd, user, success_message = True):
        conn_string = "host='localhost' dbname='%s' user='%s' password='%s'" % (db_name, user, psswrd)
        
        try:
            conn = psycopg2.connect(conn_string)
            if success_message is True:
                print("Connected to database %s." % (db_name))
                
            return conn
        except:
            print('Error! Failure to connect to database %s' % (db_name))


    def reset(self):
        self.returned_results = list()
        print("ETL reset.")

    def writeResults(self, db_name, psswrd, user):
        
        if len(self.returned_results) == 0:
            raise ValueError("No results to write. You must run 'runAPIquery' first.")
        
        conn = self.__connectToDatabase(db_name, psswrd, user)
        
        for record in self.returned_results[0]:
            
            try:
                cur = conn.cursor()
                
                try:
                    cur.execute("INSERT INTO article VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", self.__articleTuple(record))
                except psycopg2.IntegrityError:
                    conn.rollback()
                else:
                    conn.commit()
                
                cur.close()
            except Exception as err:
                print(err)
        
        #### insert tags/keywords #####
        
        for record in self.returned_results[0]:
            try:
                cur = conn.cursor()
                
                kywrds = self.__keywordTuples(record)
                
                for k in kywrds:
                    try:
                        cur.execute("INSERT INTO tags VALUES (%s,%s,%s);", k)
                    except psycopg2.IntegrityError:
                        conn.rollback()
                    else:
                        conn.commit()
                
                cur.close()
                
            except Exception as err:
                print(err)
                
        #### insert bylines ####
        
        for record in self.returned_results[0]:
            try:
                cur = conn.cursor()
                
                bylines = self.__bylineTuples(record)
                
                for b in bylines:
                    try:
                        cur.execute("INSERT INTO byline VALUES (%s, %s);", b)
                    except psycopg2.IntegrityError:
                        conn.rollback()
                    else:
                        conn.commit()
                
                cur.close()
            except Exception as err:
                print(err)
        
        conn.close()
        
        print("Finished database write.")
        
###############################################################################