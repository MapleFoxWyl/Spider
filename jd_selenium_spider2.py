import requests
from selenium import webdriver
import time


class JdSpider():
  def __init__(self):
    self.url = 'https://www.jd.com'
    #设置无界面浏览器
    self.options = webdriver.ChromeOptions()
    self.options.add_argument('--headless')
    #正常创建浏览器对象即可
    self.browser = webdriver.Chrome(options=self.options)
  # 获取页面信息
  def get_html(self):
    self.browser.get(self.url)
    # 搜索框
    self.browser.find_element_by_xpath('//*[@id="key"]').send_keys('爬虫书')
    # 搜索按钮
    self.browser.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click()
    time.sleep(2.3)
    # 添加计数
    self.i = 0

  # 解析页面
  def parse_html(self):
    #把进度条拉倒底部,是所有数据动态加载
    self.browser.execute_script(
      'window.scrollTo(0,document.body.scrollHeight)'
    )
    #等待动态数据加载完成
    time.sleep(2)
    item = {}
    # 先提取所有商品节点对象列表,li列表
    li_list = self.browser.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li')
    for li in li_list:
      # find_element
      item['name'] = li.find_element_by_xpath('.//div[@class="p-name"]/a/em').text.strip()
      item['price'] = li.find_element_by_xpath('.//div[@class="p-price"]').text.strip()
      item['comment'] = li.find_element_by_xpath('.//div[@class="p-commit"]/strong').text.strip()
      item['shop'] = li.find_element_by_xpath('.//div[@class="p-shopnum"]').text.strip()
      print(item)
      self.i += 1

  def main(self):
    self.get_html()
    while True:
      self.parse_html()
      # 判断是否为最后一页
      if self.browser.page_source.find('pn-next disabled') == -1:
        self.browser.find_element_by_class_name('pn-next').click()
        time.sleep(2)
      else:
        break
    print('数量', self.i)

    self.browser.quit()

if __name__ == '__main__':
  jd = JdSpider()
  jd.main()
