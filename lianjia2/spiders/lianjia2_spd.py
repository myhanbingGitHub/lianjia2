import scrapy
from lxml import etree
from lianjia2.items import Lianjia2Item
import pymysql
import time
import random

# 整体思路： 从租房页面pg=1开始到pg=10  抓取每个pg的房屋列表后进入其详情也继续爬取明细信息。 关键点，item可以从pg页面传参至详情页，最后抛出item.
class Lianjia2SpdSpider(scrapy.Spider):
    name = 'lianjia2_spd'
    allowed_domains = ['lianjia.com']
    urls=[]
    for pg in range(1,101):   # 租房页面 1-100页之间循环
        urls.append('https://sh.lianjia.com/zufang/zufang/pg%s' %pg)

    start_urls = urls

    def parse(self, response):

        done_list = self.getDoneList()    # 从数据库中拿已经爬过的url列表，如果已经爬过了，就不爬了。相当于断点续传。
        print(len(done_list))        # 看看数据库里面爬了多少条记录了
        print("start to parse...")
        html = etree.HTML(response.text)
        ZFs = html.xpath("//div[@class='content__list--item']")   # 查找租房列表
        time.sleep(random.randint(2, 3))  # 反爬，每一页休息x秒
        for ZF in ZFs:    # 循环爬取每套信息
            item = Lianjia2Item()    # item实例化要在循环里面，每次都要初始化。否则就是在外面造一个list了来装记录
            item['url'] = 'https://sh.lianjia.com/zufang'+ZF.xpath(".//a[@class='content__list--item--aside']/@href")[0]
            t=ZF.xpath(".//p[@class='content__list--item--title']/a/text()")
            if t:
                item['title'] = ZF.xpath(".//p[@class='content__list--item--title']/a/text()")[0].strip()
                item['addr1'] = ZF.xpath(".//p[@class='content__list--item--des']/a/text()")[0]
                item['addr2'] = ZF.xpath(".//p[@class='content__list--item--des']/a/text()")[1]
                item['addr3'] = ZF.xpath(".//p[@class='content__list--item--des']/a/text()")[2]
                if item['url'] in done_list:
                    pass
                else:
                    time.sleep(random.randint(1, 2))  # 每套房子间隔 x秒
                    yield scrapy.Request(url=item['url'],callback=self.parse_detail,cb_kwargs=dict(item=item))  # 进入详情页面爬取明细资料
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
            item['type']=html.xpath("//div[@id='aside']/ul[@class='content__aside__list']/li/text()")[1].split(" ")[0]
        if html.xpath("//div[@id='aside']/ul[@class='content__aside__list']/li/text()"):
            item['size']=html.xpath("//div[@id='aside']/ul[@class='content__aside__list']/li/text()")[1].split(" ")[1]
        if html.xpath("//div[@id='aside']/ul[@class='content__aside__list']/li/text()"):
            item['direction']=html.xpath("//div[@id='aside']/ul[@class='content__aside__list']/li/text()")[2].split(" ")[0]
        if html.xpath("//div[@id='aside']/ul[@class='content__aside__list']/li/text()"):
            item['floor']=html.xpath("//div[@id='aside']/ul[@class='content__aside__list']/li/text()")[2].split(" ")[-1]

        return item

    def getDoneList(self):   # 定义函数，抓取现有数据库中记录
        cnn_param = {
            'host': '192.168.88.106',
            'port': 3306,
            'user': 'aiquliu',
            'password': 'hukecld8010',
            'database': 'forscrapy',
            'charset': 'utf8'
        }
        cnn = pymysql.connect(**cnn_param)
        cur = cnn.cursor()

        sql = "select url from lianjia_rent"
        cur.execute(sql)
        rs = cur.fetchall()
        l = []
        for r in rs:
            l.append(r[0])

        # print(l)
        cur.close()
        cnn.close()
        return l



