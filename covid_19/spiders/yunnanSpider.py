import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class YunnannewsSpider(Spider):
    def __init__(self):
        super(YunnannewsSpider, self).__init__()
        self.num = 1
    name = "yunnannews"
    original_url = "http://www.yn.gov.cn"

    def start_requests(self):
        url = "http://www.yn.gov.cn/ynxwfbt/html/wangqizhibohuigu/shengzhengfuxinwenbanfabuhui/"
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)

    def parse(self,response):
        sel = Selector(response)
        detail_page_info = sel.xpath('//ul[@class="list lh24 f14"]//li')
        for info in detail_page_info:
            publish_time = info.xpath('./span[2]/text()').extract_first()
            detail_url_href = info.xpath('./a/@href').extract_first()
            detail_url = self.original_url + detail_url_href
            title = info.xpath('./a/text()').extract_first()
            yield scrapy.Request(url = detail_url,meta={"detail_url":detail_url,"publish_time":publish_time,"title":title},callback=self.detail_parse,dont_filter=True)

        if self.num < 3:
            self.num += 1
            next_page_url = "http://www.yn.gov.cn/ynxwfbt/html/wangqizhibohuigu/shengzhengfuxinwenbanfabuhui/%s.html"%str(self.num)
            yield scrapy.Request(url=next_page_url,callback=self.parse,dont_filter=True)

    def deatil_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        item["detail_url"] = response.meta["detail_url"]
        item["publish_time"] = response.meta["publish_time"]
        item["title"] = response.meta["title"]
        item["summary"]=""
        item["province"] = "云南"
        item["location"] = ""
        item["attend_persons"] = ""
        item["time_stamp"] = ""
        content = ""  #content内有翻页且页数不固定
        content_text = sel.xpath('')


