# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 17:26:17 2017

@author: Manish 
"""
# TWITTER BOT CODE

""" I BELIEVE THAT YOU ARE AWARE OF CREATING TWITTER ACCOUNT, TWITTER APP AND GETTING YOUR CREDENTIALS. 
    ONCE YOU HAVE THOSE, YOU CAN DO THE FOLOWING CODE """
    
# THE FOLLOWING CODE SHOULD BE SELF EXPLANATORY AND HOPE YOU'LL UNDERSTAND AND LIKE IT
    
# IMPORTING LIBRARIES 
import tweepy
import os 
from time import sleep
from random import randint

# SETTING THE PATH
os.getcwd()
os.chdir("your directory path")

########################################################################################################

######################################################################################################
# CALLING A FILE THAT HAS TWITTER LOGIN CREDENTIALS
# PUT YOUR CREDENTIALS FROM YOUR APP

consumer_key = "xxxxxxxxxxxxxxxxxxxxxxxxx"
consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxxxx"
access_token = "xxxxxxxxxxxxxxxxxxxxxxxxx"
access_token_secret = "xxxxxxxxxxxxxxxxxxxxxxxxx"  

# LOGGINING INTO THE ACCOUNT
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# SET ACCESS TOKEN
auth.set_access_token(access_token, access_token_secret)

# CONSTRUCT THE API INSTANCE
api = tweepy.API(auth)

# TO CHECK IF WE HAVE LOGGED IN THE SAME ACCOUNT 
if (api.me().screen_name == "your twitter username"):
    print("Bot has logged in!")

######################################################################################################

#######################################################################################################

# CREATING THE FUNCTION FOR GATHERING NEW TRENDS
def new_trends():

    # FINDING THE NEW TRENDS
    try:
        trends1 = []
        names = []
        
        # COLLECTING NEW GLOBAL TRENDS
        globaltrends = api.trends_available()
        for j in range(len(globaltrends)):
            trends1.append(globaltrends[j]["woeid"])
        
        for ct in trends1:
            currenttrends = api.trends_place(ct)
            data = currenttrends[0]
            currenttrends1 = data["trends"]
            currenttrends1 = currenttrends1[:6]
            for trend in currenttrends1:
                names.append(trend["name"])
                
    except tweepy.TweepError as e:
        if("88" in e.reason):
            print("You've reached to the limit of new trends and will have to wait for 15 minutes")
        
    # TO REMOVE DUPLICATES
    names = list(set(names))
    
    return names

#######################################################################################################################

#######################################################################################################################

""" CALLING TREND FUNCTION AND STORING THE TRENDS IN A VARIABLE BECAUSE WE DON'T WANT TO CALL TRENDS EVERYTIME WE RETWEET
    IF YOU WANT TO DO MANUALLY JUST REMOVE THE HASHTAG AND RUN THE CODE BELOW """
#t = new_trends()

########################################################################################################################

########################################################################################################################

# CREATING THE FUNCTION FOR RETWEETING, FOLLOWING AND LIKING THE TWEETS
def do_retweet_follow_like():
    follow_count = 0
    retweet_count = 0
    fav_count = 0
    t = new_trends()
    counter = 0
    try:
        # WE WILL RETWEET, FOLLOW AND FAVOURITE FOR EACH OF 3 DIFFERENT TRENDS
        while(counter < 3):
            counter += 1
            random_trend = randint(0, len(t))
            # TO GET USERS FROM THE RANDOM TREND 
            for tweet in tweepy.Cursor(api.search, q = t[random_trend], lang = "en").items(1):
                try:
                    #while(follow_count < 3):
                    # FOLLOWER BOT
                    if(tweet.user.following == False):
                        follow_count += 1
                        tweet.user.follow()
                        print("I followed: " + tweet.user.screen_name)
                        print("Follow Count is: " + str(follow_count))
                    else:
                        print("Follow Count is: " + str(follow_count))
                        print("I have already followed: " + tweet.user.screen_name)
                
                    # RETWEETING BOT 
                    if(tweet.retweeted == False):
                        retweet_count += 1
                        tweet.retweet()
                        print("I just retweeted:" + tweet.user.screen_name)
                        print("Retweet Count is: " + str(retweet_count))
                    else:
                        print("Retweet Count is: " + str(retweet_count))
                        print("I have already retweeted.")
                        
                    # FAVORITING BOT
                    if(tweet.favorited == False):
                        fav_count += 1
                        tweet.favorite()
                        print("I liked tweet, tweeted by: " + tweet.user.screen_name)
                        print("Favorite Count is: " + str(fav_count))
                    else:
                        print("Favorite Count is: " + str(fav_count))
                        print("I have already liked this tweet")
                       
                # HERE EXCEPTION IS IN TWEEPERROR FORMAT AND E.REASON IS IN STRING FORMAT. HENCE WE USE DOUBLE QUOTES        
                except tweepy.TweepError as e:
                    if("327" in e.reason):
                        print("You've already retweeted")
                        
    except IndexError as er:
        print("Done!, You've retweeted, liked and followed with 15 different tweets now wait for 1 hour.")                
       
    print("Done!, You've reached the follower's limit, now wait for 1 hour")    
    sleep(3600)
    print("New Tweeting!")
    do_retweet_follow_like()
            
####################################################################################################################

####################################################################################################################

# CREATING THE FUNCTION TO MESSAGE THE FOLLOWERS 
# RETRIVING FOLLOWERS AND SENDING THEM THANK YOU MESSAGE
# GETTING USERS TO WHOM WE HAVE SENT DIRECT MESSAGE
def msg_to_follower():
    
    sent_msg_user = api.sent_direct_messages()
    sent_user_id = []
    for i in range(len(sent_msg_user)):
        sent_user_id.append(sent_msg_user[i].recipient_id) 
    
    # GETTING ALL FOLLOWERS
    userid = api.followers_ids()
    l = len(userid)
    while (l != 0):
        for i in userid:
            print(i)
            if(i in sent_user_id):
                print("I already sent direct message")
                l = l - 1
                print(l)
                continue
            else:
                message = "Thank you for following me, cheers!"
                api.send_direct_message(i, text = message)
                print("Sent direct message to: " + str(i))
                l = l - 1
                       
        #return print("Done!")

    print("Sleeping for 1 hour!")
    sleep(3600)
    msg_to_follower()

# MAXIMUM TWEETS ARE 295 for quaraterly period.

######################################################################################################################

######################################################################################################################

# CALL THE FUNCTION IF YOU WANT NEW TRENDS
t = new_trends()

# CALL THE FUNCTION IF YOU WANT TO RETWEET, LIKE AND FOLLOW SOMEONE
do_retweet_follow_like()

# CALL THE FUNCTION IF YOU WANT TO MESSAGE TO YOUR FOLLOWERS        
msg_to_follower() 
    
################################################################################################################

################################################################################################################
# BOT THAT WILL POST 
# 1ST WAY
# MANUAL TWEET BY USER i.e. YOU
api.update_status("Hi there, I am new to the twitter website!")

##################################################################################################################

#################################################################################################################
# 2ND WAY
# READING FROM THE FILE AND POSTING YOUR TWEET
def post():
    filename = open('bbob.txt','r') 
    tweettext = filename.readlines() 
    filename.close()
    
    for lines in tweettext:
        try:
            if(len(lines) > 5):
                api.update_status(lines)
                print("Posted Successfully! : " + lines)
            else:
                continue
        except tweepy.TweepError as e:
            print("You must have already tweeted.")

##############################################################################################################

###############################################################################################################
# CALLING THE FUNCTION
while True:
    post()
    print("Tweet posted!")
    sleep(86400) # 1 DAY
##############################################################################################################

################################################################################################################

# 3RD WAY
# USING MARKOV CHAIN 

# IMPORTING LIBRARIES
import markovgen

# CHOOSING FILE AND NEW FILE
org = open("bbob.txt")
outfile = open("bbob_markov.txt", "w")

# REPEATABLE MARKOV' TEXT GENERATOR
newtext = []
mk = markovgen.Markov(org)

counter = 0
while counter < 10: # CHANGE 10 TO HOWEVER MANY LINES YOU WANT TO GENERATE
    line = '\n' + mk.generate_markov_text()

    # REMOVE PUNCTUATION
    exclude = ['"','(',')',';'] 
    line = ''.join(ch for ch in line if ch not in exclude)

    # MAKE LINE LOWERCASE, ADD PERIOD AT END
    line = line.lower() + "." 
    
    print (line)
    newtext.append(line)
    counter = counter + 1

for aline in newtext:
    outfile.write(aline) # MAKES TEXT FILE LINE BY LINE

outfile.close()
org.close()

#########################################################################################################################

#########################################################################################################################

# 4TH WAY 
# BOT THAT RESPONDS TO TWITTER ACTIVITY

# READING THE FILE THROUGH WHICH IT WILL TWEET
filename = open('bbob.txt', 'r')
tweettext = filename.readlines()
filename.close()

# A FUNCTION THAT PICKS A RANDOM LINE
def linenum():
    inte = randint(0, len(tweettext))
    return inte

# THIS IS THE FUNCTION THAT DOES MOST OF THE WORK OF THE BOT
def runTime():

    # GETTING ALL THE USER FROM OUR TIMELINE AND SELECTING 5 OF THEM
    getuser = api.home_timeline()
    getuser = getuser[:5]
    
    # TWEETING TO THE USERS THAT ARE ON HOME TIMELINE AND REPLYING THEM WITH THE LINE FROM THE FILE AS TWEET
    for i in getuser:
        try:
            statusid = i.id
            username = i.user.screen_name
            digit = linenum()
            line = tweettext[digit]
            m = "@%s" %(username) + " " + line
            api.update_status(m, statusid)
            print("I just replied to: %s" %(username))
        except tweepy.TweepError as e:
            if("186" in e.reason):
                print("Tweet length is more than 140 chars.")
                
###################################################################################################################

##################################################################################################################
                
# RUNS THE MAIN FUNCTION EVERY 1 HOUR
def replybot():
    while True:
        runTime()
    sleep(60) # 1 HR
    replybot()
    
################################################################################################################    
    
#################################################################################################################
