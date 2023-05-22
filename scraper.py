import time
from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class DatabaseAccessor():
    database = "localDB"
    collection = "facebookPosts"
    # the mongo client url changes between testing on local machine and on docker
    # thus we add a flag to distinguish between the two modes
    def __init__(self, dockerEnv = True):
        if (dockerEnv):
            self.myclient = MongoClient("mongodb://db:27017")
        else:
            self.myclient = MongoClient("mongodb://localhost:27017")

        db = self.myclient[self.database]
        db[self.collection]

    def insertInCollection(self, dict):
        db = self.myclient[self.database]
        collection = db[self.collection]
        collection.insert_one(dict)

    def listCollections(self):
        return self.myclient.list_database_names()
    
    def findAll(self):
        db = self.myclient[self.database]
        collection = db[self.collection]
        return list(collection.find())

class Scraper():
    def __init__(self, dockerEnviroment = True):
        self.dockerEnviroment = dockerEnviroment

    def connect(self):
        options = Options()
        options.add_argument("--no-sandbox")    
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--ignore-ssl-errors=true")
        options.add_argument("--ignore-certificate-errors")  
        driver = webdriver.Chrome(options=options)
        driver.get("https://mobile.facebook.com/TED")
        print("fetching the facebook page...")
        time.sleep(3)
        print("bypassing popups ...")
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)
        driver.find_element(By.ID, "popup_xout").click()
        time.sleep(3)
        print("bypassed popups ...")
        print("facebook page successfully fetched!")
        return driver

    def GetFacebookPage(self):
        driver = self.connect()
        page = driver.page_source
        driver.quit()
        return page

    def ScrapeFacebookPage(self):
        soup = BeautifulSoup(self.GetFacebookPage(), 'html.parser')
        dbAccessor = DatabaseAccessor(self.dockerEnviroment)
        posts = soup.find_all('article')
        for i in range(len(posts)):
            spanElements = posts[i].find_all('span')
            likesAndComms = [ s for s in spanElements if (s.text != '' and s.text[0].isdigit()) ]
            
            content = []
            for pElement in posts[i].find_all('p'):
                content.append(pElement.text)
            
            if (len(likesAndComms) == 1):
                likes = likesAndComms[0].text.split(" ")[0]
                comments = 0
                shares = 0
            elif (len(likesAndComms) == 2):
                likes = likesAndComms[1].text.split(" ")[0]
                comments = 0
                shares = 0
            elif (len(likesAndComms) == 3):
                likes = likesAndComms[1].text.split(" ")[0]
                comments = likesAndComms[2].text.split(" ")[0]
                shares = 0
            elif (len(likesAndComms) == 4):
                likes = likesAndComms[1].text.split(" ")[0]
                comments = likesAndComms[2].text.split(" ")[0]
                shares = likesAndComms[3].text.split(" ")[0]

            name = spanElements[0].text
            date = posts[i].find('abbr').text

            # create json object
            jsonContent = {
                "Data" : {
                    "name": name,
                    "postContent": content,
                    "likes": likes,
                    "comments": comments,
                    "shares": shares,
                    "asOfDate": date
                }
            }
            dbAccessor.insertInCollection(jsonContent)

        return len(posts)
    
    def GetPosts(self):
        dbAccessor = DatabaseAccessor(self.dockerEnviroment)
        results = dbAccessor.findAll()
        posts = []
        for post in results:
            posts.append(post['Data'])

        return posts