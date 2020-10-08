import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class LiaoningSpider(Spider):
    def __init__(self):
        self.year = 2020
        self.cur_page = 1
        super(LiaoningSpider, self).__init__()
    
    name = "liaoning"
    original_url = "http://www.ln.gov.cn/spzb/2020xwfbh/"
    gouver_url = "http://www.ln.gov.cn/"

    def start_requests(self):
        home_url = "http://www.ln.gov.cn/spzb/%sxwfbh/index.html"%str(self.year)
        yield scrapy.Request(url=home_url,callback=self.parse,dont_filter=True)

    def parse(self,response):
        sel = Selector(response)
        page_hrefs = []
        detail_page_info = sel.xpath('//div[@class="zf_mainconlist"]//ul/li') #当前页发布会标题和日期
        for info in detail_page_info:
            detail_url = info.xpath('./a/@href').extract_first() #当前页发布会连接
            title = info.xpath('./a/@title').extract_first() #当前页发布会标题
            publish_time = info.xpath('./span').extract_first() #当前页发布会对应发布日期
            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url,"title":title,"publish_time":publish_time},callback=self.detail_parse,dont_filter=True)
        
        
        js_text = sel.xpath('//div[@class="dlist_page"]//text()').extract_first().strip()  #当前页下方换页按钮（当前第1页 | 共4页 | 首页 | 上一页 | ）
        js_text = js_text[:20]
        numbers = re.match(".*?(\d+)",js_text)
        total_page = int(numbers.group(1))
        if self.cur_page<total_page:
            next_url = self.original_url+"index_"+str(self.cur_page)+".html"
            self.cur_page +=1
            yield scrapy.Request(url=next_url,callback=self.parse,dont_filter=True)



    def detail_parse(self,response):
        sel = Selector(response)
        detail_url = response.meta["detail_url"]
        publish_time = response.meta["publish_time"]
        title = response.meta["title"]
        text_url_src = sel.xpath('//div[@class="fbh_wz"]/iframe[1]/@src').extract_first()
        text_url = self.gouver_url + text_url_src
        title = sel.xpath('//div[@class="dlist_titlefbh"]').extract_first()

        yield scrapy.Request(url = text_url,meta={"detail_url":detail_url,"title":title,"publish_time":publish_time,"title":title},callback=self.text_parse,dont_filter=True)


    def text_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        item["publish_time"] = response.meta["publish_time"]
        item["detail_url"] = response.meta["detail_url"]
        item["title"] = response.meta["title"]
        item["location"] = "辽宁"
        content =""
        content_text = sel.xpath('//div[@class="fbh_wzf"]').extract()
        for col in content_text:
            content = content + col.strip() +"\n"

        item["content"] = content
        attend_persons_all = ""
        attend_persons_text = sel.xpath('//div[@class="fbh_wzf"]/div[@class="fbh_rm"]').extract()
        for row in attend_persons_text:
            attend_persons_all = attend_persons_all + row.strip() + "\n"
        attend_persons = list(set(attend_persons_all))
        item["attend_persons"] = attend_persons
        print(item)
        # yield item




    