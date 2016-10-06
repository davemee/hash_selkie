from TwitterSearch import *
import json
import threading
import atexit
from flask import Flask

global tweets_
tweets_ = {}
POOL_TIME = 300 #Seconds
dataLock = threading.Lock()
# thread handler
yourThread = threading.Thread()

def dumpem():
    return json.dumps(tweets_)

def create_app():
    app = Flask(__name__)
	
	#url_for('static', filename='index.html')
	
    def interrupt():
        global yourThread
        yourThread.cancel()

    def doStuff():
        global tweets
        global yourThread
        with dataLock:
        # Do your stuff with commonDataStruct Here
        	updateTweets()
        # Set the next thread to happen
        yourThread = threading.Timer(POOL_TIME, doStuff, ())
        yourThread.start()   

    def doStuffStart():
        # Do initialisation stuff here
        global yourThread
        # Create your thread
        yourThread = threading.Timer(POOL_TIME, doStuff, ())
        yourThread.start()


	@app.route('/')
	def hello():
	    return "Hello World!"
	
	@app.route('/tweets')
	def tweets():
		return dumpem()

	@app.route('/refresh')
	def refresh():
		updateTweets()



    # Initiate
    doStuffStart()
    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)
    updateTweets()
    app.run(host='0.0.0.0')
    return app

def updateTweets():
	try:
	    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
	    tso.set_keywords(['selkie', '#selkie']) # let's define all words we would like to have a look for
	    #tso.set_language('de') # we want to see German tweets only
	    tso.set_include_entities(False) # and don't give us all those entity information
	
	    # it's about time to create a TwitterSearch object with our secret tokens
	    ts = TwitterSearch(
	        consumer_key = 'mHQEOwI1U0YMv4uArStSJktmW',
	        consumer_secret = 'ZRBylgMXwkI18iGXwCaL1BqrOSOXzPRmRqg89Ww5C9QG6mWLU0',
	        access_token = '6713172-0das1x5i9TXCkl267VAR3F1ni46pjsLxxsZDAPakEb',
	        access_token_secret = 'nxihORPSAWyyFc06tSNEWgm5G4QxHP5gsqCxEKcC4HS8J'
	     )
	
	     # this is where the fun actually starts :)
	    for tweet in ts.search_tweets_iterable(tso):
	    	#print( json.dumps(tweet) )
	        body = ( '@%s@@@@@%s' % ( tweet['user']['screen_name'], tweet['text'] ) )
	    	tweets_[ tweet['created_at'] ]=body;	    
	    	#print(json.dumps(tweets))
	except TwitterSearchException as e: # take care of all those ugly errors if there are some
	    print(e)


app = create_app()          
