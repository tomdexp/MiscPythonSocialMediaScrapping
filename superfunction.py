from tweeter_scraping import scrapeTwitterPostBySearch, scrapeTwitterPostByUser
from instagram_scraping import scrapeInstagramPostBySearch, scrapeInstagramPostByUser
from youtube_scraping import scrapeYoutubePostBySearch
from csv_to_sql import csvToSqlite

def scrapeMediaPostBySearch(stringSearch, count=5, post_file = "table_post.csv", profile_file = "table_profile.csv"):
    try:
        scrapeTwitterPostBySearch(stringSearch, count, post_file, profile_file)
    except:
        print("Twitter--> Request failed")
    try:
        scrapeYoutubePostBySearch(stringSearch, count, post_file, profile_file)
    except:
        print("Youtube --> Request failed")
    try:
        scrapeInstagramPostBySearch(stringSearch, count, post_file, profile_file)
    except:
        print("Instagram --> Request failed")
    return


# EXAMPLE : scrapeMediaPostBySearch("vacciné", count=50, post_file="vaccin_table_post.csv", profile_file= "vaccin_table_profile.csv")