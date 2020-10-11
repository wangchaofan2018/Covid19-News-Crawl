import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class AnhuiSpider(Spider):
    def __init__(self):
        super(AnhuiSpider, self).__init__()
        self.num = 1

    name = "anhui"
    #  = "http://www.ah.gov.cn/content/column/6786741?pageIndex=1"
    original_url = "http://www.ah.gov.cn/zmhd/xwfbhx/index.html"
    
    def start_requests(self):
        url = "http://www.ah.gov.cn/zmhd/xwfbhx/index.html"
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)

    
    def parse(self,response):
        sel = Selector(response)
        detail_page_info =sel.xpath('//div[@class="interview-info"]')
        for info in detail_page_info:
            detail_url = info.xpath('./p/a/@href').extract_first()
            title = info.xpath('./p/a/@title').extract_first()
            publish_time = info.xpath('./p[@class="tit"]/text()').extract_first()
            print(detail_url)
            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url,"title":title,"publish_time":publish_time},callback=self.detail_parse,dont_filter=True)

        if self.num < 12:
            self.num += 1
            next_page_url = "http://www.ah.gov.cn/content/column/6786741?pageIndex=%s"%str(self.num)
            yield scrapy.Request(url=next_page_url,callback=self.parse,dont_filter=True)

    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        item["detail_url"] = response.meta["detail_url"]
        item["title"] = response.meta["title"]
        item["publish_time"] = response.meta["publish_time"]
        item["location"] = "安徽"
        item["summary"]=""

        attend_persons = ""
        attend_person_all = sel.xpath('//div[@class="fty_imglistlb"]/ul/li/a/@data-title').extract()
        # for persons in attend_person_all[:-1]:  #多一个“发布会现场”
            # attend_persons = attend_persons + persons + "\n" #应该不需要去掉空格，因为：省人民政府副省长 章㬢
        attend_persons = attend_person_all[:-1] # 直接拿到列表赋值
        item["attend_persons"] = attend_persons

        content = ""
        content_text = sel.xpath('//div[@class="desc j-fontContent"]/p/text()').extract()
        for row in content_text:
            content = content + row.strip() + "\n"
        item["content"] = content
        yield item

        





         


