import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class XizangSpider(Spider):
    def __init__(self):
        super(XizangSpider, self).__init__()

    name = "xizang"
    original_url = "http://www.xizang.gov.cn/zwgk/xxfb/xwfbh"

    def start_requests(self):
        url = "http://www.xizang.gov.cn/zwgk/xxfb/xwfbh/"
        yield scrapy.Request(url = url,callback=self.parse,dont_filter=True)

    def parse(self,response):
        sel = Selector(response)
        detail_page_info = sel.xpath('//ul[@class="zwyw_list clearfix"]/li')
        for info in detail_page_info:
            detail_page_href = info.xpath('./a/@href').extract_first()
            href = detail_page_href[1:]
            detail_url = self.original_url + href
            title = info.xpath('./a/@title').extract_first()  #在具体页面取标题更准确
            publish_time = info.xpath('./span/text()').extract_first() #content里的时间才是发布会真实日期
            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url,"publish_time":publish_time,"title":title},callback=self.detail_parse,dont_filter=True)

    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        item["detail_url"] = response.meta["detail_url"]
        item["publish_time"] = response.meta["publish_time"]
        item["title"] = response.meta["title"]
        item["summary"]=""
        item["province"] = "西藏自治区"
        item["location"] = ""
        content = ""
        content_text = sel.xpath('//div[@class="vw-art-list"]//p/text()').extract()
        for row in content_text:
            content = content + row.strip() + "\n"
        item["content"] = content
        attend_persons=""
        attend_persons_all = sel.xpath('//div[@class="vw-art-list"]//span/text()').extract()
        for person in attend_persons_all[1:]:
            attend_persons = attend_persons + person.strip() + "\n"
        item["attend_persons"] = ""
        yield item

        