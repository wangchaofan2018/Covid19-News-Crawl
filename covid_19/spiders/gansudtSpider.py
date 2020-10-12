import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class GansuDtSpider(Spider):
    def __init__(self):
        
        super(GansuDtSpider, self).__init__()

    name = "gansudt"
    original_url = "http://www.gansu.gov.cn"

    def start_requests(self):
        url = "http://www.gansu.gov.cn/col/col10497/index.html"
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)

    def parse(self,response):
        sel = Selector(response)
        deatil_page_info = sel.xpath('//table[@width="96%"]//tr')
        for info in deatil_page_info:
            detail_page_url = info.xpath('.//td[2]/a/@href').extract_first()
            detail_url = self.original_url + detail_page_url
            publish_time = info.xpath('//td[3]/span/text()').extract_first()  #但时间形式为：[2020-09-09]，需要处理
            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url,"publish_time":publish_time},callback=self.detail_parse,dont_filter=True)

    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        item["detail_url"] = response.meta["detail_url"]
        item["publish_time"] = response.meta["publish_time"]
        item["location"] = "甘肃"
        title = ""
        title_text = sel.xpath('//table[@width="95%"]//tr[1]/td/text()').extract()
        for col in title_text:
            title = title + col.strip()

        content = ""
        content_text = sel.xpath('//div[@id="zoom"]//p//text()').extract()
        for row in content_text:
            content = content + row.strip() + "\n"

        item["content"] = content
        item["summary"] = ""
        print(item)
        # yield item



