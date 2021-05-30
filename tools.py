import unidecode
import pandas as pd
import sys


# [arg] string string : the string you want to normalise
# [out] string string_result : the normalised string
def normaliseString(string):
    if string is None:
        return None
    string_result = string.splitlines()
    string_result = ' '.join(string_result)
    string_result = string_result.replace("’", "")
    string_result = string_result.replace("'", "")
    string_result = string_result.replace("&", "")
    string_result = string_result.replace(",", " ")
    string_result = string_result.replace('"', "")
    string_result = string_result.replace("“", "")
    string_result = unidecode.unidecode(string_result)
    return string_result


# [arg] string file_name : the name of the csv file
def removeDuplicatesFromCsv(file_name):
    data = pd.read_csv(file_name, header=None, encoding="UTF-8")
    data.drop_duplicates(subset=[0], keep="last", inplace=True, ignore_index=True)
    try:
        data.to_csv(file_name, index=False, header=False, encoding="UTF-8")
    except PermissionError:
        print("Please close the csv file before running the script ! Exiting...")
        sys.exit(1)
    return

# [arg] string file_name : the name of the csv file
def removeDuplicatesFromCsvOnSecondColumn(file_name):
    data = pd.read_csv(file_name, header=None, encoding="UTF-8")
    data.drop_duplicates(subset=[1], keep="last", inplace=True, ignore_index=True)
    try:
        data.to_csv(file_name, index=False, header=False, encoding="UTF-8")
    except PermissionError:
        print("Please close the csv file before running the script ! Exiting...")
        sys.exit(1)
    return


def getIdFromUrlYoutube(url):
    return url.split("=")[1]

def getIdFromChannelUrlYoutube(url):
    return url.split("/")[-1]


def getUrlFromIdYoutube(id):
    return "https://www.youtube.com/watch?v=" + id


def getChannelUrlFromId(channelId):
    return "https://www.youtube.com/channel/" + channelId


def isYoutubeUrlValid(url_list):
    return [url for url in url_list if "https://www.youtube.com/watch?v=" in url]

