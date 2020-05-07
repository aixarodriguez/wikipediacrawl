# -*- coding: utf-8 -*-
import scrapy
from wikipedia_prjct.items import articles
from w3lib.html import remove_tags

class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Wikipedia:Featured_articles']

    def parse(self, response):
        for item in self.scrape(response):
            yield item
    
    def scrape(self, response):
        host=self.allowed_domains[0]
        i=0
        for resource in response.css(".featured_article_metadata > a"):
            if i<300:
                item = articles() 
                item['name'] = resource.attrib.get("title"),
                profilepage = f"https://{host}{resource.attrib.get('href')}"
                item['link'] = profilepage        
                i+=1
                request= scrapy.Request(profilepage, callback=self.pagedtl)            
                request.meta['item'] = item #By calling .meta, we can pass our item object into the callback.
                yield request

    def pagedtl(self, response):        
        item = response.meta['item'] #Get the item we passed from scrape()   
        t=response.css("h1.firstHeading::text").extract_first() 
        p=remove_tags(response.xpath("descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' mw-parser-output ')]/p[2]").get())
        if(len(p)<10):
            p=remove_tags(response.xpath("descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' mw-parser-output ')]/p[3]").get())
        item['body']={}
        item['body']['title']=t
        item['body']['paragraph']=p        
        yield item       
        
        
