import scrapy
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class ShanxiSpider(Spider):
    def __init__(self):
        # 初始化chrome对象
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
        super(ShanxiSpider, self).__init__()
        self.since = 1

    name="shanxi"

    # start_urls = ["http://www.shanxi.gov.cn/yw/xwfbh/szfxwfbh/index.shtml"]
    base_url = "http://www.shanxi.gov.cn/yw/xwfbh/szfxwfbh"
    def start_requests(self):
        start_url = "http://www.shanxi.gov.cn/yw/xwfbh/szfxwfbh/index.shtml"
        yield scrapy.Request(url=start_url,meta={'use_browser':True},callback=self.list_parse,dont_filter=True)

    def list_parse(self,response):
        sel = Selector(response)
        hrefs = sel.xpath("//ul[@class='common-tab-content-box ftsz-16 mgtp-0 common-list-box']/li/a/@href").extract()
        total_page_str = sel.xpath('//span[@class="shanxi-gov-page-form"]').extract_first()
        total_page_obj = re.match(".*?[\u4e00-\u9fa5]+(\d+)[\u4e00-\u9fa5]+",total_page_str)
        print("first1")
        if total_page_obj:
            print("first2")
            total_page_str = total_page_obj.group(1)
            total_page = int(total_page_str)
            if self.since<total_page:
                print("first3")
                next_url = self.base_url + "/index_"+str(self.since)+".shtml"
                self.since+=1
                yield scrapy.Request(url=next_url,meta={'use_browser':True},callback=self.list_parse,dont_filter=True)

        for href_str in hrefs:
            href = href_str[1:]
            next_url = self.base_url+href
            yield scrapy.Request(url=next_url,meta={"detail_url":next_url,'use_browser':True},callback=self.detail_parse,dont_filter=True)
        


    def detail_parse(self,response):
        detail_url = response.meta["detail_url"]
        item = BaseDataItem()
        sel = Selector(response)
        title = sel.xpath('//div[@class="detail-article-title oflow-hd"]/h5//text()').extract_first()
        publish_time = sel.xpath("//li[@class='article-infos-source left']/span[1]//text()").extract_first()
        location = "山西"
        attend_persons = ""
        person_arr = sel.xpath("//p/strong/text()").extract()
        for person in person_arr:
            if person.find("记者")==-1:
                attend_persons = attend_persons+person
        summary = sel.xpath('//p[@align="center"]/following-sibling::p[1]//text()').extract_first()
        content = ""
        content_strs = sel.xpath('//div[@class="TRS_Editor"]/p//text()').extract()
        for content_row in content_strs:
            content = content + content_row.strip()+ "\n"
        
        item["title"] = title
        item['publish_time']= publish_time
        item['location'] = location
        item['attend_persons'] = attend_persons
        item['summary'] = summary
        item['content'] = content
        item['detail_url'] = detail_url
        yield item
        

        






