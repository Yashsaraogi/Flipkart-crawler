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

item = df['Name'].tolist()
starturl =[]

for w1 in item:                                                     
   starturl.append(f'https://www.flipkart.com/search?q={w1}')
print(starturl)

class FlipkartScraper(scrapy.Spider):
  name = "flipkart_scraper"
  start_urls = starturl
  no_of_pages = 4

  # page_no = 0

  def start_requests(self):
    for url in self.start_urls:
            # yield scrapy.Request(url=get_url(url), dont_filter=True, meta={'start_url': url},callback=self.parse,
            # method="GET")
            yield scrapy.Request(url, dont_filter=True, meta={'start_url': url},callback=self.parse,
            method="GET")


  def parse(self, response):
    self.no_of_pages -= 1
    # self.page_no += 1

    laptops = response.xpath("//div[@class='bhgxx2 col-12-12']/div[@class='_3O0U0u']/div/div[@class='_1UoZlX']/a[@class='_31qSD5']").xpath("@href").getall()
    
    for laptop in laptops:
      laptopUrl = response.urljoin(laptop)
      yield scrapy.Request(url = laptopUrl, callback = self.parse_laptop, headers = self.headers)

    if(self.no_of_pages > 0):
      next_page_all_href = response.xpath("//div[@class='_2zg3yZ']/nav[@class='_1ypTlJ']/a[@class='_3fVaIS']").xpath("@href").getall()
      next_page_href = next_page_all_href[len(next_page_all_href) - 1]
      next_page_url = response.urljoin(next_page_href)
      yield scrapy.Request(url = next_page_url, callback = self.parse, headers = self.headers)

  def parse_laptop(self, response):
    laptopUrl = response.request.url
    laptopName = response.xpath("//span[@class='_35KyD6']//text()").get()
    laptopPrice = response.xpath("//div[@class='_1vC4OE _3qQ9m1']//text()").get()
    laptopHighlights = response.xpath("//div[@class='g2dDAR']/div[@class='_3WHvuP']/ul/li[@class='_2-riNZ']//text()").getall()
    laptopSpec = response.xpath("//div[@class='MocXoX']/div/div[@class='_3Rrcbo V39ti-']/div[@class='_2RngUh']")
    
    laptopSpecifications = []

    for spec in laptopSpec:
      tempSpec = []

      specTitle = spec.xpath("div[@class='_2lzn0o']/text()").get()
      specItems = spec.xpath("table[@class='_3ENrHu']/tbody/tr[@class='_3_6Uyw row']")
      
      tempSpec.append(specTitle)

      detailSpec = []

      for item in specItems:
        tempDetailSpec = []

        specLabel = item.xpath("td[@class='_3-wDH3 col col-3-12']//text()").get()
        specValue = item.xpath("td[@class='_2k4JXJ col col-9-12']//text()").get()

        tempDetailSpec.append(specLabel)
        tempDetailSpec.append(specValue)

        detailSpec.append(tempDetailSpec)

      tempSpec.append(detailSpec)
      laptopSpecifications.append(tempSpec)
    
    laptopRating = response.xpath("//div[@class='col-12-12 _11EBw0']/div[@class='_1i0wk8']//text()").get()
    
    # laptopImageUrl = response.xpath("//div[@class='_3BTv9X _3iN4zu']/img/@src").get()
    
    yield {'name' : laptopName, 'price' : laptopPrice, 'highlight' : laptopHighlights, 'specification' : laptopSpecifications, 'rating' : laptopRating}