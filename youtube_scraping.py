from youtubesearchpython import VideosSearch, ChannelsSearch, ResultMode
from tools import normaliseString, getIdFromUrlYoutube, getUrlFromIdYoutube,getChannelUrlFromId, isYoutubeUrlValid, removeDuplicatesFromCsv, getIdFromChannelUrlYoutube
import sys
import csv
import pandas as pd
import math
from googleapiclient.discovery import build

apiKey = "ENTER GOOGLE API KEY HERE"
post_structure = "post_ID,postUrl,postText,pubDate,commentCount,likeCount,profileUrl"


# Take a list of youtube urls and return a list of info for the post
def getYoutubePostsByUrls(url_list):
    youtube = build('youtube', 'v3', developerKey=apiKey)
    post_info_list = []
    url_list = isYoutubeUrlValid(url_list)
    ids = [getIdFromUrlYoutube(url) for url in url_list]
    results = youtube.videos().list(id=ids, part=['snippet','statistics']).execute()
    for result in results.get('items', []):
        id = result['id']
        channelId = result['snippet']['channelId']
        postUrl = getUrlFromIdYoutube(id)
        postText = normaliseString(result['snippet']['title'])
        postText += " "  + normaliseString(result['snippet']['description'])
        pubDate = result['snippet']['publishedAt']
        profileUrl = getChannelUrlFromId(channelId)
        try:
            commentCount = result['statistics']['commentCount']
        except KeyError:
            commentCount = None
            print("Youtube --> Comments are disabled on {}, commentCount set to None".format(postUrl))
        try:
            likeCount = result['statistics']['likeCount']
        except KeyError:
            likeCount = None
            print("Youtube --> Likes are disabled on {}, likeCount set to None".format(postUrl))
        post_info_list.append([postUrl, postText, pubDate, commentCount, likeCount, profileUrl])
    return post_info_list

# Take a keyword and a integer as an argument, is used to search the results by keywords
# return a list of posts'url
def getYoutubePostUrlBySearch(stringSearch, count="5"):
    post_url_list = []
    print("Youtube --> Starting the scraping of {} post(s) from the searched string : {}".format(count, stringSearch))
    videosSearch = VideosSearch(stringSearch, limit = count)
    result = videosSearch.result()
    n_pages = math.ceil(count/20)
    if n_pages == 1:
        print("Youtube --> There is {} page of result".format(n_pages))
    else:
        print("Youtube --> There are {} page(s) of result".format(n_pages))
    for n in range(n_pages):
        for i in range(len(result["result"])):
            if len(post_url_list)<count:
                url = result["result"][i]["link"]
                post_url_list.append(url)
        if n_pages>1:
            print("Youtube --> Scraping page number ({})".format(n+1))
            videosSearch.next()
    print("Youtube --> Successfully scraped {} post(s) from the searched string : {}".format(len(post_url_list), stringSearch))
    return post_url_list

# [arg] list[] tweet_list : is a list containing x posts
# [out] string file_output : is the name of the csv file that was created/appended
def addYoutubePostsToCsv(post_list,file_output = "table_post.csv"):
    tweets_df = pd.DataFrame(post_list)
    try:
        tweets_df.to_csv(file_output, index=False, mode="a", header=False, quoting=csv.QUOTE_ALL, encoding="UTF-8")
    except PermissionError:
        print("Please close the csv file before running the script ! Exiting...")
        sys.exit(1)
    return file_output

# Main function that uses all of the other functions to search youtube by keyword and add the result to two csv
def scrapeYoutubePostBySearch(stringSearch, count="5", post_file = "table_post.csv",profile_file="table_profile.csv"):
    # google-api limit is at 50
    if count>50:
        count = 50
        print("Youtube --> Google-api is limited to 50 request")
    post_url_list = getYoutubePostUrlBySearch(stringSearch, count)
    post_info_list = getYoutubePostsByUrls(post_url_list)
    profile_file_output = addYoutubeUserInfoListToCsv(post_info_list,profile_file)
    post_file_output = addYoutubePostsToCsv(post_info_list,post_file)
    removeDuplicatesFromCsv(post_file_output)
    removeDuplicatesFromCsv(profile_file_output)
    return

# [arg] list[] tweet_list : is a list containing x profile
# [out] string file_output : is the name of the csv file that was created/appended
def addYoutubeUserInfoListToCsv(post_info_list, profile_file="table_profile.csv"):
    for post in post_info_list:
        id = getIdFromChannelUrlYoutube(post[-1])
        profileInfo = getYoutubeProfileById(id)
        if profileInfo is not None:
            file_output = addYoutubeUserInfoToCsv(profileInfo, profile_file)
    return file_output

# Take a youtube ID and return the channel's info
def getYoutubeProfileById(id):
    channelsSearch = ChannelsSearch(id, limit=1)
    try:
        dict = channelsSearch.result()["result"][0]
    except IndexError:
        return None
    try:
        desc = dict["descriptionSnippet"][0]["text"]
        desc = normaliseString(desc)
    except TypeError:
        desc = None
    return [dict["link"],stringNumToInt(dict["subscribers"]),normaliseString(dict["title"]),desc]

# [arg] list[] profileInfo : is a list containing the profile's information of the tweet
# [out] string file_output : is the name of the csv file that was created/appended
def addYoutubeUserInfoToCsv(profileInfo, file_output = "table_profile.csv"):
    profile_df = pd.DataFrame([profileInfo])
    try:
        profile_df.to_csv(file_output, index=False, mode="a", header=False, quoting=csv.QUOTE_ALL, encoding="UTF-8")
    except PermissionError:
        print("Please close the csv file before running the script ! Exiting...")
        sys.exit(1)
    return file_output

# Convert subscribers number in string to real int ( 1.06M => 1060000)
# [arg] string stringNumber : a string with those formats : 1.51K OR 60M
# [out] int : an integer corresponding to the argument
def stringNumToInt(stringNumber):
    if stringNumber is None:
        return None
    number = stringNumber.split(" ")[0]
    left_part = number.split(".")[0]
    try:
        right_part = number.split(".")[1]
    except IndexError:
        right_part = ""
    if "K" in right_part or "K" in left_part:
        right_part = right_part.translate({ord('K'): None})
        left_part = left_part.translate({ord('K'): None})
        zeros = 3 - len(right_part)
        right_part += right_part.join("0")*zeros
    elif "M" in right_part or "M" in left_part:
        right_part = right_part.translate({ord('M'): None})
        left_part = left_part.translate({ord('M'): None})
        zeros = 6 - len(right_part)
        right_part += right_part.join("0") * zeros
    return int(left_part+right_part)


profile_structure = "profile_ID,profileUrl,subCount,userName,profileDesc"

# EXAMPLE : scrapeYoutubePostBySearch("bitcoin",count=150)
