from urllib import request
from urllib import parse
import time
import random
from useragents import ua_list


class BaiduSpider(object):
  def __init__(self):
    self.url = 'http://tieba.baidu.com/f?kw={}&pn={}'

  # 获取相应内容
  def get_html(self, url):
    headers = {
      'User-Agent': random.choice(ua_list)
    }
    req = request.Request(url=url, headers=headers)
    res = request.urlopen(req)
    html = res.read().decode('utf-8')
    print(headers)
    return html

  # 解析相应内容(提取所需数据)
  def parse_html(self):
    pass

  # 保存
  def write_html(self, filename, html):
    with open(filename, 'w', encoding='utf-8') as f:
      f.write(html)

  # 主函数
  def main(self):
    # 拼接每一页的地址
    # 接收用户的输入(例如贴吧名,第几页)
    name = input('请输入贴吧名:')
    begin = int(input('请输入起始页'))
    end = int(input('请输入终止页'))
    # url 缺两个数据: 贴名吧  pn
    params = parse.quote(name)
    for page in range(begin, end + 1):
      pn = (page - 1) * 50
      url = self.url.format(params, pn)
      filename = '{}-第{}页.html'.format(name, page)

      # 调用类内函数
      html = self.get_html(url)
      self.write_html(filename, html)
      # 每爬取1个页面随机休眠1-3秒钟
      time.sleep(random.randint(1, 3))
      print('第%d页爬取完成' % page)


if __name__ == '__main__':
  start = time.time()
  spider = BaiduSpider()
  spider.main()
  end = time.time()
  print('执行时间:%.2f' % (end-start))
