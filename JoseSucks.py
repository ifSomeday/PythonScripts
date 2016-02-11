import requests, pickle, tweepy, time, keys
CONSUMER_KEY = keys.CONSUMER_KEY
CONSUMER_SECRET = keys.CONSUMER_SECRET 
ACCESS_TOKEN = keys.ACCESS_TOKEN
ACCESS_SECRET = keys.ACCESS_SECRET
KEY = keys.KEY
GETPROFILE = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"
GETMATCHES = "https://na.api.pvp.net/api/lol/na/v2.2/matchlist/by-summoner/"
GETMATCHINFO = "https://na.api.pvp.net/api/lol/na/v2.2/match/"
CHAMPINFO = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/"
BEGINTIME = "beginTime="
JOSE = "FalconBlitzKrieg"
JOSEID = "47780020"
requestsMade = 0
matchTime = 0;
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def loadPickle():
    try:
        with open('latesttime.pickle','rb') as f:
            matchTime = pickle.load(f)
            matchTime = int(matchTime)
            print('latest=', matchTime)
            
    except:
        print("generating pickle")
        with open('latesttime.pickle','wb') as f:
            pickle.dump('0',f)
            matchTime = 1454792827096
    return(matchTime)

def dumpPickle(matchTime):
    with open('latesttime.pickle', 'wb') as f:
        pickle.dump(matchTime,f)

def main():
    matchTime = loadPickle()
    r = requests.get(GETMATCHES + JOSEID + "?" + BEGINTIME + str(matchTime) + "&" + KEY)
    requestsMade = 1
    mjson = r.json()
    matchTime = mjson['matches'][0]['timestamp']
    #dumpPickle(matchTime)
    for match in mjson['matches']:
        r2 = requests.get(GETMATCHINFO + str(match['matchId']) + "?" + KEY)
        requestsMade += 1
        if(requestsMade > 9):
            print('sleeping')
            requestsMade = 0
            time.sleep(10)
        infojson = r2.json()
        slotID = 0
        for identities in infojson['participantIdentities']:
            if(str(identities['player']['summonerId']) == JOSEID):
                slotID = int(identities['participantId']-1)

        kills = infojson['participants'][slotID]['stats']['kills']
        deaths = infojson['participants'][slotID]['stats']['deaths']
        assists = infojson['participants'][slotID]['stats']['assists']
        if(kills+assists == 0):
            champjson = requests.get(CHAMPINFO + str(infojson['participants'][slotID]['championId']) + "?" + KEY).json()
            requestsMade += 1
            if(requestsMade > 9):
                print('sleeping')
                requestsMade = 0
                time.sleep(10)
            tweet = "Jose literally contributed nothing to his team on " + champjson['name'] + ".\nK/D/A: " + str(kills) + "/" + str(deaths) + "/" + str(assists)
            print(tweet)
            api.update_status(status=tweet)
        else:
            if(not deaths ==0 and (kills+assists)/deaths < 1.0):
                champjson = requests.get(CHAMPINFO + str(infojson['participants'][slotID]['championId']) + "?" + KEY).json()
                requestsMade += 1
                if(requestsMade > 9):
                    print('sleeping')
                    requestsMade = 0
                    time.sleep(10)
                tweet = "Jose fed uncontrollably on " + champjson['name'] + ".\nK/D/A: " + str(kills) + "/" + str(deaths) + "/" + str(assists)
                print(tweet)
                api.update_status(status=tweet)
        dumpPickle(matchTime)
main()
