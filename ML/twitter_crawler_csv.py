# -*- coding: utf-8 -*-  

''''' 
Created on 2018-2-23 
@author: Jackustc
'''  
import tweepy 
import csv
import datetime 

consumer_key= 'pUAVjeYT1HSv27OZQm6iIjUKB' # add your own key
consumer_secret ='lV61CW17tSs4zWiyXqMxEMGOYH7FVDoHvttynkEdardI5Q579y' # add your own secret
access_token = '899020336817164288-mWTulcxqNTfTgsb5xBfAgNOBpaDA99I' # add your own access_token
access_token_secret = 'YjxdGtZKiWco0xV2LPuSsE1MJZFblgOcEVevcNDGG2ruT' # add your own access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  # create auth 
auth.set_access_token(access_token,access_token_secret) #set access_token and access_token_secret

api = tweepy.API(auth)

# keywords search 

#print('please input your search keywords:')
#query = input()

query = 'Florida Shooting' # change your own search query
language = 'en'
results = api.search(q=query,language=language,count=1)
Screen_name=['Screen_name']
Text = ['Text']
id = ['id']
Created_time = ['Created_time']
#print(type(Created_time))
replyToSID = ['replyToSID']
replyToUID = ['replyToUID']
replytoSN = ['replytoSN']
truncated = ['truncated']
retweeted = ['retweeted']
retweetedcount = ['retweetedcount']
coordinates = ['coordinates']
user_location = ['user_location']
Favorited = ['Favorited']
FavoriteCount = ['FavoriteCount']
statusSource = ['statusSource']
isRetweet = ['isRetweet']
for tweet in results:
    #print(type(tweet.created_at))
    #print(tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    #print('Screen_name: '+tweet.user.screen_name)
    Screen_name. append(tweet.user.screen_name)
    #print('Text: ' + tweet.text)
    Text.append(tweet.text)
    #print('Created_time: ',tweet.created_at)
    Created_time.append(tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    replyToSID.append(tweet.in_reply_to_status_id)
    replyToUID.append(tweet.in_reply_to_user_id)
    replytoSN.append(tweet.in_reply_to_screen_name)
    id.append(tweet.id)
    truncated.append(tweet.truncated)
    retweeted.append(tweet.retweeted)
    retweetedcount.append(tweet.retweet_count)
    coordinates.append(tweet.coordinates)
    user_location.append(tweet.user.location)
    FavoriteCount.append(tweet.favorite_count)
    Favorited.append(tweet.favorited)
    statusSource.append(tweet.source)
    if tweet.in_reply_to_user_id is None: isr = 'New tweet'
    else: isr = 'retweet'
    isRetweet.append(isr)
    '''
    print('replyToSID: ',tweet.in_reply_to_status_id)
    print('replyToUID: ',tweet.in_reply_to_user_id)
    print('replytoSN: ',tweet.in_reply_to_screen_name)
    print('id: ', tweet.id)
    print('truncated: ',tweet.truncated) 
    print('retweeted: ', tweet.retweeted) 
    print('retweetedcount: ',tweet.retweet_count)
    print('coordinates: ',tweet.coordinates) 
    print('user_location: ',tweet.user.location)
    print('Favorited: ',tweet.favorited)
    print('FavoriteCount: ', tweet.favorite_count)
    print('statusSource: ',tweet.source)
    
    print('\n\n')'''
    #print(Screen_name)
with open('twitter_news.csv','wt',encoding='utf-8',newline='') as f:
    f_w = csv.writer(f)
    for i in range(len(id)):
        row = [Screen_name[i],str(id[i]),Created_time[i],str(replyToSID[i]),str(replyToUID[i]),str(replytoSN[i]),str(retweeted[i]),str(retweetedcount[i]),str(truncated[i]),str(coordinates[i]),str(user_location[i]),str(isRetweet[i]),str(Favorited[i]),str(FavoriteCount[i]),str(Text[i])]
        print(row)
        f_w.writerow(row)
        #f_w.writerow('\n')
