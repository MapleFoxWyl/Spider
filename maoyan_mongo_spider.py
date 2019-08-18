import pymongo
from urllib import request
import re
import time
import random
from useragents import ua_list


class MaoyanSpider(object):
  def __init__(self):
    self.url = 'https://maoyan.com/board/4?offset={}'
    # 计数
    self.num = 0
    # 创建3个对象
    self.conn = pymongo.MongoClient(host='127.0.0.1',port=27017)
    self.db = self.conn['maoyandb']
    self.myset = self.db['filmset']

  def get_html(self, url):
    headers = {
      'User-Agent': random.choice(ua_list)
    }
    req = request.Request(url=url, headers=headers)
    res = request.urlopen(req)
    html = res.read().decode('utf-8')
    # 直接调用解析函数
    self.parse_html(html)

  def parse_html(self, html):
    # 创建正则的编译对象
    re_ = '<div class="movie-item-info">.*?title="(.*?)".*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p> '
    pattern = re.compile(re_, re.S)
    # film_list:[('霸王别姬','张国荣','1993')]
    film_list = pattern.findall(html)
    self.write_html(film_list)

  # mysql-executemany
  def write_html(self, film_list):
    for film in film_list:
      film_dict = {
        'name':film[0].strip(),
        'star':film[1].strip(),
        'time':film[2].strip()[5:15]
      }
      self.num+=1
      #插入mongodb数据库
      self.myset.insert_one(film_dict)
      print('爬取成功', self.num, '部')


  def main(self):
    for offset in range(0, 91, 10):
      url = self.url.format(offset)

      self.get_html(url)
      time.sleep(random.randint(1, 2))
    print('共抓取数据', self.num, "部")


if __name__ == '__main__':
  start = time.time()
  spider = MaoyanSpider()
  spider.main()
  end = time.time()
  print('执行时间:%.2f' % (end - start))
