import tweepy
from credentials import *
from flask import Flask, render_template, request, url_for, redirect
from pymorphy2 import MorphAnalyzer
import json


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

def twi_search(words):
    words = words.split(' ')
    print(words)
    data = []
    for word in words:
        word = word.strip(',.^&!?;;"')
        data.append(get_data(word))
    return table_data(data, words)

def wordforms(word):
    arr = []
    morph = MorphAnalyzer()
    lex = morph.parse(word)[0].lexeme 
    for l in lex:
        arr.append(l.word)
    return set(arr)

def get_data(word):
    dates = []
    d = {}
    for wordform in wordforms(word):
        tweets = tweepy.Cursor(api.search, q=wordform, count=100, result_type='recent').items()
        for tweet in tweets:
            if wordform.lower() in tweet.text.lower():
                dates.append(str(tweet.created_at.month) + '.' + str(tweet.created_at.day))
    for el in set(dates):
         d[el] = dates.count(el)
    return d

def table_data(data, words):
    arr = []
    days = data[0].keys()
    labels = ['days'] + words
    arr.append(labels)
    for day in days:
        arr.append([day] + [el[day] for el in data])
    return arr

app = Flask(__name__)

@app.route('/')
def form():
    if request.args:
        word = request.args['word']
        res = json.dumps(twi_search(word), ensure_ascii=False)
        return render_template('chart.html', word=word, res=res)
    else:
        return render_template('form.html')

if __name__ == '__main__':
    app.run(debug = True)
