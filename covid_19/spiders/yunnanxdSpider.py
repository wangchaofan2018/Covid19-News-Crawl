import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class YunnanXdSpider(Spider):
    def __init__(self):
        super(YunnanXdSpider, self).__init__()
        self.num = 1
    name = "yunnanxd"
    original_url = "http://www.yn.gov.cn/ztgg/yqfk/ynxd"
    def start_requests(self):
        url = "http://www.yn.gov.cn/ztgg/yqfk/ynxd/index.html"
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)
    def parse(self,response):
        sel = Selector(response)
        detail_page_info = sel.xpath('//dl[@class="thlist"]')
        for info in detail_page_info:
            detail_url_href = info.xpath('./dt/a/@href').extract_first()
            href = detail_url_href[1:]
            # href = "".join(href_list)
            detail_url = self.original_url + href
            title = info.xpath('./dt/a//text()').extract_first()
            publish_time = info.xpath('.//dd/text()').extract_first()
            yield scrapy.Request(url = detail_url,meta={"detail_url":detail_url,"publish_time":publish_time,"title":title},callback=self.detail_parse,dont_filter=True)

        if self.num < 18:
            next_page_url = "http://www.yn.gov.cn/ztgg/yqfk/ynxd/index_%s.html"%str(self.num)
            self.num += 1
            yield scrapy.Request(url=next_page_url,callback=self.parse,dont_filter=True)

    def detail_parse(self,response):
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
        content = ""
        content_text = sel.xpath('//div[@class="view TRS_UEDITOR trs_paper_default trs_web"]//p//text()').extract()
        for row in content_text:
            content = content + row.strip() +"\n"
        item["content"] = content
        yield item
