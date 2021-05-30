# import the module
import tweepy
import sys
import pandas as pd
from tools import removeDuplicatesFromCsvOnSecondColumn

# assign the values accordingly
consumer_key = "ENTER YOUR CONSUMER KEY HERE"
consumer_secret = "ENTER YOUR CONSUMER SECRET HERE"
access_token = "ENTER YOUR ACCESS TOKEN HERE"
access_token_secret = "ENTER YOUR ACCESS TOKEN SECRET HERE"


# def addFriendListToCsv(user_friend_list):
#     file_output = "twitter_user_friend_list.csv"
#     tweets_df = pd.DataFrame([user_friend_list])
#     try:
#         tweets_df.to_csv(file_output, index=False, mode="a", header=False, quoting=csv.QUOTE_ALL, encoding="UTF-8")
#     except PermissionError:
#         print("Please close the csv file before running the script ! Exiting...")
#         sys.exit(1)
#     return file_output

# [arg] string twitterAt : is the username after the @
# [arg] list[] friend_list : a list containing twitterAt that are followed by the first twitterAt arg
# [out] string file_output : the name of the file that was appended/created
def addTwitterRelationToCsv(twitterAt, friend_list, file_output = "table_relation.csv"):
    relations_list = []
    twitterAt = "https://twitter.com/" + twitterAt
    for friend in friend_list:
        friend = "https://twitter.com/" + friend
        relations_list.append([twitterAt,friend])
    relation_df = pd.DataFrame(relations_list)
    try:
        relation_df.to_csv(file_output, index=False, mode="a", header=False, encoding="UTF-8")
    except PermissionError:
        print("Please close the csv file before running the script ! Exiting...")
        sys.exit(1)
    return file_output

# [arg] string twitterAt : is the username after the @
# [out] string twitterAt : is the username after the @
# [out] list[] friend_list : a list containing twitterAt that are followed by the first twitterAt arg
def getTwitterUserFriendList(twitterAt):
    friend_list = []
    i = 0
    consumer_key = "ENTER YOUR CONSUMER KEY HERE"
    consumer_secret = "ENTER YOUR CONSUMER SECRET HERE"
    access_token = "ENTER YOUR ACCESS TOKEN HERE"
    access_token_secret = "ENTER YOUR ACCESS TOKEN SECRET HERE"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    cursor = tweepy.Cursor(api.friends, twitterAt)
    c_list = cursor.items()
    for friend in c_list:
        friend_list.append(friend.screen_name)
        # print(friend.screen_name)
    print("{} has {} friends".format(twitterAt, len(friend_list)))
    return twitterAt, friend_list

# [arg] string twitterAt : is the username after the @
def scrapeAllUserFollowingList(twitterAt, relation_file = "table_relation.csv"):
    twitterAt, friend_list = getTwitterUserFriendList(twitterAt)
    file_output = addTwitterRelationToCsv(twitterAt, friend_list, relation_file)
    removeDuplicatesFromCsvOnSecondColumn(file_output)
    return

# EXAMPLE : scrapeAllUserFollowingList("Motvallsliberal",relation_file="vaccin_table_relation.csv")