import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class NeimengguSpider(Spider):
    def __init__(self):
        super(NeimengguSpider, self).__init__()
        self.num = 1


    name = "neimenggu"
    original_url = "http://www.nmg.gov.cn"
    original_page_url = "http://www.nmg.gov.cn/col/col1972/index.html?uid=1301&pageNum=1"

    def start_requests(self):
        url = "http://www.nmg.gov.cn/col/col1972/index.html"
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)
    
    def parse(self,response):
        sel = Selector(response)
        detail_page_info =sel.xpath('//div[@class="msg_listcon_list_title"]')
        for info in detail_page_info:
            detail_page_url = self.xpath('./a/@href').extract_first()
            detail_url = self.original_url + detail_page_url
            title = info.xpath('./a/@title').extract_first()
            publish_time = info.xpath('./div').extract_first()
            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url,"title":title,"publish_time":publish_time},callback=self.detail_parse,dont_filter=True)

        if self.num <7:
            self.num += 1
            next_page_url = "http://www.nmg.gov.cn/col/col1972/index.html?uid=1301&pageNum=%s"%str(self.num)
            yield scrapy.Request(url=next_page_url,callback=self.parse,dont_filter=True)

    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        item["detail_url"] = response.meta["detail_url"]
        item["title"] = response.meta["title"]
        item["publish_time"] = response.meta["publish_time"]
        item["location"] = "内蒙古自治区"
        content = ""
        content_text = sel.xpath('//div[@id="zoom"]/p/text()').extract()
        for row in content_text:
            content = content + row.strip() + "\n"

        item["content"] = content
        item["attend_persons"] = ""
        item["summary"]=""
        print(item)
        # yield item
        #//div[@id="zoom"]/p[@style="text-align: left; text-indent: 2em;"]/strong  可拿到正文左侧加粗，但并不只有参加人



        