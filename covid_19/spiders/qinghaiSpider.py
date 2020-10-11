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
        detail_page_info =sel.xpath('//table[@align="center"]//td')
        for info in detail_page_info:
            detail_url = info.xpath('./a/@href').extract_first()
            publish_time = info.xpath('./div[@align="right"]').extract_first()
            # publish_time = publish_time_original[1:-1]  # 返回的日期为[03-27]，需要取出3-27
            print(detail_url)
            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url,"publish_time":publish_time},callback=self.detail_parse,dont_filter=True)

        if self.num > 5:
            next_page_url = "http://www.qh.gov.cn/zwgk/system/more/203080000000000/0000/203080000000000_0000003%s.shtml"%str(self.num)
            self.num -= 1
            yield scrapy.Request(url=next_page_url,callback=self.parse,dont_filter=True)


    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        item["detail_url"] = response.meta["detail_url"]
        item["publish_time"] = response.meta["publish_time"]
        item["location"] = "青海"
        title = sel.xpath('//h1[@class="blue tc"]').extract_first()
        item["title"] = title
        content = ""
        content_text = sel.xpath('//div[@class="details_content"]/p/text()').extract()
        for row in content_text:
            content = content + row.strip() + "\n"
        item["content"] = content
        item["attend_persons"] = ""
        item["summary"]=""
        print(item)
        # yield item

