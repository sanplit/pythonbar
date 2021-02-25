#-*- coding:utf-8 -*-
"""
@desc 抓取应用宝信息
@author Sanplit
"""

import io
import sys
import xlwt
import requests

class Spider(object):
    def __init__(self):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8') #改变标准输出的默认编码
        self.app_list = ['qq','微信','虎牙直播']
        self.sj_url = 'https://sj.qq.com/myapp/searchAjax.htm?kw='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }

    def get_code(self, url):
        response = requests.get(url, headers=self.headers)
        return response

    def write_in_excel(self, data = []):
        # 创建一个workbook 设置编码
        workbook = xlwt.Workbook(encoding = 'utf-8')
        # 创建一个worksheet
        worksheet = workbook.add_sheet(u'Subject Card',cell_overwrite_ok=True) 

        #设置表格样式 
        style = xlwt.easyxf('font: name Arial Black, colour_index black, bold on; align: wrap on, vert centre, horiz center;border:left thin, right thin, top thin, bottom thin')

        #创建复杂表头 write_merge(x, x + m, y, y + n, string, sytle) 
        #x表示行，y表示列，m表示跨行个数，n表示跨列个数，string表示要写入的单元格内容，style表示单元格样式。 
        #其中，x, y, m, n，都是以0开始计算的。 
        worksheet.write_merge(0,0,0,0,u'应用名称', style)
        worksheet.write_merge(0,0,1,1,u'公司', style)
        worksheet.write_merge(0,0,2,2,u'包名', style)
        worksheet.write_merge(0,0,3,3,u'评分', style)
        worksheet.write_merge(0,0,4,4,u'下载量', style)
        worksheet.write_merge(0,0,5,5,u'下载链接', style)

        # 二维列表写入excel
        for index,item in enumerate(data):
            for i in range(0, len(item)):
                # 参数对应 行, 列, 值
                worksheet.write(1+index, i, item[i])

        # 保存到当前目录
        workbook.save('appinfo.xls')

    def run(self):
        # 有序列表
        res = list()

        for i in range(0, len(self.app_list)):
            cur_url = self.sj_url+self.app_list[i]
            print(cur_url)

            code = self.get_code(cur_url)
            data = self.get_code(cur_url).json()

            tmp = []
            #取搜索的第一项，可自由选择
            tmp.append(data['obj']['items'][0]['appDetail']['appName'])
            tmp.append(data['obj']['items'][0]['appDetail']['authorName'])
            tmp.append(data['obj']['items'][0]['appDetail']['pkgName'])
            tmp.append(round(data['obj']['items'][0]['appDetail']['averageRating'], 2))
            tmp.append(round(data['obj']['items'][0]['appDetail']['appDownCount'], 2))
            tmp.append(data['obj']['items'][0]['appDetail']['apkUrl'])

            res.append(tmp)
        
        print(res)
        self.write_in_excel(res)

spider = Spider()
spider.run()
