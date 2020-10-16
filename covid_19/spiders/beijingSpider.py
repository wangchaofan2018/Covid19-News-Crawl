import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class BeijingSpider(Spider):
    def __init__(self):
        self.num = 1
        super(BeijingSpider, self).__init__()

    name = "beijing"
    original_url = "http://www.beijing.gov.cn/shipin/xxgzbdfyyqfb"

    def start_requests(self):
        url = "http://www.beijing.gov.cn/shipin/xxgzbdfyyqfb/"
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)

    def parse(self,response):
        sel = Selector(response)
        detail_page_hrefs =sel.xpath('//div[@class="globalPage_list clearfix"]//li//a/@href').extract()
        for href in detail_page_hrefs:
            detail_url = href
            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url},callback=self.detail_parse,dont_filter=True)

        if self.num < 3:
            self.num += 1
            next_page_url = "http://www.beijing.gov.cn/shipin/xxgzbdfyyqfb/page/%s/"%str(self.num)
            yield scrapy.Request(url=next_page_url,callback=self.parse,dont_filter=True)

        if (self.num >= 3) and (self.num < 23):
            self.num += 1
            next_page_url = "http://www.beijing.gov.cn/shipin/index.php?option=com_content&ItemId=140&page=%s"%str(self.num)
            yield scrapy.Request(url=next_page_url,callback=self.parse,dont_filter=True)
    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        publish_time = sel.xpath("//span/text()").extract_first()
        if len(publish_time)<6:
            publish_time = sel.xpath('//p[@class="detailmsg"]').extract_first()
            if publish_time is None:
                publish_time = sel.xpath('//h6/text()').extract_first()
                pass
            pass
        print(publish_time)
        publish_time = re.findall(r".*?(\d+-\d+-\d+).*",publish_time,re.M)[0]
        title = sel.xpath("//h1/text()").extract_first()
        if title is None:
            title = sel.xpath("//h2/text()").extract_first()
            pass
        item["detail_url"] = response.meta["detail_url"]
        item["publish_time"] = publish_time
        item["title"] = title
        item["summary"]=""
        item["province"] = "北京"
        item["location"] = "北京"
        item["attend_persons"] = ""
        item["time_stamp"] = ""
        content = ""
        content_text = sel.xpath('//div[@class="container"]/p/text()').extract()
        if len(content_text)==0:
            content_text = sel.xpath('//div[@class="brief"]/text()').extract()
        
        for row in content_text:
            content = content + row.strip() +"\n"
        item["content"] = content
        yield item




