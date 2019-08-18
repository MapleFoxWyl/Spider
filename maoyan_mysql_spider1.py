import pymysql
from urllib import request, parse
import re
import time
import random
from useragents import ua_list


class MaoyanSpider(object):
  def __init__(self):
    self.url = 'https://maoyan.com/board/4?offset={}'
    # 计数
    self.num = 0
    self.db = pymysql.connect(
      'localhost', 'root', '123456', 'maoyandb', charset='utf8'
    )
    self.cursor = self.db.cursor()

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

  def write_html(self, film_list):
    ins = 'insert into filmtab values(%s,%s,%s)'
    for film in film_list:
      L = [
        film[0].strip(),
        film[1].strip(),
        film[2].strip()[5:15]
      ]
      self.num+=1
      print('爬取成功',self.num,'部')
      self.cursor.execute(ins, L)
      #提交到数据库执行
      self.db.commit()

  def main(self):
    for offset in range(0, 91, 10):
      url = self.url.format(offset)

      self.get_html(url)
      time.sleep(random.randint(1, 2))
    print('共抓取数据', self.num, "部")
    # 断开数据库
    self.cursor.close()
    self.db.close()


if __name__ == '__main__':
  start = time.time()
  spider = MaoyanSpider()
  spider.main()
  end = time.time()
  print('执行时间:%.2f' % (end - start))
