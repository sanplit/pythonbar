#-*- coding:utf-8 -*-
import requests     # 发送请求
import re
from lxml import etree

# 伪装
headers = {
    'cookie': '_yep_uuid=b1421b7f-11da-b15f-a3ad-95316478f93c; e1=%7B%22pid%22%3A%22qd_P_read%22%2C%22eid%22%3A%22%22%2C%22l1%22%3A3%7D; e2=%7B%22pid%22%3A%22qd_P_read%22%2C%22eid%22%3A%22%22%2C%22l1%22%3A3%7D; newstatisticUUID=1648708045_1995757040; _csrfToken=mAWbsvESMNwir4NfKBy5fy8RedwvNBabTq3PLx6r; fu=721555856; _gid=GA1.2.1193345906.1648708045; e1=%7B%22pid%22%3A%22qd_p_qidian%22%2C%22eid%22%3A%22qd_A18%22%2C%22l1%22%3A3%7D; e2=; qdrs=0%7C3%7C0%7C0%7C1; showSectionCommentGuide=1; qdgd=1; rcr=1031788647%2C1031920667; bc=1031920667%2C1031788647; pageOps=1; lrbc=1031788647%7C686160165%7C0%2C1031920667%7C695153167%7C1; _ga_FZMMH98S83=GS1.1.1648708044.1.1.1648708759.0; _ga_PFYW0QLV3P=GS1.1.1648708044.1.1.1648708759.0; _ga=GA1.2.777546916.1648708045',
    'referer': 'https://www.kankan365.cc/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
}
url = 'https://www.kankan365.cc/read/73867.html'
html_data = requests.get(url=url, headers=headers).text.encode('utf-8').decode('utf-8')
# info_list = re.findall(r'<div class="book-chapter-list"><ul class="cf"><li><a href="(.*?)">(.*?)</a></li></ul></div>', html_data, re.S)

#解析成xml
new_code = etree.HTML(html_data)
#在xml中定位节点，返回的是一个列表
info_list = new_code.xpath('//*[@id="list"]/div[3]/ul[2]/li/a/@href')

for index, link in info_list:
    tag1,tag2,tag3,tag4 = link.split('/', 3)

    print('第'+str(index + 1)+'篇: ', tag4)

    pageid,ext = tag4.split('.')
    link = 'https://www.kankan365.cc/files/article/html555/136/136583/'+str(pageid)+'.html'
    print(link)

    # 1. 发送请求
    response = requests.get(url=link, headers=headers)
    # 2. 获取数据
    link_data = response.text

    text = link_data.replace('<br><br>', '\n')
    text = text.replace('&nbsp;&nbsp;', '')

    text = re.sub(r'茵右脚楞夺','的', text);
    text = re.sub(r'顺困顶枯枵','是', text);
    text = re.sub(r'顶置中夺粗功肖功地','有', text);
    text = re.sub(r'夺回顾功带困','，', text);

    # 4. 保存数据
    with open('名侦探世界的警探.txt', mode='a', encoding='utf-8') as f:
        f.write(text)
