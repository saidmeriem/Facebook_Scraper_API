# Facebook_Scraper_API

## Description
 This application based on selenium, beautifulSoup and mongodb allows the scraping of a specific public facebook page and storing all the posts as json in the database.
 It handles only one TED facebook page, as a proof of concept, more pages are yet to come.
 Asides from the code we have a dockerFile allowing the creation of two containers for the scraping service and the mongo database.

## Workflow
The API works in 2 stages :
- The scraping stage: We call the fastapi get method wich in turn will initiate the scraping process.
First the selenium driver is created to bypass the popups and return the html page to be parsed.
Once we get the html page we pass it as input to beautiful soup wich will extract all the useful data per 
post such as the name, content, number of likes, comments and shares. 
Each Json is then stored in mongodb
- The fetching stage: We expose another method in fastapi for getting the posts from the database.

## How to use
 Once downloaded the project run docker-compose up -d, it will create and run the two containers

