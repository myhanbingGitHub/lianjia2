# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Lianjia2Item(scrapy.Item):
    title = url = addr1 = addr2 = addr3 = size = direction = type = price = \
        updateDate = floor = price_unit = rent_model = rent_id = scrapy.Field()
