import tweepy, time, threading, json, requests, pickle, sys, keys

CONSUMER_KEY = keys.CONSUMER_KEY
CONSUMER_SECRET = keys.CONSUMER_SECRET 
ACCESS_TOKEN = keys.ACCESS_TOKEN
ACCESS_SECRET = keys.ACCESS_SECRET
REQUEST_URL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?account_id=75419738&key=91831BD94FD63626CF1DF4D6566ABA84&matches_requested=10'
MATCH_DETAIL_BASE = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id="
MATCH_DETAIL_KEY = keys.MATCH_DETAIL_KEY
HERO_LIST = "https://raw.githubusercontent.com/kronusme/dota2-api/master/data/heroes.json"
ACCOUNT_ID = 75419738

latest = 0
matchArray = []

def apiSetup():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    herojson = requests.get(HERO_LIST).json()
    updateMatch(herojson)
    tweetActual(api)

def loadPickle():
    try:
        with open('latestmatch.pickle','rb') as f:
            latest = pickle.load(f)
            latest = int(latest)
            print('latest=', latest)
            
    except:
        print("generating pickle")
        with open('latestmatch.pickle','wb') as f:
            pickle.dump('0',f)
            latest = 0

def getLatest():
    with open('latestmatch.pickle','rb') as f:
        latest = pickle.load(f)
        latest = int(latest)
    return(latest)

def updateLatest(new):
    with open('latestmatch.pickle', 'wb') as f:
        pickle.dump(new,f)

def updateMatch(herojson):
    newLatest = 0
    r = requests.get(REQUEST_URL)
    mjson = r.json()
    latest = int(getLatest())
    for item in mjson['result']['matches']:
        mid = item['match_id']
        if mid > latest:
            if mid > newLatest:
                newLatest = mid
            print('new match')
            for item2 in item['players']:
                if item2['account_id'] == ACCOUNT_ID:
                    if item2['player_slot'] < 5:
                        radiant = True
                    else:
                        radiant = False
                    hero_id = item2['hero_id']
            r2 = requests.get(MATCH_DETAIL_BASE + str(mid) + MATCH_DETAIL_KEY)
            njson = r2.json()
            if(njson):
                if njson['result']['radiant_win']:
                    radiantwinner = True
                else:
                    radiantwinner = False
                for item2 in njson['result']['players']:
                    if item2['account_id'] == ACCOUNT_ID:
                        kills = item2['kills']
                        deaths = item2['deaths']
                        assists = item2['assists']
                heroes = herojson['heroes']
                for mhero in heroes:
                    if mhero['id'] == hero_id:
                        hero = mhero['localized_name']
                createMatch(hero, mid, radiantwinner, kills, deaths, assists, radiant)
    if newLatest:    
        updateLatest(newLatest)

def createMatch(hero, matchid, radiantwinner, kills, deaths, assists, radiant):
    tweet = ""
    if radiantwinner and radiant or not radiantwinner and not radiant:
        tweet += "Won Match \n"
    else:
        tweet += "Lost Match \n"
    if radiant:
        tweet += "Radiant "
    else:
        tweet += "Dire "
    tweet += hero
    tweet += '\n'
    tweet += str(kills)+"/"+str(deaths)+"/"+str(assists)+'\n'
    tweet += "http://yasp.co/matches/" + str(matchid)
    print(tweet)
    matchArray.insert(0,tweet)
    
def tweetActual(api):
    for item in matchArray:
        try:
            api.update_status(status=item)
        except:
            print('exception thrown')
    
        

def main():
    loadPickle()
    apiSetup()
    sys.exit()

main()

    
