import requests
import json
import time
import random
from useragents import ua_list
from multiprocessing import Process
from queue import Queue


class TencentSpider():
  def __init__(self):
    self.one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1563912271089&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
    self.two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1563912374645&postId={}&language=zh-cn'
    self.q = Queue()

  # 获取相应内容的函数
  def get_page(self, url):
    headers = {'User-Agent': random.choice(ua_list)}
    html = requests.get(url=url, headers=headers).text
    # json格式字符串->python
    html = json.loads(html)
    return html

  # 主线函数:获取所有数据
  def parse_page(self):
    while True:
      if not self.q.empty():
        one_url=self.q.get()
        html = self.get_page(one_url)
        item = {}
        for job in html['Data']['Posts']:
          # 名称
          item['name'] = job['RecruitPostName']
          # postId
          post_id = job['PostId']
          # 拼接二级地址,获取职责和要求
          two_url = self.two_url.format(post_id)
          item['duty'], item['requirement'] = self.parse_two_page(two_url)
          print(item)
      else:
        break
  # 解析二级页面函数
  def parse_two_page(self, two_url):
    html = self.get_page(two_url)
    # replace处理特殊字符
    # 职责
    duty = html['Data']['Responsibility']
    duty = duty.replace('\r\n', '').replace('\n', '')
    # 要求
    require = html['Data']['Requirement']
    require = require.replace('\r\n', '').replace('\n', '')
    return duty, require

  # 获取总页数
  def get_number(self):
    url = self.one_url.format(1)
    html = self.get_page(url)
    number = (html['Data']['Count']) // 10 + 1
    return number

  def main(self):
    #url先入队列
    number = self.get_number()
    for page in range(1, number+1):
      one_url = self.one_url.format(page)
      self.q.put(one_url)
    t_list=[]
    for i in range(5):
      t= Process(target=self.parse_page)
      t_list.append(t)
      t.start()
    for t in t_list:
      t.join()
      # self.parse_page(one_url)


if __name__ == '__main__':
  s = TencentSpider()
  s.main()
