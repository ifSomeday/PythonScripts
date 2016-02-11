import tweepy, pickle
from keys.py import *



#for tweet in public_tweets:
 #   print(tweet.text)

def loadPickle():
    try:
        with open('twitbotline.pickle','rb') as f:
            i = pickle.load(f)
    except:
        print("generating pickle")
        with open('twitbotline.pickle','wb') as f:
            pickle.dump('0',f)
            i = 0

def apiSetup():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    public_tweets = api.home_timeline()

def main():
    apiSetup()
    loadPickle()

main()
