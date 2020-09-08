# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import datetime


class Lianjia2Pipeline:

    def __init__(self):
        cnn_param = {
            'host': '192.168.88.106',
            'port': 3306,
            'user': 'aiquliu',
            'password': 'hukecld8010',
            'database': 'forscrapy',
            'charset': 'utf8'
        }
        self.cnn = pymysql.connect(**cnn_param)
        self.cur = self.cnn.cursor()

    def process_item(self, item, spider):
        try:
            sql = "insert into lianjia_rent (RentID, Title, url, addr1, addr2, addr3, AreaSize, Direction, " \
                  "Type, Price,Updated, Price_Unit, Floor, Rent_Model)" \
                  " values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cur.execute(sql,
                             (item['rent_id'], item['title'], item['url'], item['addr1'], item['addr2'], item['addr3'],
                              item['size'], item['direction'], item['type'], int(item['price']),
                              datetime.datetime.strptime(item['updateDate'], "%Y-%m-%d"),
                              item['floor'],
                              item['price_unit'], item['rent_model'])
                             )
            self.cnn.commit()
            print("记录已存入！")
        except:
            self.cnn.rollback()
            print("记录存入失败！%s" % item['url'])

        return item
