import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class ZhejiangSpider(Spider):
    def __init__(self):
        super(ZhejiangSpider, self).__init__()
        self.num = 1

    name = "zhejiang"
    original_url = "http://www.zj.gov.cn/col/col1228996603/index.html"

    def start_requests(self):
        news_url = "http://www.zj.gov.cn/col/col1228996603/index.html"
        yield scrapy.Request(url=news_url,callback=self.parse,dont_filter=True)

    def parse(self,response):
        sel = Selector(response)
        detail_page_info = sel.xpath('//div[@class="xc_pgContainer"]/ul/li') #得到当前页发布会标题和日期
        for info in detail_page_info:
            detail_url = info.xpath('./a/@href').extract_first() #当前页每条发布会链接
            title = info.xpath('./a/@title').extract_first()  #当前页每条发布会标题
            # publish_time = info.xpath('./span').extract_first() #当前页每条发布会发布日期
            print(detail_url)
            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url,"title":title},callback=self.detail_parse,dont_filter=True)
        
        if self.num < 4:
            self.num += 1
            next_page_url = self.original_url + "?uid=5504308&pageNum=%s"%str(self.num)
            yield scrapy.Request(url=next_page_url,callback=self.parse,dont_filter=True)

    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        item["detail_url"] = response.meta["detail_url"]
        item["title"] = response.meta["title"]
        item["location"] = "浙江"
        content = sel.xpath('//div[@class="chat_cont_list"]/ul/li[4]/span[2]').extract_first()
        item["content"] = content

        attend_persons_all = sel.xpath('//div[@class="chat_cont_list"]/ul/li[3]/span[2]').extract_first()
        item["attend_persons"] = attend_persons_all

        publish_time = sel.xpath('//div[@class="chat_cont_list"]/ul/li[2]/span[2]').extract_first()
        item["publish_time"] = publish_time
        print(item)
        # yield item



