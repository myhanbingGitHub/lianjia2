from scrapy.cmdline import execute

execute('scrapy crawl lianjia2_spd'.split(' '))


# -----------------test-------------------------------
#
# import pymysql
#
# cnn_param = {
#     'host': '192.168.88.106',
#     'port': 3306,
#     'user': 'aiquliu',
#     'password': 'hukecld8010',
#     'database': 'forscrapy',
#     'charset': 'utf8'
# }
# cnn = pymysql.connect(**cnn_param)
# cur = cnn.cursor()
#
# sql = "select url from lianjia_rent"
# cur.execute(sql)
# rs=cur.fetchall()
# l=[]
# for r in rs:
#     l.append(r[0])
#
# print(l)
# cur.close()
# cnn.close()