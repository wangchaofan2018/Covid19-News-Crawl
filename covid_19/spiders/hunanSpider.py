import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class HunanSpider(Spider):
    def __init__(self):
        super(HunanSpider, self).__init__()
        self.num = 1

    name = "hunan"
    original_url = "http://www.hunan.gov.cn"

    def start_requests(self):
        url = "http://www.hunan.gov.cn/hnszf/hdjl/xwfbhhd/wqhg/wqgl.html"
        yield scrapy.Request(url = url,callback=self.parse,dont_filter=True)

    def parse(self,response):
        sel = Selector(response)
        detail_page_href = sel.xpath('//div[@class="yl-listbox"]/ul/li') #得到当前页发布会标题和日期
        for each in detail_page_href:
            detail_page_url = each.xpath('./a/@href').extract_first()
            detail_url = self.original_url + detail_page_url
            title = each.xpath('./a/@title').extract_first()
            publish_time = each.xpath('./span/text()').extract_first()
            print(detail_url)
            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url,"title":title,"publish_time":publish_time},callback=self.detail_parse,dont_filter=True)

        if self.num < 3:
            self.num += 1
            next_page_url = "http://www.hunan.gov.cn/hnszf/hdjl/xwfbhhd/wqhg/wqgl_%s.html"%str(self.num)
            yield scrapy.Request(url=next_page_url,callback=self.parse,dont_filter=True)

    def detail_parse(self,response):
        sel = Selector(response)
        item = BaseDataItem()
        item["detail_url"] = response.meta["detail_url"]
        item["title"] = response.meta["title"]
        item["publish_time"] = response.meta["publish_time"]
        item["location"] = "湖南"
        attend_persons_all=sel.xpath('//ul[@class="fbh_list"]/li/p/text()').extract()
        item["attend_persons"] = attend_persons_all

        content = ""
        content_text = sel.xpath('//div[@class="ct_txt"]//p//text()').extract()
        for row in content_text:
            content = content + row.strip() + "\n"
        item["content"] = content
        item["summary"]=""
        print(item)

        # yield item


