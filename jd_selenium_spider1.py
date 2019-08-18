import requests
from selenium import webdriver
import time
class JdSpider():
  def __init__(self):
    self.url = 'https://www.jd.com'
    self.browser = webdriver.Chrome()
  #获取页面信息
  def get_html(self):
    self.browser.get(self.url)
    #搜索框
    self.browser.find_element_by_xpath('//*[@id="key"]').send_keys('爬虫书')
    #搜索按钮
    self.browser.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click()
    time.sleep(2.3)
  #解析页面
  def parse_html(self):
    #先提取所有商品节点对象列表,li列表
    li_list = self.browser.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li')
    for li in li_list:
      print("*"*10)
      # print(li.text) #先打印看看规律
      info_list = li.text.split('\n')
      if info_list[0].startswith('每满') or info_list[1].startswith('￥'):
        price = info_list[1]
        name = info_list[2]
        comment = info_list[3]
        shop = info_list[4]
      elif info_list[0].startswith('单价'):
        price = info_list[3]
        name = info_list[4]
        comment = info_list[5]
        shop = info_list[6]
      else:
        price = info_list[0]
        name = info_list[1]
        comment = info_list[2]
        shop = info_list[3]
      print(price)
      print(comment)
      print(shop)
      print(name)
  def main(self):

    self.get_html()
    self.parse_html()

if __name__ == '__main__':
    jd =JdSpider()
    jd.main()