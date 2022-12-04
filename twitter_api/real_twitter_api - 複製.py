import snscrape.modules.twitter as snstwitter
import pandas as pd
from pprint import pprint
import time
from flask import*
import configparser, tweepy

app = Flask(__name__, static_folder="public", static_url_path="/")
app.secret_key="123456"

# 處理路由
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    
    tweets = []
    from_date = request.args.get("from", "")
    to_date = request.args.get("to", "")
    count = request.args.get("count", "")
    query = f"covid-19 (#covid-19) until:{to_date} since:{from_date}"
    try:
        for tweet in snstwitter.TwitterSearchScraper(query).get_items():
            if len(tweets) == int(count):
                break
            else:
                tweets.append([tweet.date, tweet.user.username, tweet.content])
        df = pd.DataFrame(tweets, columns=['Date', 'User', 'Text'])
        json_formmat = pd.DataFrame.to_json(df, orient='records')
        pprint(json_formmat)
    
        return render_template("result_page.html", result=json_formmat)
    except:
        return render_template("error.html")
    
@app.route("/quicksearch")
def quicksearch():

    config = configparser.ConfigParser()
    config.read("config.ini")
    api_key = config['twitter']['api_key']
    api_key_secret = config['twitter']['api_key_secret']
    access_token = config['twitter']['access_token']
    access_token_secret = config['twitter']['access_token_secret']

    # authentication
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    keywords = ["covid-19", "#covid-19"]
    limit = 100    
    get_localtime = time.localtime() 
    localtime = time.strftime("%Y-%m-%d", get_localtime)        
    tweets = tweepy.Cursor(api.search_tweets, q=keywords, until=localtime, tweet_mode = "extended").items(limit)

    columns = ['Date', 'User', 'Text']
    data = []

    for tweet in tweets:
        data.append([tweet.created_at, tweet.user.screen_name, tweet.full_text])

    df = pd.DataFrame(data, columns=columns)
    json_format = pd.DataFrame.to_json(df, orient='records')
    pprint(json_format)
    return render_template("result_page.html", result=json_format)

app.run(port=3000)
        

