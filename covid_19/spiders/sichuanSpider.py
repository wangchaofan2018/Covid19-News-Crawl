import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class SichuanSpider(Spider):
    def __init__(self):
        super(SichuanSpider, self).__init__()
        self.num = 1
    
    name = "sichuan"
    original_url = "http://www.sc.gov.cn"
    
    def start_requests(self):
        url = "http://www.sc.gov.cn/10462/10705/10707/xwfbt_list.shtml"
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)

    def parse(self,response):
        sel = Selector(response)
        detail_page_info =sel.xpath('//table[@align="center"]')
        for info in detail_page_info:
            detail_page_url = sel.xpath('.//td/a/@href').extract_first()
            detail_url = self.original_url + detail_page_url
            publish_time = sel.xpath('.//td[@align="right"]/text()').extract_first()
            print(detail_url)
            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url,"publish_time":publish_time},callback=self.detail_parse,dont_filter=True)

        if self.num < 2:
            self.num += 1
            next_page_url = "http://www.sc.gov.cn/10462/10705/10707/xwfbt_list_%s.shtml"%str(self.num)
            yield scrapy.Request(url=next_page_url,callback=self.parse,dont_filter=True)

    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        item["detail_url"] = response.meta["detail_url"]
        item["publish_time"] = response.meta["publish_time"]
        item["location"] = "四川"
        title = sel.xpath('//div[@id="articlecontent"]/h2/ucaptitle/text()').extract_first()
        item["title"] = title

        content = ""
        content_text = sel.xpath('//div[@id="cmsArticleContent"]//p/text()').extract()
        for row in content_text:
            content = content + row.strip() + "\n"
        item["content"] = content
        item["attend_persons"] = ""
        item["summary"]=""
        print(item)

        # yield item
        #//table[@align="center"]//td[@align="right"]







