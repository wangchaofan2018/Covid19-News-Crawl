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
        detail_page_info =sel.xpath('//table[@width="95%"]//table[@width="100%"]//tr')
        for info in detail_page_info:
            detail_page_url = info.xpath('./td[1]/a/@href').extract_first()
            if detail_page_url is None:
                break
            detail_url = self.original_url + detail_page_url
            publish_time = sel.xpath('./td[2]/text()').extract_first()
            # yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url,"publish_time":publish_time},callback=self.detail_parse,dont_filter=True)

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
        item["title"] = title.strip()

        content = ""
        content_text = sel.xpath('//div[@id="cmsArticleContent"]//p/text()').extract()
        for row in content_text:
            content = content + row.strip() + "\n"
        item["content"] = content
        item["attend_persons"] = ""
        item["summary"]=""
        yield item







