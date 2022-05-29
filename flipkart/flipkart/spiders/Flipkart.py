from contextlib import nullcontext
from turtle import title
import scrapy
import json
import time
import json
#import cfscrape
#from fake_useragent import UserAgent
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlencode
from urllib.parse import urljoin
from scrapy import signals
from pydispatch import dispatcher
import pandas as pd

df = pd.read_csv('C:/Users/Asus/OneDrive/Desktop/crawler/postscrape/postscrape/spiders/Book1.csv')

w2 = 2                    #no of pages

w3 =  'price_asc'      # 'popularity', 'price_asc' , 'price_desc' , 'recency_desc','relevance'

item = df['Name'].tolist()
starturl =[]

for w1 in item:                                                     
   starturl.append(f'https://www.flipkart.com/search?q={w1}&sort={w3}')


# w1 = input("Enter your item: ")
# starturl.append(f'https://www.flipkart.com/search?q={w1}')   //  Comment line 20-22 and comment out line 24-25 to get input realtime rather than uploading csv file

# API = '17a5880c2d8754577f3991c405ad5b5a'

# def get_url(url):
#     payload = {'api_key': API, 'url': url}
#     proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)    #comment line 46-47 and comment out 29-32 and 44-45 if serval request has to made as it will avoid blockage of spider 
#     return proxy_url

class QuotesSpider(scrapy.Spider):
    name = "flipkart"
    # *** Change this url for your prefered search from hemnet.se ***
    start_urls = starturl
    print(start_urls)
    globalIndex = 0
    results = {}

    def start_requests(self):
        for url in self.start_urls:
            # yield scrapy.Request(url=get_url(url), dont_filter=True, meta={'start_url': url},callback=self.parse,
            # method="GET")
            yield scrapy.Request(url, dont_filter=True, meta={'start_url': url},callback=self.parse,
            method="GET")
    
    def parse(self, response):
        for ad in response.css("div._2B099V "):   
            description  = ad.css("  a.IRpwTa::text ").get()
            title = ad.css(" div._2WkVRV::text").get()

                
            prices = ad.css(" a._3bPFwb > div._25b18c > div._30jeq3::text").get()
            if prices != None:
                    prices = prices.replace('\u20b9', '')

            original_price = ad.css(" a._3bPFwb > div._25b18c > div._3I9_wc::text")[1].get()
            if original_price != None:
                    original_price = original_price.replace('\u20b9', '')
                
            Free_delivery = ad.css(" a._3bPFwb > div._3tcB5a _2AaDRY > div._2Tpdn3::text").get()
            # review = ad.css("div.a-spacing-top-micro > div.a-row  > span::attr(aria-label)").get()

            # No_of_review = ad.css("div.a-spacing-top-micro > div.a-row  > span > a.a-link-normal > span.a-size-base::text").get()

            id = ad.css("a.IRpwTa::attr(href)").get()

                
            start = id.find('pid=') +4
            end = id.find('&lid=')

            if description == None :
                   description = id[1:start - 26]
            id = id[start:end]
                

            # if len(id) == 10:
            #         sponsered = 0
            # else :
            #         sponsered = 1

            f_Assured = ad.css("div._1a8UBa> img::attr(src)").get()
            if f_Assured != None :
                f_Assured='f_Assured'

            Special_Offer = ad.css("div._2ZdXDB > div._3xFhiH > div._2Tpdn3::text").get()
                
           
            
                
                
            start_url = response.meta['start_url']
            start1 = start_url.find('?q=') + 3
            end1 = start_url.find('&sort') 
            category = start_url[start1:end1]
                
            yield {
            'category' : category,
            'Brand': title,
            'title': description,
            'price': prices,
            'original-price' : original_price,
            # 'review' : review ,
            # 'No_of_review' : No_of_review,  
            'id' : id,
            # 'sponsered' : sponsered,
            'f-Assured' : f_Assured,
            'Free delivery' : Free_delivery,   
            'Special Offer' : Special_Offer,
            'Sorted by' : w3 , 
            'start_url': response.meta['start_url'] ,
                }    
        next_page = response.css('div._2MImiq > nav.yFHi8N > a._1LKTO3::attr(href)').get() 
        print(next_page)
        global w2
        w2 = w2-1          
        if w2 > 0 :
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)