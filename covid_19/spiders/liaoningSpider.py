import scrapy
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class LiaoningSpider(Spider):
    def __init__(self):
        self.year = 2020
        super(LiaoningSpider, self).__init__()
    
    name = "liaoning"

    def start_requests(self):
        home_url = "http://www.ln.gov.cn/spzb/%sxwfbh/index.html"%str(self.year)
        yield scrapy.Request(url=home_url,callback=self.parse,dont_filter=True)

    def parse(self,response):
        print(response.text)
    