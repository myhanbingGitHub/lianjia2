import scrapy
from lxml import etree
from lianjia2.items import Lianjia2Item

class Lianjia2SpdSpider(scrapy.Spider):
    name = 'lianjia2_spd'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://sh.lianjia.com/zufang/']

    def parse(self, response):
        print("start to parse...")
        html = etree.HTML(response.text)
        ZFs = html.xpath("//p[@class='content__list--item']")
        # title = url = addr1 = addr2 = addr3 = size = direction = type = price = updateDate = floor = scrapy.Field()
        item = Lianjia2Item
        for ZF in ZFs:
            item['title']=ZF.x
        return None
