from scraper import Scraper

# dockerEnviroment=False is used for testing and for deploying on local environment
scraper = Scraper(dockerEnviroment=False)
print("testing facebook page scraping ...")
print(f"processed {scraper.ScrapeFacebookPage()} posts")
print(10*'*')
print(scraper.GetPosts())
