import scrapy
import re
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from urllib.parse import urlencode
from covid_19.items import BaseDataItem

class ZhejiangSpider(Spider):
    def __init__(self):
        self.since = 0
        super(ZhejiangSpider, self).__init__()

    name = "zhejiang"

    def start_requests(self):
        data_param = {
            'webid':"3096",
            'columnid':"1228996602",
            'unitid':"5504308"
        }
        post_url = "http://www.zj.gov.cn/module/jpage/dataproxy.jsp?startrecord=1&endrecord=45&perpage=15"

        yield scrapy.FormRequest(url=post_url,method="POST",formdata=data_param,headers={"Content_type":"application/x-www-form-urlencoded"},callback=self.parse,dont_filter=True)

    def parse(self,response):
        sel = Selector(response)
        records = sel.xpath("//record").extract()
        for record in records[:-1]:
            detail_url = re.findall(r'.*?<a href="(.*?)" title', record, re.I|re.S|re.M)[0]
            title =re.findall(r'.*?<a.*?title="(.*?)" target', record, re.I|re.S|re.M)[0]
            # 可以看一下能否处理一下publish_time的正则，从这里获取
            publish_time = re.findall('.*<span.*?>(.*?)</span>',record,re.M)[0]

            yield scrapy.Request(url=detail_url,meta={"detail_url":detail_url,"title":title,"publish_time":publish_time},callback=self.detail_parse,dont_filter=True)
        
        if len(records)>45:
            data_param = {
                'webid':"3096",
                'columnid':"1228996602",
                'unitid':"5504308"
            }
            self.since+=45
            post_url = "http://www.zj.gov.cn/module/jpage/dataproxy.jsp?startrecord=%s&endrecord=%s&perpage=15"%(str(self.since+1),str(self.since+45))
            yield scrapy.FormRequest(url=post_url,method="POST",formdata=data_param,headers={"Content_type":"application/x-www-form-urlencoded"},callback=self.parse,dont_filter=True)

        

    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        item["detail_url"] = response.meta["detail_url"]
        item["title"] = response.meta["title"]
        item["province"] = "浙江"
        item["location"] = ""
        content = sel.xpath('//tbody//div[@id="zoom"]/p//text()').extract_first()
        item["content"] = content

        # attend_persons_all = sel.xpath('//div[@class="chat_cont_list"]/ul/li[3]/span[2]/text()').extract_first()
        item["attend_persons"] = ""
        # publish_time = sel.xpath('//div[@class="chat_cont_list"]/ul/li[2]/span[2]/text()').extract_first()
        item["publish_time"] = response.meta["publish_time"]
        item["summary"]=""
        yield item



