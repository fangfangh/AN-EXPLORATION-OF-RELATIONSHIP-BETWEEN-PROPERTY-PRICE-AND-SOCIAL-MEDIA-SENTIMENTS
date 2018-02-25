import tweepy
import couchdb
import json

# Essential information for the twitter api authentication
consumer_key = "uZ1GTFPFk9JMPEzrXPDJRDEUI"
consumer_secret = "zf7XGACgxtLRwuJyqTBFxbhmmnD3hBfdwEIeuShdgO51eLof8l"
access_token = "1075921620-u6NuHGTBrs5H8O2qqxbiLsRxVXt67QMMywxtGAN"
access_token_secret = "can1AIRhKxit4yz7C1jWWyQ0hzzSfTSfXP2vaTFyo5Dn0"

# pass our consumer key  to Tweepy's user authentication handler
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# pass our access token and access secret to tweepy
auth.set_access_token(access_token, access_token_secret)
# Creating a twitter API wrapper using tweepy
api = tweepy.API(auth)
count=0

#sydeny and perth location
sydney = 151.0103360483,-33.9982467898,151.4159790724,-33.7001897961
perth  = 115.6964492016,-32.2328805327,116.100279325,-31.6829344398
# info for couch DB
user = "admin"
password = "12345678"
couchserver = couchdb.Server("http://%s:%s@43.240.96.22:5984/" % (user, password))
dbname = "perth_tweets"
if dbname in couchserver:
    db = couchserver[dbname]
else:
    db = couchserver.create(dbname)

keyword_list = ["property value","house","real estate",
                "property price","house price","sold price",
                "#house","housing","#property","#realestate"]


# create a listener that prints the text of any tweet that comes from the Twitter API
class StreamListener(tweepy.StreamListener):

    # filter out retweet
    def on_status(self, status):

        name_id = status.user.screen_name
        print("start!!!!!!!! {0}".format(name_id))
        # go direct into user's profile download all his posts
        self.download_from_timeline(name_id)

    # method of stream listener to handle errors coming from the Twitter API properly
    def on_error(self, status_code):
        if status_code == 420:
            return False

    # method used to download from particular user
    def download_from_timeline(self,name_id):
        for tweet in tweepy.Cursor(api.user_timeline,id=name_id,
                                   wait_on_rate_limit=True,
                                   wait_on_rate_limit_notify=True).items(500):
            # if user's tweet contain any keyword then save it to couchDB
            if any(word in tweet.text for word in keyword_list):
                    self.save_to_couchdb(tweet._json)
                    continue

    #method to store the tweet into couchDB
    def save_to_couchdb(self,tweet):
        db.save(tweet)


# create an instance of MystreamListener class
stream_listener = StreamListener()
# pass our authentication credentials
stream = tweepy.Stream(auth=api.auth,listener=stream_listener)
# filter tweets from Sydney
stream.filter(locations=[115.6964492016,-32.2328805327,116.100279325,-31.6829344398])
