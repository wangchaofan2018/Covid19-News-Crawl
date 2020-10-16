#http://www.nx.gov.cn/zwxx_11337/ftt/index_34.html    到35页
import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class NingxiaSpider(Spider):
    def __init__(self):
        super(NingxiaSpider, self).__init__()
        self.prefix1 = "http://www.nx.gov.cn/zwxx_11337/ftt"
        self.prefix2 = "http://www.nx.gov.cn/zwxx_11337/wztt"
        self.num = 1

    name = "ningxia"

    def start_requests(self):
        url = "http://www.nx.gov.cn/zwxx_11337/ftt/index.html"
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)

    def parse(self,response):
        sel = Selector(response)
        detail_page_info = sel.xpath('//div[@class="list-con"]//ul/li')
        for info in detail_page_info:
            url_info = info.xpath('./a/@href').extract_first()
            detail_url = ""
            if(url_info.find("..")):
                detail_url = self.prefix1 + url_info[1:]
            else:
                detail_url = self.prefix2 + url_info[2:]
            scrapy.Request(url=detail_url,callback=self.detail_parse,dont_filter=True)

    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        title = sel.xpath('//div[@id="info_title"]/text()').extract_first()
        raw_time = sel.xpath('//span[@id="info_released_dtime"]/text()').extract_first()
        publish_time = raw_time[:-9]
        content = ""
        content_strs = sel.xpath('//div[@id="ofdneed"]//p/text()').extract()
        for content_str in content_strs:
            content = content + content_str.strip()+"\n"
        attend_persons_str = sel.xpath('//div[@id="ofdneed"]//p[last()]/text()').extract_first()
        attend_persons = attend_persons_str.split("，")
        item["publish_time"] = publish_time
        item["location"]=""
        item["province"]="宁夏"
        item["attend_persons"]=attend_persons
        item["title"] = title
        item["summary"] = ""
        item["content"] = content
        yield item
                

