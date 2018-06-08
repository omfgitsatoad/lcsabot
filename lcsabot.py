import re
import os
import random as rng
import markovify
import tweepy
from time import sleep
from optparse import OptionParser

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_secret = os.environ['ACCESS_SECRET']

hashtags = [
    ' #southboiz',
    ' #docketdaddy',
    ' #biginthegame',
    ' #wrongchat',
    ' #messfam',
    ' #messlife',
    ' #londonmess',
    ' #neverdeliveralwayssleep',
    ' #tentoes',
    ' #10toes',
    ' #3arun',
    ' #comesouth',
    ' #noisis',
    ' #manciniyoucreep',
    ' #calltheguy',
    ' #nicshadadrink',
    ' #crud',
    ' #cruddy',
    ' #greez',
    ' #calm',
    ' #truss'
]

def corpusFromChatlog(chatlog):
    places = [
        'scrutton',
        'soho',
        'leather lane',
    ]
    chatlog = open(chatlog, 'r')
    corpus = []
    for line in chatlog:
        line = re.sub(r'\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - ', '', line)
        line = re.sub(r'@\d{12}', ' ', line)
        line = re.sub(r'@\d{11}', ' ', line)
        line = re.sub(r'university', places[rng.randrange(0,len(places))], line)
        if ':' in line:
            line = line.split(':', 1)
            corpus.append(line[1])
        else:
            corpus.append(line)

    corpusFile = open('corpus.txt', 'w')
    count = 0
    for line in corpus:
        corpusFile.write(corpus[count])
        count += 1

    corpusFile.close()
    chatlog.close()


def tweet(model, suffix, api):
    status = model.make_short_sentence(200 - len(suffix))+suffix
    try:
        api.update_status(status)
    except tweepy.TweepError as e:
        print(e.reason)

def getRandomFollowerName(api):
    followers = api.followers_ids()
    if len(followers) > 0:
        user_id = followers[rng.randrange(0,len(followers))]
        user = api.get_user(user_id)
        return user.screen_name
    else:
        return None


def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token,access_secret)
    api = tweepy.API(auth)

    corpusFromChatlog('chatlog.txt')
    corpus = open('corpus.txt', 'r')
    model = markovify.Text(corpus, state_size=2)
    corpus.close()



    run = True
    while(run):
        addendum = ' #lcsa'
        if rng.randrange(0,100) > 30:
            addendum = hashtags[rng.randrange(0,len(hashtags))]+addendum

        if rng.randrange(0,100) > 95:
            user = getRandomFollowerName(api)
            if user != None:
                addendum = ' @'+user+addendum
        # new tweet
        tweet(model,addendum,api)
        delay = rng.randrange(15,120)

        sleep(delay*60)

if __name__ == '__main__':
    main()

