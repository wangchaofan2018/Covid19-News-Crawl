#http://www.nx.gov.cn/zwxx_11337/ftt/index_34.html    到35页
import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class NingxiaSpider(Spider):
    def __init__(self):
        super(NingxiaSpider, self).__init__()
        self.num = 1

    name = "ningxia"

    def start_requests(self):
        url = "http://www.nx.gov.cn/zwxx_11337/ftt/index.html"
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)

    def parse(self,response):
        sel = Selector(response)
        detail_page_info = sel.xpath('//div[@class="list-con"]//ul/li')
        for info in detail_page_info:
            detail_url = info.xpath('.')

