from fastapi import FastAPI
from scraper import Scraper

app = FastAPI()
scraper = Scraper()

@app.get("/scrape-TED-facebook-page")
async def scrapeFacebookPage():
    try:
        postsCount = scraper.ScrapeFacebookPage()
        return f"Successfully processed {postsCount} posts."
    except Exception as e:
        return({"unexpected exception" : e})

@app.get("/posts")
async def getPosts():
    try:
        return {"posts" : scraper.GetPosts()}
    except Exception as e:
        return({"unexpected exception" : e})