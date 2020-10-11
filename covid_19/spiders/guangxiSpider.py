import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class GuangxiSpider(Spider):
    def __init__(self):
        super(GuangxiSpider, self).__init__()
        
    name = "guangxi"
    original_url = "http://www.gxzf.gov.cn/xwfb/index_2.shtml"

    def start_requests(self):
        url = "http://www.gxzf.gov.cn/xwfb/index_2.shtml"
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)

    def parse(self,response):
        sel = Selector(response)
        detail_page_info = sel.xpath('//div[@class="more"]/ul/li')
        for info in detail_page_info:
            detail_url = info.xpath('./a/@href').extract_first()
            title = info.xpath('./a/@title').extract_first()
            publish_time = info.xpath('./span/text()').extract_first()
            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url,"title":title,"publish_time":publish_time},callback=self.detail_parse,dont_filter=True)

    def detail_parse(self,response):
        sel = Selector(response)
        detail_url = response.meta["detail_url"]
        publish_time = response.meta["publish_time"]
        title = response.meta["title"]
        summary = sel.xpath('//td[@class="h1"]/text()').extract_first()
        text_url = sel.xpath('//td[@class="h1"]/a/@href').extract_first()

        yield scrapy.Request(url = text_url,meta={"detail_url":detail_url,"title":title,"publish_time":publish_time,"summary":summary},callback=self.text_parse,dont_filter=True)


    def text_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        item["publish_time"] = response.meta["publish_time"][1:-1]
        item["detail_url"] = response.meta["detail_url"]
        item["location"] = "广西"
        item["title"] = response.meta["title"]
        item["attend_persons"] = ""
        item["summary"] = response.meta["summary"]
        content =""
        content_text = sel.xpath('//div[@class="article-con"]/p//text()').extract()
        for col in content_text:
            content = content + col.strip() +"\n"

        item["content"] = content
        print(item)
        # yield item





