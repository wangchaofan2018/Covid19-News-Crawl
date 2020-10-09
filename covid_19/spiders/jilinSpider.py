import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class JilinSpider(Spider):
    def __init__(self):
        super(JilinSpider, self).__init__()
        self.num = 1

    name = "jilin"
    original_url = "http://www.jl.gov.cn/szfzt/xwfb/xwfbh/"


    def start_requests(self):
        url = "http://www.jl.gov.cn/szfzt/xwfb/xwfbh/index.html"
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)

    def parse(self,response):
        sel = Selector(response)
        detail_page_info = sel.xpath('//div[@class="news_List_mod_wap news_List_mod_sp ywtplb2"]/ul/li') #得到当前页发布会标题和日期
        for info in detail_page_info:
            detail_url = info.xpath('./a/@href').extract_first() #当前页发布会连接
            title = info.xpath('./a/@title').extract_first() #当前页发布会标题
            publish_time = info.xpath('./span/text()').extract_first() #当前页发布会对应发布日期
            if detail_url[0] == ".":
                return
            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url,"title":title,"publish_time":publish_time},callback=self.detail_parse,dont_filter=True)

        if self.num < 24:
            next_page_href = self.original_url + "index_%s.html"%str(self.num)
            self.num += 1
            yield scrapy.Request(url=next_page_href,callback=self.parse,dont_filter=True)


    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        item["publish_time"] = response.meta["publish_time"]
        item["detail_url"] = response.meta["detail_url"]
        item["title"] = response.meta["title"]
        item["location"] = "吉林"

        content =""
        content_text = sel.xpath('//div[@class="TRS_Editor"]//text()').extract()
        for col in content_text:
            content = content + col.strip() +"\n"
        item["content"] = content

        attend_persons_all = ""
        attend_persons_text = sel.xpath('//font/text()').extract()
        item["attend_persons"] = attend_persons_text
        item["summary"]=""
        yield item



