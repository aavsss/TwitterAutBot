import tweepy
import time

print("Twitter bot")

CONSUMER_KEY = '*'
CONSUMER_SECRET = '*'
ACCESS_KEY = '*'
ACCESS_SECRET = '*'

#OAuth
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

#Redirect user to Twitter to authorize
#redirect_iser(auth.get_authorization_url())
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)

#Get access token
#auth.get_access_token("verifier_value")

#Construct the API instance
api = tweepy.API(auth)

#Pagination
#Iterate through all of the authenticated user's friends
for friend in tweepy.Cursor(api.friends).items():
        #Process the friend here
        process_friend(friend)

#Iterate through the first 10 statuses in the friends timeline
for status in tweepy.Cursor(api.friends_timeline).items(10):
        #Process the status here
        process_status(status)

#Download home timeline tweets and print each one of the texts
public_tweets = api.home_timeline()
for tweet in public_tweets:
        print (tweet.text)

# Get the User object for twitter...
user = api.get_user('aavsss')
print (user.screen_name)
print (user.followers_count)
for friend in user.friends():
        print (friend.screen_name)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
        print('retrieving and replying to tweets...')
        last_seen_id = retrieve_last_seen_id(FILE_NAME)
        mentions = api.mentions_timeline(last_seen_id, tweet_mode = 'extended')

        for mention in reversed(mentions):
                print(str(mention.id)+' - ' + mention.full_text)
                last_seen_id = mention.id
                store_last_seen_id(last_seen_id, FILE_NAME)
                if '#born' in mention.full_text.lower():
                        print('It is #born')
                        print('responding back...')
                        api.update_status('@' + mention.user.screen_name + ' Im #born!', mention.id)

while True:
        reply_to_tweets()
        time.sleep(2)
