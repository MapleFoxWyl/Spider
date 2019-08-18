import requests
import re
from lxml import etree
import time
import random
from useragents import ua_list


class LianjiaSpider():
  def __init__(self):
    self.url = 'https://sy.lianjia.com/ershoufang/pg{}/'
    self.blog = 1

  def get_html(self, url):
    headers = {'User-Agent': random.choice(ua_list)}
    if self.blog<=3:
      try:
        res = requests.get(url=url, headers=headers,timeout=5)
        res.encoding = 'utf-8'
        html = res.text
        #直接调用解析函数
        self.parse_page(html)

      except Exception as e:
        self.blog += 1
        print('Retry')
        self.get_html(url)



  def parse_page(self, html):
    parse_html = etree.HTML(html)
    # li_list:[<element li at xxxx>,<element li at xxxx>]
    li_list = parse_html.xpath('//ul[@class="sellListContent"]/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]')
    item = {}
    for li in li_list:
      # 名称
      xpath_name = './/a[@data-el="region"]/text()'
      name_list = li.xpath(xpath_name)
      # if name_list:
      #   item['name'] = name_list[0].strip()
      # else:
      #   item['name'] = None
      # 列表推导式
      item['name'] = [name_list[0].strip() if name_list else None][0]

      # item['name'] = li.xpath()[0].strip()
      # 户型+面积+方位+是否精装
      info_xpath = './/div[@class="houseInfo"]/text()'
      info_list = li.xpath(info_xpath)
      if info_list:
        info_list = info_list[0].strip().split('|')
        if len(info_list)==5:
          item['model'] = info_list[1].strip()
          item['direction'] = info_list[3].strip()
          item['area'] = info_list[2].strip()
          item['perfect'] = info_list[4].strip()
        else:
          item['model']=item['area']=item['direction']=item['perfect']=None
      else:
        item['model']=item['area']=item['direction']=item['perfect']=None
      # 楼层
      xpath_floor = './/div[@class="positionInfo"]/text()'
      floor_list = li.xpath(xpath_floor)
      item['floor'] = [floor_list[0].strip().split()[0] if floor_list else None][0]
      # 地区
      item['address'] = li.xpath('.//div[@class="positionInfo"]/a/text()')[0].strip()
      # 总价
      item['total_price'] = li.xpath('.//div[@class="totalPrice"]/span/text()')[0].strip()
      # 单价
      item['unit_price'] = li.xpath('.//div[@class="unitPrice"]/span/text()')[0].strip()
      print(item)

  def main(self):
    for pg in range(1, 2):
      url = self.url.format(pg)
      self.get_html(url)
      time.sleep(random.randint(1, 2))


if __name__ == '__main__':
  start = time.time()
  l = LianjiaSpider()
  l.main()
  end = time.time()
  print('执行时间%d' % (end - start))
