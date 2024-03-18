# Importing relevant libraries
from getpass import getpass
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json
from .helpers.utils import detect_language
# from msedge.selenium_tools import Edge, EdgeOptions


edge_driver_path = "C:/Users/rahul/Downloads/edgedriver_win32/msedgedriver.exe"
service = Service(executable_path=edge_driver_path)

driver = webdriver.Edge(service=service)


# Class for Twitter Scrapper

class ScrapeTwitter():

    URL = "https://www.twitter.com"
    
    
    def __init__(self, credentials, query):
        self.credentials = credentials
        self.query = query
        
    
    def login(self):
        # print(self.URL)
        driver.get(self.URL + "/login")
        sleep(10)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='text']")))
        username = driver.find_element(By.XPATH, "//input[@name='text']")
        username.send_keys(self.credentials[0])
        username.send_keys(Keys.RETURN)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='password']")))
        password = driver.find_element(By.XPATH, "//input[@name='password']")
        password.send_keys(self.credentials[1])
        password.send_keys(Keys.RETURN)

        try:
            login_success = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//div[@data-testid="SideNav_AccountSwitcher_Button"]')))
            return {"status": "success"} if login_success else {"status": "fail"}
        except TimeoutException:
            return {"status":"TimedOut"}

    def searchTwitter(self, number_tweets=5):
        # URL to Twitter's search page
        twitter_search_url = self.URL + '/search?q='
        
        # Navigate to Twitter's search page with the current prompt
        driver.get(twitter_search_url + self.query)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Latest"))).click()
        
        tweets_data = []
        count = 0
        while len(tweets_data) < number_tweets:

            current_cards = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//div/article[@data-testid="tweet"]')))            
            
            for card in current_cards[len(tweets_data):]:
                try:
                    username = card.find_element(By.XPATH, './/div[@data-testid="User-Name"]//span').text
                    twitter_handle = card.find_element(By.XPATH, './/div[@data-testid="User-Name"]/div[2]//span').text
                    tweets_web = card.find_elements(By.XPATH, './/div[@data-testid="tweetText"]/span')
                    tweets_str = [i.text for i in tweets_web]
                    tweet_text = " ".join(tweets_str)
                    language = detect_language(tweet_text)
                    try:
                        replies = card.find_element(By.XPATH, './/div[@data-testid="reply"]//span[@data-testid="app-text-transition-container"]/span/span').text
                        if not replies:
                            replies = 0
                    except NoSuchElementException:
                        replies = 0
                    try:
                        retweets = card.find_element(By.XPATH, './/div[@data-testid="retweet"]//span[@data-testid="app-text-transition-container"]/span').text
                        if not retweets:
                            retweets = 0                    
                    except NoSuchElementException:
                        retweets = 0
                    try:
                        likes = card.find_element(By.XPATH, './/div[@data-testid="like"]//span[@data-testid="app-text-transition-container"]/span').text
                        if not likes:
                            likes = 0
                    except NoSuchElementException:
                        likes = 0
                    
                    tweet_data = {
                        "count" : count,
                        "username" : username,
                        "twitterhandle" : twitter_handle,
                        "tweettext" : " ".join(tweet_text),
                        "language":language,
                        "replies": replies,
                        "retweets" : retweets,
                        "likes" : likes                
                    }
                    count += 1
                    tweets_data.append(tweet_data)

                    if len(tweets_data) >= number_tweets:
                        break

                except NoSuchElementException as e1:
                    print(e1)
                    continue
                except StaleElementReferenceException as e2:
                    print(e2)
                    continue
                
                try:
                    if len(tweets_data) < number_tweets:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        WebDriverWait(driver, 30).until(lambda d: len(d.find_elements(By.XPATH, '//div/article[@data-testid="tweet"]')) > len(current_cards))
                except TimeoutException as e:
                    print("No More Tweets Loaded...")
               
        return json.dumps(tweets_data, indent=4)



    