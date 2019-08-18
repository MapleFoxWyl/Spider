import requests
from lxml import etree
import re
import pymysql
class GovmentSpider():
  def __init__(self):
    self.url = 'http://www.mca.gov.cn/article/sj/xzqh/2019/'
    self.headers={'User-Agent':'Mozilla/5.0'}
    self.db = pymysql.connect(
      '127.0.0.1','root','123456','govdb',charset='utf8'
    )
    self.cursor = self.db.cursor()
  #获取假链接
  def get_false_link(self):
    html = requests.get(
      url=self.url,
      headers = self.headers,
    ).text  #等于content.decode()
    #解析
    parse_html = etree.HTML(html)
    print(parse_html)  #网页对象
    a_list = parse_html.xpath('//a[@class="artitlelist"]')
    for a in a_list:
      #titel = a.xpath('./@titel')[0]
      #get()方法:获取某个属性的值
      title = a.get('title')
      if title.endswith('代码'):#末尾以代码结束的
        false_link = 'http://www.mca.gov.cn'+a.get('href')
        break
    # if false_link 在数据库表中没有:
    #   self.get_true_link(false_link)
    #   把链接插入到数据库中
    # else:
    #   print('数据已经是最新,无需爬取')
    self.incr_spider(false_link)
  #增量爬取函数
  def incr_spider(self, false_link):
    sel = 'select url from version '
    self.cursor.execute(sel)
    # fetchall:(('http://xxx.html',),)
    result = self.cursor.fetchall()
    # not result:代表数据库version表中无数据
    if not result:
      self.get_true_link(false_link)
      #可选操作:数据库version表中只保留最新一条数据
      del_ = 'delete from version'
      self.cursor.execute(del_)
      # 把爬取后的url插入到version
      ins = 'insert into version values(%s)'
      self.cursor.execute(ins, [false_link])
      self.db.commit()
    else:
      print('数据已经是最新,无需爬取')

  #获取真链接
  def get_true_link(self,false_link):
    #先获取加链接的响应,然后根据响应获取真链接
    html = requests.get(
      url=false_link,
      headers=self.headers
    ).text
    #利用正则提取真是链接
    re_bds = r'window.location.href="(.*?)"'
    pattern = re.compile(re_bds,re.S)
    # 打印看看是否成功爬取头
    # print(html)
    # with open('false_link.html','a') as f:
    #   f.write(html)
    true_link = pattern.findall(html)[0]
    self.save_data(true_link)
    # print(true_link)


  #提取数据
  def save_data(self,true_link):
    html = requests.get(
      url = true_link,
      headers = self.headers
    ).text
    #xpath提取数据
    parse_html = etree.HTML(html)
    tr_list = parse_html.xpath('.//tr[@height="19"]')
    for tr in tr_list:
      code = tr.xpath('./td[2]/text()')[0].strip()
      name=tr.xpath('./td[3]/text()')[0].strip()
      print(name,code)


  def main(self):
    self.get_false_link()

if __name__ == '__main__':
    spider=GovmentSpider()
    spider.main()