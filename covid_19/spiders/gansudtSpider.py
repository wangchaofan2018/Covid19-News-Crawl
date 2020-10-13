import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class GansuDtSpider(Spider):
    def __init__(self):
        self.data_param = {
            'webid':"1",
            'columnid':"10497",
            'unitid':"1342"
        }
        self.since = 0
        super(GansuDtSpider, self).__init__()

    name = "gansudt"
    original_url = "http://www.gansu.gov.cn"

    def start_requests(self):
        url = "http://www.gansu.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord=1&endrecord=120&perpage=40"
        yield scrapy.FormRequest(url=url,method="POST",formdata=self.data_param ,headers={"Content_type":"application/x-www-form-urlencoded"},callback=self.parse,dont_filter=True)

    def parse(self,response):
        total = int(re.findall(r"totalRecord=(\d+)",response.text,re.M)[0])
        sel = Selector(response)
        deatil_page_info = sel.xpath('//table[@width="96%"]//tr')
        for info in deatil_page_info:
            detail_page_url = info.xpath('.//td[2]/a/@href').extract_first()
            print(detail_page_url)
            print("***")
            detail_url = self.original_url + "/" + detail_page_url[2:-2]
            publish_time_all = info.xpath('//td[3]/span/text()').extract_first()  #但时间形式为：[2020-09-09]，需要处理
            publish_time = publish_time_all[1:-1]
            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url,"publish_time":publish_time},callback=self.detail_parse,dont_filter=True)

        self.since +=120
        if self.since<total:
            url = "http://www.gansu.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord=%s&endrecord=%s&perpage=40"%(str(self.since+1),str(self.since+120))
            yield scrapy.FormRequest(url=url,method="POST",formdata=self.data_param ,headers={"Content_type":"application/x-www-form-urlencoded"},callback=self.parse,dont_filter=True)
        

    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        item["detail_url"] = response.meta["detail_url"]
        item["publish_time"] = response.meta["publish_time"]
        item["province"] = "甘肃"
        item["location"] = ""
        item["attend_persons"]=[]
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
        yield item



