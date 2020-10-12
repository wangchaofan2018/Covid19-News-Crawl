# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field

class BaseDataItem(Item):
    #日期
    publish_time = Field()
    #地点
    location = Field()
    #省份
    province = Field()
    #出席人员
    attend_persons = Field()
    #标题
    title = Field()
    #新闻概要
    summary = Field()
    #新闻文字实录
    content = Field()
    #详情链接
    detail_url = Field()
    #时间戳
    time_stamp = Field()
    pass
