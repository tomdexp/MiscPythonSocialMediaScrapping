from selenium import webdriver
import time
import csv
import io
from datetime import datetime
import regex

def scrapeInstagramPostByUrl(url):
    return


driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://www.instagram.com/p/CO-lvzcsXG2/")
driver.implicitly_wait(5)

time.sleep(4)
#accept cookies
try:
    driver.find_element_by_xpath("//div[@class='aOOlW  bIiDR']")
    driver.click
except:
    pass
try:
    close_button = driver.find_element_by_class_name('xqRnw')
    close_button.click()
except:
    pass

try:
    load_more_comment = driver.find_element_by_css_selector('.MGdpg > button:nth-child(1)')
    print("Found {}".format(str(load_more_comment)))
    i = 0
    while load_more_comment.is_displayed() and i < int(100):
        driver.execute_script("arguments[0].click();", load_more_comment)
        time.sleep(1.5)
        load_more_comment = driver.find_element_by_css_selector('.MGdpg > button:nth-child(1)')
        print("Found {}".format(str(load_more_comment)))
        i += 1
except Exception as e:
    print(e)
    pass


user_names = []
user_comments = []
comment = driver.find_elements_by_class_name('gElp9 ')
for c in comment:
    container = c.find_element_by_class_name('C4VMK')
    name = container.find_element_by_class_name('_6lAjh').text
    content = container.find_element_by_tag_name('span').text
    content = content.replace('\n', ' ').strip().rstrip()
    user_names.append(name)
    user_comments.append(content)

user_names.pop(0)
user_comments.pop(0)

comment_count = 0
for i in range(len(user_names)):
    print(user_names[i], " : ", user_comments[i])
    comment_count += 1
print("{} comments have been scraped.".format(comment_count))

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)
title_date = regex.sub('[^A-Za-z0-9]+', '', dt_string)


with io.open('comments_insta'+ title_date + '.csv', 'w', newline='', encoding="utf-16") as file:
    writer = csv.writer(file, delimiter=",", quoting=csv.QUOTE_ALL)
    writer.writerow(["Username", "Comment", "Extraction_datetime"])
    for username, comment in zip(user_names, user_comments):
        writer.writerow([username, comment, dt_string])

driver.close()