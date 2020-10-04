# -*-coding: utf-8 -*-
import sys,os
import scrapy
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
from covid_19.items import BaseDataItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class HubeiSpider(Spider):
    def __init__(self):
        # 初始化chrome对象
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        # chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
        super(HubeiSpider, self).__init__()

    name="hubei"
    base_url = "http://www.hubei.gov.cn/hbfb/xwfbh/"
    # allowed_domains = ["http://www.hubei.gov.cn"]

    def start_requests(self):
        url = "http://www.hubei.gov.cn/hbfb/xwfbh/index.shtml"
        yield scrapy.Request(url=url,meta={'use_browser':True},callback=self.parse,dont_filter=True)

    def parse(self,response):
        page_hrefs = []
        sel = Selector(response)
        detail_page_hrefs = sel.xpath('//div[@class="row media_block"]//h4/a/@href').extract()
        for href_str in detail_page_hrefs:
            href = href_str[2:]
            detail_url = self.base_url+href
            yield scrapy.Request(url=detail_url,meta={'use_browser':True,"detail_url":detail_url},callback=self.detail_parse,dont_filter=True)

        next_page_href = sel.xpath("//nav/ul/li[last()]/a/@href").extract_first()
        if not next_page_href is None:
            next_url = self.base_url+''+next_page_href
            yield scrapy.Request(url=next_url,meta={'use_browser':True},callback=self.parse,dont_filter=True)

    def detail_parse(self,response):
        item = BaseDataItem()
        sel = Selector(response)
        current_url = response.meta["detail_url"]
        cols = sel.xpath('//div[@class="text_record"]/div/p/text()').extract()
        if cols is None:
            cols = sel.xpath('//div[@class="text_record"]//p/span/text()').extract()
        content = ""
        for col in cols:
            content = content+col.strip()+"\n"
        item["publish_time"] = sel.xpath("//ul[@class='list-unstyled int_list']/li[1]/text()").extract_first()
        item["attend_persons"] = sel.xpath("//ul[@class='list-unstyled int_list']/li[2]/text()").extract_first()
        item["location"] = "湖北"
        item["summary"] = sel.xpath("//ul[@class='list-unstyled int_list']//p/text()").extract_first().strip()
        item["title"] = sel.xpath("//h2/text()").extract_first()
        item["content"] = content
        item["detail_url"] = current_url
        yield item


        


