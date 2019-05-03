# -*- coding: utf-8 -*-
# @Data : 2019-05-03 10:20
# @Author : 小酒窝
# @Software : PyCharm
import time
import requests
from fake_useragent import UserAgent
from lxml import etree


class MZTSpider:
    def __init__(self):
        self.parse_url = 'https://www.mzitu.com/xinggan/'
        self.ua = UserAgent()
        self.headers = {
            "host": "api.meizitu.net",
            "Referer": "https://app.mmzztt.com",
            "user-agent": "Mozilla/5.0 (Linux; Android 9; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/72.0.3626.121 Mobile Safari/537.36"
        }
        self.num = 1
    def get_html(self,url):
        r = requests.get(url,self.headers)
        r.encoding = 'utf-8'
        time.sleep(1)
        html = r.text
        parseHTML = etree.HTML(html)
        rList = parseHTML.xpath("//div[@class='postlist']/ul[@id='pins']//li")
        for r in rList:
            if r.xpath('./a/@href'):
                link = r.xpath('./a/@href')[0]
            else:
                link = ""
            if r.xpath('./span/a/text()'):
                content = r.xpath('./span/a/text()')[0]
            else:
                content = ""
            if r.xpath('./span[2]/text()'):
                release_data = r.xpath('./span[2]/text()')[0]
            else:
                release_data = ''
            print(link, content)
            self.get_page(link,content)
    def get_page(self,link,content):
        time.sleep(1)
        self.headers__ ={
            "Referer":link,
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        }
        r = requests.get(link,headers=self.headers__)
        r.encoding = 'utf-8'
        parseHTML = etree.HTML(r.text)
        try:
            page_index = parseHTML.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
        except:
            print("未找到图片最大页码")
        print(content+"共{}张图片".format(page_index))
        parse_url = parseHTML.xpath('//div[@class="main-image"]/p/a/img/@src')[0].split('01.jpg')[0]
        for _ in range(1, int(page_index)+1):
            if _ < 10:
                page_url = parse_url + '0' + str(_) + '.jpg'
            else:
                page_url = parse_url + str(_) + '.jpg'
            self.write_page(page_url,content,_)


        # self.write_page(link,page_index,content)
    def write_page(self,page_url,content,page_index):
        html = requests.get(page_url,headers=self.headers__).content
        filename = "D:\项目\MTZPP\image\\" + content + "[" +str(page_index) + "].jpg"
        with open(filename, 'wb') as file:
            file.write(html)
            print(f"已下载{self.num}张妹纸图片")
            self.num += 1


    def main(self):
        self.get_html(self.parse_url)

if __name__ == '__main__':
    spider = MZTSpider()
    spider.main()

