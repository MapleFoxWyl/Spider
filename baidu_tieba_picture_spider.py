import requests
from lxml import etree
import random
import time
from useragents import ua_list
from urllib import parse


class BaiduImageSpider():
  def __init__(self):
    self.url = 'http://tieba.baidu.com/f?kw={}&pn={}'

  # 获取html功能函数
  def get_html(self, url):
    html = requests.get(
      url=url,
      headers = {
      'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}
    ).content.decode('utf=8','ignore')
    print(html)
    return html

  # 解析html功能函数
  def xpath_func(self, html, xpath_dbs):
    parse_html = etree.HTML(html)
    r_list = parse_html.xpath(xpath_dbs)
    return r_list

  # 解析函数-实现最终的图片抓取
  def parse_html(self, one_url):
    html = self.get_html(one_url)
    # 准备提取帖子链接:xpath_list ['/p/323232','','']
    xpath_dbs = '//div[@class="author clearfix"]/div/a/h2/a/@href'
    r_list = self.xpath_func(html, xpath_dbs)
    print(r_list) #[/p/6211946198', '/p/6223280220','',''..]
    for r in r_list:
      # 拼接帖子的URL地址
      t_url = 'http://tieba.baidu.com' + r
      # 把帖子中所有图片保存到本地
      self.get_image(t_url)
      time.sleep(random.uniform(0,1))

  # 给定1个帖子URL,把帖子中所有图片保存到本地
  def get_image(self, t_url):
    html = self.get_html(t_url)
    xpath_dbs = '//div[@class="d_post_content j_d_post_content  clearfix"]/img[@class="BDE_Image"]/@src'
    img_list = self.xpath_func(html, xpath_dbs)
    for img in img_list:
      html_bytes = requests.get(
        url=img,
        headers={'User-Agent': random.choice(ua_list)}
      ).content
      self.save_img(html_bytes, img)

  # 保存图片函数
  def save_img(self, html_bytes, img):
    filename = img[-10:]
    with open(filename, 'wb') as f:
      f.write(html_bytes)
      print('%s下载成功' % filename)

  # 主函数
  def main(self):
    name=input('请输入贴吧名:')
    begin = int(input('请输入起始页:'))
    end = int(input('请输入终止页:'))
    kw = parse.quote(name)
    for page in range(begin,end+1):
      pn=(page-1)*50
      url = self.url.format(kw,pn)
      self.parse_html(url)




if __name__ == '__main__':
  spider = BaiduImageSpider()
  spider.main()
