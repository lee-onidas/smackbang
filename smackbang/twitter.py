from textblob import TextBlob
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from app import Twitter

consumerKey = "PqA88zMUxSwVZi5hJpKdVKT4L"
consumerSecret = "WQ1xDXrygO4US93heMenGkj5z6DZeUQrZDIyoACAVZqtzulpPc"
accessToken = "1499085994561310727-p9J1gRV1tsLrVowGCvinw3lEvMHB5z"
accessTokenSecret = "zVxDSNXC8qmv2ZR5ZD6bE7rT0EmaRewTJxakYlQx89ncL"
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

#Sentiment Analysis


keyword = input("Please enter keyword or hashtag to search: ")
noOfTweet = 2000

#tweets = tweepy.Cursor(api.search_tweets(), q=keyword).items(noOfTweet)
tweets = api.search_tweets(q=keyword, count=noOfTweet)

tweet_list = []

for tweet in tweets:
    #print(tweet.text)
    tweet_list.append(tweet.text)

#Tweets to DF
tweet_list = pd.DataFrame(tweet_list)

#Clean the data
tweet_list.drop_duplicates(inplace = True)
tw_list = pd.DataFrame(tweet_list)

#Make another column to compare
tw_list["text"] = tw_list[0]

#More cleaning
remove_rt = lambda x: re.sub('RT @\w+:'," ",x)
rt = lambda x: re.sub('(@[A-Za-z0–9]+)|(\w+:\/\/\S+)'," ",x)
removen = lambda x: re.sub('\n',' ', x)
tw_list["text"] = tw_list.text.map(remove_rt).map(rt).map(removen)
tw_list["text"] = tw_list.text.str.lower()

#I will try to simplify this
tw_list[["polarity", "subjectivity"]] = tw_list["text"].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
for index, row in tw_list["text"].iteritems():
    score = SentimentIntensityAnalyzer().polarity_scores(row)
    neg = score["neg"]
    neu = score["neu"]
    pos = score["pos"]
    comp = score["compound"]
    if neg > pos:
        tw_list.loc[index, "sentiment"] = "negative"
    elif pos > neg:
        tw_list.loc[index, "sentiment"] = "positive"
    else:
        tw_list.loc[index, "sentiment"] = "neutral"
        tw_list.loc[index, "neg"] = neg
        tw_list.loc[index, "neu"] = neu
        tw_list.loc[index, "pos"] = pos
        tw_list.loc[index, "compound"] = comp

def thumb(neg,neu,pos):
    if pos+(neu/2) >= neg+(neu/2):
        return "👍"
    else:
        return "👎"

#Output a simplified DF
def count_values_in_column(data,feature):
    total=data.loc[:,feature].value_counts(dropna=False)
    percentage=round(data.loc[:,feature].value_counts(dropna=False,normalize=True)*100,2)
    df= pd.concat([total,percentage],axis=1,keys=["Total","Percentage"])
    df["Verdict"] = thumb(df["Total"].loc["negative"], df["Total"].loc["neutral"], df["Total"].loc["positive"])
    return df


#Count_values for sentiment
count_values_in_column(tw_list,"sentiment")
