import scrapy
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class LiaoningSpider(Spider):
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
        self.domain = "http://www.hlj.gov.cn"
        self.next_base_url = "http://www.hlj.gov.cn/33/49/586/"
        super(LiaoningSpider, self).__init__()
    
    name = "heilongjiang"

    def start_requests(self):
        home_url = "http://www.hlj.gov.cn/33/49/586/index.html"
        yield scrapy.Request(url=home_url,meta={'use_browser':False},callback=self.parse,dont_filter=True)

    def parse(self,response):
        sel = Selector(response)
        li_labels = sel.xpath('//div[@class="clearfix w1000 ej_con"]/ul/li')
        for li_label in li_labels:
            href_str = li_label.xpath(".//a/@href").extract_first()
            publish_time = li_label.xpath(".//em/text()")
            target_url = ""
            if href_str[0]=="/":
                target_url = self.domain+href_str
            else:
                target_url = href_str
            yield scrapy.Request(url=target_url,meta={"publish_time":publish_time,"detail_url":target_url,'use_browser':True},callback=self.parse_detail,dont_filter=True)

        next_page_url = sel.xpath('//div[@class="page_ejn clearfix"]/a[last()-1]/@href').extract_first()
        if not next_page_url is None:
            next_page_url = self.next_base_url+next_page_url
            yield scrapy.Request(url=next_page_url,meta={'use_browser':False},callback=self.parse,dont_filter=True)

    def parse_detail(self,response):
        item = BaseDataItem()
        publish_time = response.meta["publish_time"]
        detail_url = response.meta["detail_url"]
        sel = Selector(response)
        attend_persons = sel.xpath('//div[@class="zbBox"]/div[2]//span//text()').extract_first()
        summary = sel.xpath('//div[@class="zbBox"]/div[3]//span//text()').extract_first()
        content_strs= sel.xpath('//div[@id="zhiboc"]//text()').extract()
        title = sel.xpath('//div[@class="title"]//text()').extract_first()
        content = ""
        location = "黑龙江"
        for content_str in content_strs:
            content = content + content_str.strip()+"\n"
        item["title"] = title
        item['publish_time']= publish_time
        item['location'] = location
        item['attend_persons'] = attend_persons
        item['summary'] = summary
        item['content'] = content
        item['detail_url'] = detail_url
        yield item


        
            
