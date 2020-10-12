import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem

class NeimengguSpider(Spider):
    def __init__(self):
        self.data_param = {
            'webid':"2",
            'columnid':"1972",
            'unitid':"1301"
        }
        super(NeimengguSpider, self).__init__()
        self.num = 1


    name = "neimenggu"
    original_url = "http://www.nmg.gov.cn"
    original_page_url = "http://www.nmg.gov.cn/col/col1972/index.html?uid=1301&pageNum=1"

    def start_requests(self):
        post_url = "http://www.nmg.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=1&endrecord=40&perpage=40"
        yield scrapy.FormRequest(url=post_url,method="POST",formdata=self.data_param ,headers={"Content_type":"application/x-www-form-urlencoded"},callback=self.parse,dont_filter=True)
    
    def parse(self,response):
        sel = Selector(response)
        records =sel.xpath('//record/text()').extract()
        for record in records[:-1]:
            detail_page_url = re.findall(".*<a.*?href='(.*?)' title", record, re.I|re.S|re.M)[0]
            detail_url = self.original_url + "/" + detail_page_url
            title = re.findall(".* title='(.*?)'>",record)
            publish_time = re.findall('.*<div .*?>(.*?)</div>',record,re.M)[0].strip()
            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url,"title":title,"publish_time":publish_time},callback=self.detail_parse,dont_filter=True)

        if self.num <3:
            url = "http://www.nmg.gov.cn/module/web/jpage/dataproxy.jsp?startrecord=%s&endrecord=%s&perpage=40"%(str(self.num*40),str(self.num*40+40))
            self.num += 1
            yield scrapy.FormRequest(url=url,method="POST",formdata=self.data_param,headers={"Content_type":"application/x-www-form-urlencoded"},callback=self.parse,dont_filter=True)

    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        item["detail_url"] = response.meta["detail_url"]
        item["title"] = response.meta["title"]
        item["publish_time"] = response.meta["publish_time"]
        item["province"] = "内蒙古自治区"
        item["location"] = ""
        content = ""
        content_text = sel.xpath('//div[@id="zoom"]/p//text()').extract()
        for row in content_text:
            content = content + row.strip() + "\n"

        item["content"] = content
        item["attend_persons"] = ""
        item["summary"]=""
        yield item



        