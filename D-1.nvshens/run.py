#-*- coding:utf-8 -*-
"""
@desc 抓个美女图吧 顺便比较re、etree、BeautifulSoup
@author Sanplit
"""

import os
import re
import requests
from lxml import etree
from bs4 import BeautifulSoup

class Spider(object):
    def __init__(self):
        self.request_url = 'https://www.nvshens.org'    #福利地址
        self.headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }

    #解码URL获取网页的源码
    def get_code(self, url):
        response = requests.get(url, headers=self.headers).content.decode('utf-8')
        return response

    #目录是否存在，不存在则创建
    def create_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            if os.path.isfile(path):
                os.mkdir(path)
    #保存图片
    def save_img(self, img_list, path = './imgs/'):
        self.create_dir(path)
        imgIndex = 1
        print('------ Download Start ------- ')
        for img_url in img_list:
            header = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Host': 't1.onvshen.com:85',
                'Referer': 'https://www.nvshens.org/gallery/'
            }

            try:
                #这里获取图片header是必须的
                response = requests.get(img_url, headers=header, allow_redirects=False, stream=True)

                filename = path+str(imgIndex)+'.jpg'
                if response.status_code == 200:
                    with open(filename, "wb") as f:
                        f.write(response.content) # 将内容写入图片

                imgIndex += 1
            except:
                print('failed"')

        print('------ Download Over ------- Count: ',imgIndex-1)

    def use_re(self, code):
        href_list = re.findall(r"<a class='galleryli_link' href='(.*?)'", code)

        print('----detail href----')
        for href in href_list:
            print(self.request_url+href)

            new_code2 = self.get_code(self.request_url+href)

            title = re.findall(r'<h1 id="htilte">(.*?)</h1>', new_code2)[0]

            pattern = re.compile(r"<img src='(.*?)'", re.S)
            # 第一页图片
            first_img = re.findall(pattern, new_code2)

            # 所有页 由于页数会变动，所有不准
            pages = re.findall(r'>(\d)</a>', new_code2)

            flen = len(first_img)
            img_list = first_img
            # for pi in range(1,len(pages)):
            for pi in range(1,20):    # 抓取20页,从第二页开始
                for ii in range(flen):
                    name_str = str(flen*pi+ii) if flen*pi+ii >= 10 else '0'+str(flen*pi+ii)
                    #将匹配到的数字替换成对应数,替换1个
                    tmp = re.sub('/\d{3}.jpg', '/0'+name_str+'.jpg', first_img[1], 1)
                    img_list.append(tmp)

            self.save_img(img_list, './imgs/'+title+'/')

    def use_soup(self, code):
        soup = BeautifulSoup(code, 'lxml')

        print('----detail href----')
        tag = soup.find_all('a', attrs={'class', 'galleryli_link'})
        for x in tag:
            cur_href = self.request_url+x.get('href')
            print(cur_href)

            soup2 = BeautifulSoup(self.get_code(cur_href), 'lxml')
            img1 = soup2.select('#hgallery img')

            # 获取分页
            total_page = soup2.select('#pages a')
            #去掉第一个（上一页）和最后一个（下一页）元素
            del(total_page[0])
            total_page.pop()

            for page in total_page:
                print('第'+page.text+'页')
                soup3 = BeautifulSoup(self.get_code(cur_href+page.text+'.html'), 'lxml')
                img1 += soup3.select('#hgallery img')

            img_list = []
            for index,item in enumerate(img1):
                img_list.append(item.get('src'))

            self.save_img(img_list, './imgs/'+soup2.find(id='htilte').text+'/')

    def use_xpath(self, code):
        #解析成xml
        new_code = etree.HTML(code)
        #在xml中定位节点，返回的是一个列表
        tag = new_code.xpath('//*[@id="listdiv"]/ul/li/*/a/@href')

        print('----detail href----')
        for index in range(len(tag)):
            print(self.request_url+tag[index])

            new_code2 = etree.HTML(self.get_code(self.request_url+tag[index]))
            tag2 = new_code2.xpath('//*[@id="hgallery"]/img')

            img_list = []
            for i in tag2:
                img_list.append(i.xpath('@src')[0])

            self.save_img(img_list, './imgs/'+new_code2.xpath('//*[@id="htilte"]/text()')[0]+'/')

    def run(self):
        code = self.get_code(self.request_url+'/gallery/')  #确定抓取起始页
        self.use_soup(code)
        # self.use_xpath(code)
        # self.use_re(code)

spider = Spider()
spider.run()
