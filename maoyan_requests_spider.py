import csv
from urllib import request, parse
import re
import time
import random
from useragents import ua_list
import requests
from lxml import etree


class MaoyanSpider(object):
  def __init__(self):
    self.url = 'https://maoyan.com/board/4?offset={}'
    # 计数
    self.num = 0
    self.blag=1

  def get_html(self, url):
    headers = {
      'User-Agent': random.choice(ua_list)
    }
    if self.blag<=3:
      try:
        res = requests.get(url, headers=headers,timeout=3)
        res.encoding = 'utf-8'
        html = res.text
        # 直接调用解析函数
        self.parse_html(html)
      except Exception as e:
        print('Retry')
        self.blag+=1
        self.get_html(url)


  def parse_html(self, html):
    parse_html = etree.HTML(html)
    # 创建正则的编译对象
    dd_list = parse_html.xpath('.//dl[@class="board-wrapper"]/dd')
    print(dd_list)
    item = {}
    if dd_list:
      for dd in dd_list:
        item['电影名称'] = dd.xpath('.//p[@class="name"]/a/@title')[0].strip()
        item['主演'] = dd.xpath('.//p[@class="star"]/text()')[0].strip()[3::]
        item['上映时间'] = dd.xpath('.//p[@class="releasetime"]/text()')[0].strip()[5:15]
        self.num+=1

        print(item)

  #   self.write_html(film_list)
  #
  # def write_html(self,film_list):
  #   film_dict={}
  #   for film in film_list:
  #     film_dict['name']=film[0].strip()
  #     film_dict['star']=film[1].strip()
  #     film_dict['time']=film[2].strip()[5:15]
  #     print(film_dict)
  #     self.num += 1

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
