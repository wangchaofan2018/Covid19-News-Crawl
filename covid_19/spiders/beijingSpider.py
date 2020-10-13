import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class BeijingSpider(Spider):
    def __init__(self):
        self.num = 1
        super(BeijingSpider, self).__init__()

    name = "beijing"
    original_url = "http://www.beijing.gov.cn/shipin/xxgzbdfyyqfb"

    def start_requests(self):
        url = "http://www.beijing.gov.cn/shipin/xxgzbdfyyqfb/"
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)

    def parse(self,response):
        sel = Selector(response)
        detail_page_hrefs =sel.xpath('//div[@class="globalPage_list clearfix"]//li//a/@href')
        for href in detail_page_hrefs:
            detail_url = href
            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url},callback=self.detail_parse,dont_filter=True)

        if self.num < 3:
            self.num += 1
            next_page_url = "http://www.beijing.gov.cn/shipin/xxgzbdfyyqfb/page/%s/"%str(self.num)
            yield scrapy.Request(url=next_page_url,callback=self.parse,dont_filter=True)

        if (self.num >= 3) and (self.num < 50):
            self.num += 1
            next_page_url = "http://www.beijing.gov.cn/shipin/index.php?option=com_content&ItemId=140&page=%s"%str(self.num)
            yield scrapy.Request(url=next_page_url,callback=self.parse,dont_filter=True)
    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        item["detail_url"] = response.meta["detail_url"]
        item["publish_time"] = ""
        item["title"] = ""
        item["summary"]=""
        item["province"] = "北京"
        item["location"] = "北京"
        item["attend_persons"] = ""
        item["time_stamp"] = ""
        content = ""
        content_text = sel.xpath('').extract()
        for row in content_text:
            content = content + row.strip() +"\n"
        item["content"] = content
        print(item)
        # yield item




