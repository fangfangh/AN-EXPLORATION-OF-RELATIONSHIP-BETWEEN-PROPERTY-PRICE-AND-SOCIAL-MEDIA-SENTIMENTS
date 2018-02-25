import couchdb
# info for couch DB
#user = "admin"
#password = "12345678"
user="readonly"
password="ween7ighai9gahR6"
# connects to couchDB
#couch = couchdb.Server("http://%s:%s@43.240.96.22:5984//" % (user, password))
couch = couchdb.Server("http://%s:%s@45.113.232.90:5984//" % (user, password))
# requesting exist view from database
counts = couch['twitter'].view('twitter/geoindex',
                                     reduce=False, descending=True,stale="ok",limit=5)