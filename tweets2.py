import snscrape.modules.twitter as snstwitter
import pandas as pd
from pprint import pprint
import pymongo
import time
from flask import*

app = Flask(__name__, static_folder="public", static_url_path="/")
app.secret_key="123456"

client = pymongo.MongoClient("mongodb+srv://Leo:27092633@leocluster.svkl3gk.mongodb.net/?retryWrites=true&w=majority")# 把資料放進資料庫中
db = client.twitter_api #選擇操作twitter_api資料庫
collection = db.tweets #選擇操作tweets集合
print("伺服器連線成功")


@app.route("/cal")
def cal():
    
    until_year = 2020
    until_month = 2
    since_year = 2020
    since_month = 1
    tweets = []
    index = 0

    while until_year < 2023:

        query = f"covid-19 (#covid-19) until:{until_year}-{str(until_month)}-01 since:{since_year}-{str(since_month)}-01"
        for tweet in snstwitter.TwitterSearchScraper(query).get_items():
            index += 1 
            
        tweets.append([str(since_year)+'/'+str(since_month)+'/01'+'-'+str(until_year)+'/'+str(until_month)+'/01' ,index])
        
        result = collection.insert_one({
            f"{since_year}/{since_month}/01-{until_year}/{until_month}/01":index
        })
        print(result)

        time.sleep(30)
        index = 0

        if until_month < 12:
            until_month += 1
        else:
            until_month = 1 
            until_year += 1

        if since_month < 12:
            since_month += 1
        else:
            since_month = 1 
            since_year += 1

    df = pd.DataFrame(tweets, columns=['Interval', 'Number'])
    pprint(df)
    df.to_csv('pandemic.csv')
    

# 處理路由
@app.route("/")
def home():
    databse_number = {}
    collection = db.tweets
    cursor = collection.find()
    for n in cursor:
        databse_number.update(n)
    return databse_number

app.run(port=3000)
        