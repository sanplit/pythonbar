#-*- coding:utf-8 -*-

import re
import requests

from lxml import etree
from bs4 import BeautifulSoup


class Spider(object):
    def __init__(self):
        # self.tb_url = 'https://dahua.m.tmall.com'
        self.tb_url = 'https://market.m.taobao.com/app/tb-source-app/shop-auction/pages/auction?_w&sellerId=2201404549418&shopId=315821385&dynamicCard=true&crowdRights=true&disablePromotionTips=true&shop_navi=allitems&displayShopHeader=true'
        # self.tb_url = 'https://dahua.tmall.com/search.htm?spm=a1z10.1-b-s.w5001-22753675625.5.5a5026bdnY9SeR&scene=taobao_shop'
        self.headers = {
            'Referer': 'https://m.taobao.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }

    def get_code(self, url):
        response = requests.get(url, headers=self.headers).content.decode('utf-8')
        return response

    def run(self):
        print('******************* Wait a minute.It has begun. ****************************')

        code = self.get_code('https://h5api.m.taobao.com/h5/mtop.taobao.wsearch.appsearch/1.0/?jsv=2.5.1&appKey=12574478&t=1618993349808&sign=e10cfe64592d7d3ed337e51a3a6bdc93&api=mtop.taobao.wsearch.appSearch&v=1.0&H5Request=true&AntiCreep=true&type=jsonp&timeout=3000&dataType=jsonp&callback=mtopjsonp1&data=%7B%22m%22%3A%22shopitemsearch%22%2C%22vm%22%3A%22nw%22%2C%22sversion%22%3A%224.6%22%2C%22shopId%22%3A%22315821385%22%2C%22sellerId%22%3A%222201404549418%22%2C%22style%22%3A%22wf%22%2C%22page%22%3A%221%22%2C%22sort%22%3A%22_coefp%22%2C%22catmap%22%3A%22%22%2C%22wirelessShopCategoryList%22%3A%22%22%7D')  #确定抓取起始页
        print('----code--------')
        print('----code--------', code)
        
        res = re.search(r'"data":(.*?)}};', code)
        print('----code--------', res)

        soup = BeautifulSoup(code, 'lxml')

        print('----detail href----')
        tag = soup.find_all('div', attrs={'target', '_parent'})

        for x in tag:
            cur_href = x.get('href')
            print(cur_href)

spider = Spider()
spider.run()