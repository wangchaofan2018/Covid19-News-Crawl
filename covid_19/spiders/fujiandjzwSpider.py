import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class FujianDjzwSpider(Spider):
    def __init__(self):
        super(FujianDjzwSpider, self).__init__()

    name = "fujiandjzw"
    def start_requests(self):
        url = "http://www.fjsen.com/a/gov/node_16712.htm"
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True) 

    def parse(self,response):
        sel = Selector(response)
        detail_page_info = sel.xpath('//ul[@class="list_page"]//li')
        for info in detail_page_info:
            detail_url = info.xpath('./a/@href').extract_first()
            publish_time = info.xpath('./span/text()').extract_first()
            title = info.xpath('./a/text()').extract_first()
            yield scrapy.Request(url = detail_url,meta={"detail_url":detail_url,"publish_time":publish_time,"title":title},callback=self.detail_parse,dont_filter=True)
    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        item["detail_url"] = response.meta["detail_url"]
        item["publish_time"] = response.meta["publish_time"]
        item["title"] = response.meta["title"]
        summary = ""
        summary_text = sel.xpath('//td[@id="new_message_id"]//p[1]//text()').extract()
        for sum in summary_text:
            summary = summary + sum.strip() +"\n"
        item["summary"]= summary
        item["province"] = "福建"
        item["location"] = ""
        item["attend_persons"] = ""
        item["time_stamp"] = ""
        content = ""
        content_text = sel.xpath('//td[@id="new_message_id"]//p//text()').extract()
        for row in content_text:
            content = content + row.strip() +"\n"
        item["content"] = content
        print(item)
        # yield item
