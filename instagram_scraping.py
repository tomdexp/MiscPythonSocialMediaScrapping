from igramscraper.instagram import Instagram
from tools import normaliseString, removeDuplicatesFromCsv
import pandas as pd
import sys
import csv
import random
from myigbot import MyIGBot
from instascrape import *


post_structure = "post_ID,postUrl,postText,pubDate,commentCount,likeCount,profileUrl"


# [arg] string url : the url of an Instagram Post
# [out] list[] postInfo : a list of the Instagram Post information
def getInstagramPostByPostObject(postObject):
    postUrl = postObject.link
    instagram = Instagram()
    media = instagram.get_media_by_url(postUrl)
    postText = media.caption
    pubDate = media.created_time
    commentCount = media.comments_count
    likeCount = media.likes_count
    account = media.owner
    username = account.username
    profileUrl = "https://www.instagram.com/"+ username + "/"
    return [
        postUrl,
        normaliseString(postText),
        pubDate,
        commentCount,
        likeCount,
        profileUrl,
    ]

profile_structure = "profile_ID,profileUrl,subCount,userName,profileDesc"

# [arg] string userName : the username after the @
# [out] list[] profileInfo : is a list containing the profile's information of the post
def getInstagramProfileByUsername(userName):
    instagram = Instagram()
    account = instagram.get_account(userName)
    profileUrl = "https://www.instagram.com/" + userName + "/"
    subCount = account.followed_by_count
    profileDesc = account.biography
    profileDesc = normaliseString(profileDesc)
    return [profileUrl,subCount,userName,profileDesc]

# [arg] string userName : the username after the @
# [arg] integer count : the number of Post the function will return
# [out] list[] post_list : is a list containing x post's informations
def getInstagramPostsObjectByUser(userName, count=5):
    instagram = Instagram()
    medias = instagram.get_medias(userName, count)
    print("Instagram user : {} - starting the scraping of {} post's urls".format(userName, count))
    post_list = [media for media in medias]
    print("Instagram user : {} - successfully scraped {} post's url(s)".format(userName, len(post_list)))
    return post_list


# [arg] string userName : the username after the @
# [arg] integer count : the number of Post the function will return
def scrapeInstagramPostByUser(userName, count=5, post_file = "table_post.csv", profile_file = "table_profile.csv"):
    post_list = getInstagramPostsObjectByUser(userName, count)
    post_info_list = []
    for post in post_list:
        time.sleep(random.randrange(1,3))
        post_info_list.append(getInstagramPostByPostObject(post))
    profileInfo = getInstagramProfileByUsername(userName)
    file_name_post = addInstagramPostsToCsv(post_info_list, post_file)
    file_name_profile = addInstagramUserInfoToCsv(profileInfo, profile_file)
    removeDuplicatesFromCsv(file_name_profile)
    removeDuplicatesFromCsv(file_name_post)
    return

# [arg] list[] post_info_list : a list containing info on x posts
# [out] string file_output : is the name of the csv file that was created/appended
def addInstagramPostsToCsv(post_info_list, file_output = "table_post.csv"):
    insta_post_df = pd.DataFrame(post_info_list)
    try:
        insta_post_df.to_csv(file_output, index=False, mode="a", header=False, quoting=csv.QUOTE_ALL, encoding="UTF-8")
    except PermissionError:
        print("Please close the csv file before running the script ! Exiting...")
        sys.exit(1)
    return file_output

# [arg] list[] profileInfo : is a list containing the profile's information of the tweet
# [out] string file_output : is the name of the csv file that was created/appended
def addInstagramUserInfoToCsv(profileInfo, file_output = "table_profile.csv"):
    profile_df = pd.DataFrame([profileInfo])
    try:
        profile_df.to_csv(file_output, index=False, mode="a", header=False, quoting=csv.QUOTE_ALL, encoding="UTF-8")
    except PermissionError:
        print("Please close the csv file before running the script ! Exiting...")
        sys.exit(1)
    return file_output

def getInstagramPostUrlsBySearch(stringSearch, count=5, email="ENTER INSTAGRAM EMAIL ACCOUNT HERE", password="ENTER INSTAGRAM PASSWORD HERE"):
    stringSearch = stringSearchToTag(stringSearch)
    bot = MyIGBot(email,password)
    response = bot.hashtag_posts(stringSearch, limit=count)
    while response is None:
        response = bot.hashtag_posts(stringSearch, limit=count)
    return [url for url in response]

    # instagram = Instagram()
    # instagram.with_credentials(email, password)
    # instagram.login()
    # medias = instagram.get_medias_by_tag(stringSearch, count=count)
    # print([type(str(media)) for media in medias])
    # return [str(media.link) for media in medias]

def scrapeInstagramPostBySearch(stringSearch, count=5, post_file = "table_post.csv", profile_file="table_profile.csv"):
    post_list = getInstagramPostUrlsBySearch(stringSearch, count=count)
    post_info_list = []
    post_list = [getInstagramPostObjectByUrl(post) for post in post_list]
    print("Instagram --> Starting the scraping of {} post(s) from the searched string : {}".format(count, stringSearch))
    for post in post_list:
        time.sleep(random.randrange(3,7))
        post_info_list.append(getInstagramPostByPostObject(post))
        print("Instagram --> {} post scraped".format(len(post_info_list)))
    print("Instagram --> Successfully scraped {} post(s) from the searched string : {}".format(len(post_info_list), stringSearch))
    file_name_post = addInstagramPostsToCsv(post_info_list, post_file)
    file_name_profile = addInstagramUserInfoListToCsv(post_info_list, profile_file)
    removeDuplicatesFromCsv(file_name_post)
    removeDuplicatesFromCsv(file_name_profile)
    return

def getInstagramPostObjectByUrl(url):
    instagram = Instagram()
    return instagram.get_media_by_url(url)

def getUserNameByPost(post):
    return post[-1].split("/")[-2]

def addInstagramUserInfoListToCsv(post_info_list, profile_file = "table_profile.csv"):
    for post in post_info_list:
        userName = getUserNameByPost(post)
        profileInfo = getInstagramProfileByUsername(userName)
        file_output = addInstagramUserInfoToCsv(profileInfo, profile_file)
    return file_output

def stringSearchToTag(stringSearch):
    return stringSearch.replace(" ", "")

# EXAMPLE : scrapeInstagramPostBySearch("vaccin", count=50,post_file="table_post.csv",profile_file="table_profile.csv")