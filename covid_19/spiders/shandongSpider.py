import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class HainanSpider(Spider):
    def __init__(self):
        super(HainanSpider, self).__init__()
        self.num = 1
    name = "shandong"
    def start_requests(self):
        url = "http://sd.iqilu.com/v5/live/qwfbList?page=1"
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)
    def parse(self,response):
        sel = Selector(response)
        detail_page_info = sel.xpath('//div[@class="news-pic-item"]//dl')
        for info in detail_page_info:
            detail_url = info.xpath('.//h3/a/@href').extract_first()
            publish_time = info.xpath('.//dd[@class="info"]/span[2]/text()').extract_first()
            title = info.xpath('.//h3/a/@title').extract_first()
            yield scrapy.Request(url = detail_url,meta={"detail_url":detail_url,"publish_time":publish_time,"title":title},callback=self.detail_parse,dont_filter=True)

        if self.num < 10:
            self.num += 1
            next_page_url = "http://sd.iqilu.com/v5/live/qwfbList?page=%s"%str(self.num)
            yield scrapy.Request(url=next_page_url,callback=self.parse,dont_filter=True)

    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        item["detail_url"] = response.meta["detail_url"]
        item["publish_time"] = response.meta["publish_time"]
        item["title"] = response.meta["title"]
        item["summary"] = ""
        item["province"] = "山东"
        item["location"] = ""
        attend_persons = ""
        attend_persons_text = sel.xpath('//div[@class="photos"]/ul//li/p/a/text()').extract()
        for per in attend_persons_text:
            attend_persons = attend_persons + per.strip() +"\n"
        item["attend_persons"] = attend_persons
        item["time_stamp"] = ""
        item["score"] = ""
        content = ""
        content_text = sel.xpath('//div[@class="info"]//text()').extract()
        for col in content_text:
            content = content + col.strip() +"\n"
        item["content"] = content
        yield item



