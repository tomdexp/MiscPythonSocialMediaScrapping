import csv
import io
from selenium import webdriver
from selenium.common import exceptions
import time
import regex
from datetime import datetime

def scrape(url):
    """
    Extracts the comments from the Youtube video given by the URL.

    Args:
        url (str): The URL to the Youtube video

    Raises:
        selenium.common.exceptions.NoSuchElementException:
        When certain elements to look for cannot be found
    """

    # Note: Download and replace argument with path to the driver executable.
    # Simply download the executable and move it into the webdrivers folder.
    driver = webdriver.Chrome("/Users/X360 1030 G2/chromedriver.exe")

    # Navigates to the URL, maximizes the current window, and
    # then suspends execution for (at least) 5 seconds (this
    # gives time for the page to load).
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(5)
    driver.find_element_by_xpath("//div[@class='VfPpkd-Jh9lGc']").click()
    time.sleep(5)

    try:
        # Extract the elements storing the video title and
        # comment section.
        title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
        comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
    except exceptions.NoSuchElementException:
        # Note: Youtube may have changed their HTML layouts for
        # videos, so raise an error for sanity sake in case the
        # elements provided cannot be found anymore.
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    # Scroll into view the comment section, then allow some time
    # for everything to be loaded as necessary.
    driver.execute_script("arguments[0].scrollIntoView();", comment_section)
    time.sleep(7)

    # Scroll all the way down to the bottom in order to get all the
    # elements loaded (since Youtube dynamically loads them).
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # Scroll down 'til "next load".
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load everything thus far.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # One last scroll just in case.
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    try:
        # Extract the elements storing the usernames and comments.
        username_elems = driver.find_elements_by_xpath('//*[@id="author-text"]')
        comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
        like_elems = driver.find_elements_by_xpath('//*[@id="vote-count-middle"]')
        date_elems = driver.find_elements_by_xpath('//*[contains(@Class,"published-time-text above-comment style-scope ytd-comment-renderer")]')
    except exceptions.NoSuchElementException:
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    print("> VIDEO TITLE: " + title + "\n")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    print("creating file => ",'comments_' + regex.sub('[^A-Za-z0-9]+', '', title) + '.csv')

    with io.open('comments_' + regex.sub('[^A-Za-z0-9]+', '', title) + '.csv', 'w', newline='', encoding="utf-16") as file:
        writer = csv.writer(file, delimiter =",", quoting=csv.QUOTE_ALL)
        writer.writerow(["Username", "Comment", "Likes", "Date", "Extraction_datetime"])
        for username, comment, like, date in zip(username_elems, comment_elems, like_elems, date_elems):
            writer.writerow([username.text, comment.text, like.text, date.text, dt_string])

    driver.close()

# scrape(url="https://www.youtube.com/watch?v=wR9DRl9kl-o")
# scrape(url="https://www.youtube.com/watch?v=vQ7WY_gerls")
# scrape(url="https://www.youtube.com/watch?v=dp--UxiBMN4")
# scrape(url="https://www.youtube.com/watch?v=8hElr5lCkG4")
scrape(url="https://www.youtube.com/watch?v=wTbw7Zjg5mM&")