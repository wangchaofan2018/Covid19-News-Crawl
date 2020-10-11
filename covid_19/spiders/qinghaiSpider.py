import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class QinghaiSpider(Spider):
    def __init__(self):
        super(QinghaiSpider, self).__init__()
        self.num = 7

    name = "qinghai"
    original_url = "http://www.qh.gov.cn/zwgk/xwfbh/zxfb/"

    def start_requests(self):
        url = "http://www.qh.gov.cn/zwgk/xwfbh/zxfb/"
        yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)
    def parse(self,response):
        sel = Selector(response)
        detail_page_info =sel.xpath('//table[@width="720"]//td[1]')
        for info in detail_page_info:
            detail_url = info.xpath('./a/@href').extract_first()
            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url},callback=self.detail_parse,dont_filter=True)

        if self.num > 5:
            next_page_url = "http://www.qh.gov.cn/zwgk/system/more/203080000000000/0000/203080000000000_0000003%s.shtml"%str(self.num)
            self.num -= 1
            yield scrapy.Request(url=next_page_url,callback=self.parse,dont_filter=True)


    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        raw_time_data = sel.xpath("//div[@class='abstract tc']/text()").extract()
        raw_time = raw_time_data[3].strip().split(" ",1)
        publish_time = raw_time[0]
        item["detail_url"] = response.meta["detail_url"]
        item["publish_time"] = publish_time
        item["province"] = "青海"
        item["location"] = ""
        title = sel.xpath('//h1[@class="blue tc"]/text()').extract_first()
        item["title"] = title
        content = ""
        content_text = sel.xpath('//div[@class="details_content"]/p/text()').extract()
        for row in content_text:
            content = content + row.strip() + "\n"
        item["content"] = content
        item["attend_persons"] = ""
        item["summary"]=""
        yield item

