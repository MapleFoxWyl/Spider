from urllib import request
import re
from useragents import ua_list
import time
import random
import pymysql
import requests


class FilmSkySpider(object):
  def __init__(self):
    self.url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
    self.num = 0

  # 获取相应内容
  def requests_get(self, url):
    headers = {'User-Agent': random.choice(ua_list)}
    res = requests.get(url=url, headers=headers)
    res.encoding = 'gb2312'
    # 通过网站查看网页远吗,查看网站charset='gb2312'
    # 如果遇到解码错误,识别不了一些字符,则 ignore
    html = res.text
    return html

  # 正则解析功能函数
  def re_func(self, re_bds, html):
    pattern = re.compile(re_bds, re.S)
    r_list = pattern.findall(html)
    return r_list

  # 获取数据函数 html是一级页面相应内容
  def parse_page(self, html):
    # 想办法获取到 电影名称和下载链接
    re_bds = r'<td width="5%".*?<a href="(.*?)".*?class="ulink">(.*?)</a>.*?</td>'
    # one_page_list:[('/html/xxx','幸福猎人'),()]
    one_page_list = self.re_func(re_bds, html)
    item = {}
    for film in one_page_list:
      item['name'] = film[1].strip()
      link = 'https://www.dytt8.net' + film[0]
      item['download'] = self.parse_two_page(link)
      # uniform:浮点数,爬取一个电影信息后sleep
      time.sleep(random.uniform(1, 3))
      print(item)
      self.num+=1
      print('爬取成功', self.num, '部')


  # 解析二级页面数据
  def parse_two_page(self, link):
    html = self.requests_get(link)
    re_bds = r'<tbody>.*?<td style="WORD-WRAP:.*?href="(.*?)">ftp.*?</tbody>'
    # two_page_list:['ftp://xxxx.mkv']
    two_page_list = self.re_func(re_bds, html)
    download = two_page_list[0].strip()
    return download

  def main(self):
    for page in range(1, 2):
      url = self.url.format(page)
      html = self.requests_get(url)
      self.parse_page(html)



if __name__ == '__main__':
  start = time.time()
  spider = FilmSkySpider()
  spider.main()
  end = time.time()
  print('执行时间:%.2f' % (end - start))
