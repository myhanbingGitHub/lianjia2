import scrapy
from lxml import etree
from lianjia2.items import Lianjia2Item
import path
class Lianjia2SpdSpider(scrapy.Spider):
    name = 'lianjia2_spd'
    allowed_domains = ['lianjia.com']
    urls=[]
    for pg in range(1,101):
        urls.append('https://sh.lianjia.com/zufang/zufang/pg%s' %pg)

    start_urls = urls

    def parse(self, response):

        print("start to parse...")
        html = etree.HTML(response.text)
        ZFs = html.xpath("//div[@class='content__list--item']")
        # title = url = addr1 = addr2 = addr3 = size = direction = type = price = updateDate = floor = scrapy.Field()
        for ZF in ZFs:
            item = Lianjia2Item()    # item实例化要在循环里面，每次都要初始化。否则就是在外面造一个list了来装记录
            item['url'] = 'https://sh.lianjia.com/zufang'+ZF.xpath(".//a[@class='content__list--item--aside']/@href")[0]
            t=ZF.xpath(".//p[@class='content__list--item--title']/a/text()")
            if t:
                item['title'] = ZF.xpath(".//p[@class='content__list--item--title']/a/text()")[0].strip()
                item['addr1'] = ZF.xpath(".//p[@class='content__list--item--des']/a/text()")[0]
                item['addr2'] = ZF.xpath(".//p[@class='content__list--item--des']/a/text()")[1]
                item['addr3'] = ZF.xpath(".//p[@class='content__list--item--des']/a/text()")[2]
                yield scrapy.Request(url=item['url'],callback=self.parse_detail,cb_kwargs=dict(item=item))
        return None

    def parse_detail(self,response,item):
        print("start to parse detail page:",response.url)
        # print("page title:-----------",item_passed)
        html=etree.HTML(response.text)
        # print(html.xpath("//div[@id='aside']/div[@class='content__aside--title']/span/text()")[0])
        if html.xpath("//div[@class='content__subtitle']/text()"):
            item['updateDate'] = html.xpath("//div[@class='content__subtitle']/text()")[0].strip().split("：")[-1]
        if html.xpath("//div[@class='content__subtitle']/i[@class='house_code']/text()"):
            item['rent_id']=html.xpath("//div[@class='content__subtitle']/i[@class='house_code']/text()")[0].\
                strip().split("：")[-1]
        if html.xpath("//div[@id='aside']/div[@class='content__aside--title']/span/text()"):
            item['price']=html.xpath("//div[@id='aside']/div[@class='content__aside--title']/span/text()")[0]
        if html.xpath("//div[@id='aside']/div[@class='content__aside--title']/text()"):
            item['price_unit']=html.xpath("//div[@id='aside']/div[@class='content__aside--title']/text()")[1].\
                strip().split(" ")[0].strip()
        if html.xpath("//div[@id='aside']/ul[@class='content__aside__list']/li/text()"):
            item['rent_model']=html.xpath("//div[@id='aside']/ul[@class='content__aside__list']/li/text()")[0]
        if html.xpath("//div[@id='aside']/ul[@class='content__aside__list']/li/text()"):
            item['type']=html.xpath("//div[@id='aside']/ul[@class='content__aside__list']/li/text()")[1]
        if html.xpath("//div[@id='aside']/ul[@class='content__aside__list']/li/text()"):
            item['direction']=html.xpath("//div[@id='aside']/ul[@class='content__aside__list']/li/text()")[2].split(" ")[0]
        if html.xpath("//div[@id='aside']/ul[@class='content__aside__list']/li/text()"):
            item['floor']=html.xpath("//div[@id='aside']/ul[@class='content__aside__list']/li/text()")[2].split(" ")[-1]

        return item







