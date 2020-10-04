from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class ShanxiSpider(Spider):
    name="shanxi"
    start_urls = ["http://www.shanxi.gov.cn/yw/xwfbh/szfxwfbh/index_2.shtml"]

    def parse(self,response):
        sel = Selector.xpath(response)
        print(response.text)

