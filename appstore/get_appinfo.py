#-*- coding:utf-8 -*-
"""
@desc 抓取应用宝信息 顺便比较re、etree、BeautifulSoup
	  参考： https://blog.csdn.net/qq_39610888/article/details/81262193
@author Sanplit
"""

import re
import requests
from lxml import etree
from bs4 import BeautifulSoup

class Spider(object):
    def __init__(self):
        self.app_list = ['qq','微信','虎牙直播']
        self.js_url = 'https://sj.qq.com/myapp/search.htm?kw='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }

    def get_code(self, url):
        response = requests.get(url, headers=self.headers).content
        return response

    def use_re(self, code):
        pattern = re.compile(r'<li class="d_name".*?<a.*?>(.*?)</a>'
                             r'.*?<cc.*?class="d_post_content j_d_post_content ">(.*?)</div>', re.S)
        result = re.findall(pattern, code)
        pattern = re.compile(r'<.*?>|<br>|</a>', re.S)
        for name, content in result:
            new_name = re.sub(pattern, '', name)
            new_name = pattern.sub('', name)
            # 两种写法
            new_content = re.sub(pattern, '', content)
            print(new_content)

    def use_soup(self, code):
        soup = BeautifulSoup(code, 'lxml')

        print('----href----')
        for x in soup.find_all('a'):
            print(x.get('href'))

        print('----text----')
        print(len(soup.findAll(text=re.compile('QQ'))))
        #for x in soup.find_all("a", {"class": "appName"}):
        for x in soup.findAll('span') :
            print(x.get_text())

        name = soup.select('#J_SearchDefaultListBox > li:nth-child(1) > div.search-boutique-data > div.data-box > div.name-line > div.name > a')
        for new in name:
            print(new.get_text())

        content = soup.select('cc div')
        for new in content:
            print(new.get_text())

    def use_xpath(self, code):
        new_code = etree.HTML(code)
        print(new_code)
        print(len(new_code))
        #name = new_code.xpath('//*[@id="article"]/header/h1/text()')
        name = new_code.xpath('//*[@id="J_SearchDefaultListBox"]/li[1]/div[1]/div[2]/div[1]/div[1]/a/text()')
        print(name)
        for new in name:
            print(new.replace(' ', '').strip('\n'))
        content = new_code.xpath('//cc/div[@class="d_post_content j_d_post_content "]//text()')
        for new in content:
            print(new)

    def run(self):
        cur_url = self.js_url+'qq'
        print(cur_url)
        #code = self.get_code('http://sanplit.cn/archives/5/')
        code = self.get_code(cur_url)
        self.use_soup(code)
        #self.use_xpath(code)

spider = Spider()
spider.run()
