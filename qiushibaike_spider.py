import requests
from lxml import etree
from useragents import ua_list
import random
import time


class QiushiSpider():
  def __init__(self):
    self.url = 'https://www.qiushibaike.com/text/page/{}/'
    self.num = 0

  def get_html(self, url):
    html = requests.get(
      url=url,
      headers={
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}
    ).content.decode('utf=8', 'ignore')
    # print(html)
    self.parse_page(html)

  def xpath_func(self, html, xpath_dbs):
    parse_html = etree.HTML(html)
    r_list = parse_html.xpath(xpath_dbs)
    return r_list

  def parse_page(self, html):

    xpath_dbs = './/div[@class="col1"]/div'
    r_list = self.xpath_func(html,xpath_dbs)
    #print(r_list)  # [/p/6211946198', '/p/6223280220','',''..]

    item = {}
    if r_list:
      for r in r_list:
        try:
          user_xpath='.//div[@class="author clearfix"]/a[2]/h2/text()'
          item['用户名'] = r.xpath(user_xpath)[0].strip()
        except Exception as e:
          item['用户名'] ='匿名用户'
        # 好笑数
        smile_xpath = './/div[@class="stats"]/span/i/text()'
        item['好笑数'] = r.xpath(smile_xpath)[0].strip()
        # 评论
        review_xpath = './/div[@class="stats"]/span[2]/a/i/text()'
        item['评论数'] = r.xpath(review_xpath)[0].strip()
        # 内容
        content_xpath = './/div[@class="content"]/span/text()'
        item['内容'] = r.xpath(content_xpath)[0:-1]
        print(item)

        self.num += 1
    print('共抓取数据', self.num, "部")
  def main(self):
    for offset in range(1, 2):
      url = self.url.format(offset)

      self.get_html(url)
      time.sleep(random.randint(1, 2))



if __name__ == '__main__':
  start = time.time()
  spider = QiushiSpider()
  spider.main()
  end = time.time()
  print('执行时间:%.2f' % (end - start))
