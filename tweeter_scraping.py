import snscrape.modules.twitter as sntwitter
import pandas as pd
import csv
import sys
from tools import normaliseString, removeDuplicatesFromCsv

# [arg] str twitterAt : is the username after the @
# [arg] int count : is the number of Post the function will return
# [out] list[] tweet_list : is a list containing x post's informations
# [out] tweet_object tweet : is a single Post used for scraping the profile
def getTwitterPostByUser(twitterAt, count=5):
    tweet_list = []
    print("Tweeter --> Starting the scraping of {} post(s) from the user @{}".format(count, twitterAt))
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:' + twitterAt).get_items()):
        if i > count - 1:
            break
        tweet_content = normaliseString(tweet.content)
        tweet_list.append([tweet.url, tweet_content, tweet.date, tweet.replyCount, tweet.likeCount, tweet.user.url])
    print("Tweeter --> Successfully scraped {} post(s) from the user @{}".format(len(tweet_list), twitterAt))
    try:
        type(tweet)
    except UnboundLocalError:
        print("An error occurred, the user's @ may not be correct")
        sys.exit(1)
    return tweet_list, tweet


# [arg] tweet_object tweet : is a single Post containing one tweet
# [out] list[] profileInfo : is a list containing the profile's information of the tweet
def getTwitterUserInfo(tweet):
    return [tweet.user.url, tweet.user.followersCount, tweet.user.username,
                   normaliseString(tweet.user.rawDescription)]

# [arg] string twitterAt : is the username after the @
# [out] list[] profileInfo : is a list containing the profile's information of the tweet
def getTwitterUserInfoByUsername(twitterAt):
    i = 1
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:' + twitterAt).get_items()):
        profileInfo = getTwitterUserInfo(tweet)
    return profileInfo

# [arg] list[] profileInfo : is a list containing the profile's information of the tweet
# [out] string file_output : is the name of the csv file that was created/appended
def addTwitterUserInfoToCsv(profileInfo, file_output = "table_profile.csv"):
    profile_df = pd.DataFrame([profileInfo])
    try:
        profile_df.to_csv(file_output, index=False, mode="a", header=False, quoting=csv.QUOTE_ALL, encoding="UTF-8")
    except PermissionError:
        print("Please close the csv file before running the script ! Exiting...")
        sys.exit(1)
    return file_output


# [arg] list[] tweet_list : is a list containing x posts
# [out] string file_output : is the name of the csv file that was created/appended
def addTwitterPostsToCsv(tweet_list, file_output = "table_post.csv"):
    tweets_df = pd.DataFrame(tweet_list)
    try:
        tweets_df.to_csv(file_output, index=False, mode="a", header=False, quoting=csv.QUOTE_ALL, encoding="UTF-8")
    except PermissionError:
        print("Please close the csv file before running the script ! Exiting...")
        sys.exit(1)
    return file_output

# [arg] string twitterAt : is the username after the @
# [arg] integer count : is the number of Post the function will return
def scrapeTwitterPostByUser(twitterAt, count=5, post_file = "table_post.csv", profile_file = "table_profile.csv"):
    tweet_list, tweet = getTwitterPostByUser(twitterAt, count)
    profileInfo = getTwitterUserInfo(tweet)
    file_name_profile = addTwitterUserInfoToCsv(profileInfo, profile_file)
    file_name_post = addTwitterPostsToCsv(tweet_list, post_file)
    removeDuplicatesFromCsv(file_name_profile)
    removeDuplicatesFromCsv(file_name_post)
    return

# [arg] string stringSearch : the string the API will search post for (can use #)
# [arg] integer count : is the number of Post the function will return
# [out] list[] tweet_list : is a list containing x post's informations
# [out] list[] tweetObject_list : is a list containing x tweet's object
def getTwitterPostBySearch(stringSearch, count=5):
    tweet_list = []
    tweetObject_list = []
    print("Tweeter --> Starting the scraping of {} post(s) from the searched string : {}".format(count, stringSearch))
    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(stringSearch).get_items()):
        if i > count - 1:
            break
        tweet_content = normaliseString(tweet.content)
        tweet_list.append([tweet.url, tweet_content, tweet.date, tweet.replyCount, tweet.likeCount, tweet.user.url])
        tweetObject_list.append(tweet)
    print("Tweeter --> Successfully scraped {} post(s) from the searched string : {}".format(len(tweet_list), stringSearch))
    return tweet_list, tweetObject_list

# Main function used to connect each function, this is the one that will be called by the user
# [arg] string stringSearch : the string the API will search post for (can use #)
# [arg] integer count : is the number of Post the function will return
def scrapeTwitterPostBySearch(stringSearch, count=5,post_file = "table_post.csv", profile_file = "table_profile.csv"):
    global file_name_profile
    tweet_list, tweetObject_list = getTwitterPostBySearch(stringSearch, count)
    for tweet in tweetObject_list:
        profileInfo = getTwitterUserInfo(tweet)
        file_name_profile = addTwitterUserInfoToCsv(profileInfo, profile_file)
    file_name_post = addTwitterPostsToCsv(tweet_list, post_file)
    removeDuplicatesFromCsv(file_name_profile)
    removeDuplicatesFromCsv(file_name_post)
    return

# [arg] string csvFileName : the name of the csv file containing the relations
# [out] list[] followed_list : is a list containing usernames
def getUserFromRelationCsv(csvFileName):
    df = pd.read_csv(csvFileName + ".csv", encoding="UTF-8", header=None)
    followed_list = [user for user in df[1]]
    print(followed_list)
    return followed_list

# [arg] string csvFileName : the name of the csv file containing the relations
def scrapeUserFromUserRelationCsv(csvFileName):
    followed_list = getUserFromRelationCsv(csvFileName)
    for followed in followed_list:
        print("{} : starting scraping".format(followed))
        profileInfo = getTwitterUserInfoByUsername(followed)
        addTwitterUserInfoToCsv(profileInfo)
        print("{} : finished scraping".format(followed))
    return

# [arg] list[] tweet_list : is a list containing x posts
# [arg] list[] jsonStructure : is the json structure of the list
# [out] string file_output : is the name of the csv file that was created/appended
def addTwitterProfileToJson(profile_list, jsonStructure, file_output = "table_post"):
    file_output += ".json"
    df = pd.DataFrame(profile_list, columns=jsonStructure)
    try:
        df.to_json(file_output, orient="records", mode="a")
    except PermissionError:
        print("Please close the json file before running the script ! Exiting...")
        sys.exit(1)
    return file_output

# EXAMPLE : scrapeTwitterPostBySearch("vaccin", count=10)
# EXAMPLE : scrapeTwitterPostByUser("elonmusk", count=50)
