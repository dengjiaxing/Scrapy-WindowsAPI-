# -*- coding: utf-8 -*-
import scrapy
import bs4
from bs4 import BeautifulSoup
import demjson
from selenium import webdriver
import argparse
import time
import os
from scrapy.http import HtmlResponse
from winAPI.items import  WinapiItem
from scrapy_redis.spiders import RedisSpider
# from scrapy.selector import Selector
# from scrapy.http import HtmlResponse
# from noval.items import  NovalItem
import re
#from scrapy_redis.spiders import RedisSpider

class novalSpider(scrapy.Spider):
    name = "api"
    allowed_domains=["msdn.microsoft.com"]
    path=r'D:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe'
    #allowed_domains = ["lagou.com/zhaopin/"]
    start_urls = ("https://social.msdn.microsoft.com/Search/zh-CN?query=")
    base_url="https://social.msdn.microsoft.com/Search/zh-CN?query="
    #item = NovalItem()
    def start_requests(self):
        fp=open("E:\\true_all_api.txt",'r')
        lines=fp.readlines()
        for line in lines:
            if line=='\n':
                continue
            api=line.strip('\n')
            driver=webdriver.PhantomJS(self.path)
            url=self.base_url+api
            driver.get(url)
            time.sleep(3)
            filename=api+'.html'
            fp = open(filename,'w')
            fp.write(driver.page_source)
            driver.quit()
            fp.close()
            #print query_url
            htmlfile = open(filename, 'r')
            the_page = htmlfile.read()
            htmlfile.close()
            data=BeautifulSoup(the_page,"html.parser")
            #new_url=''
            #non_result=data.find('div',{'id':'NoResultsContainer'})#  没有找到搜索项
            os.remove(filename)
            # if non_result:
            #     # item['APIName'] = ''
            #     # item['documentation'] =''
            #     # item['example'] =''
            #     # item['example_url']=''
            #     # yield item
            #     continue
            result_list=data.find_all('a',{'class':'resultTitleLink'})
            se=''
            for result in result_list:
                se=re.search(r'\sfunction\s',result.text)
                if se:
                    break
            if se:
                new_url=result.get('href')
                #item['APIName']=api
                #yield scrapy.Request(new_url,callback=self.parse,meta={'item':item})
                yield scrapy.Request(new_url, callback=self.parse, meta={'item_APIName': api})
            else:
                continue
            
    def parse(self, response):

        the_page=BeautifulSoup(response.body, 'html5lib')
        example=the_page.find_all('h2')


        for h in example:             #得到Examples下所有测试用例链接地址,存在一个函数有多种测试用例的情况
            if h.text=="Examples":
                nexts=h.next_siblings
                for tag in nexts:
                    if tag.string=="Requirements":
                        break
                    if type(tag)==bs4.NavigableString:         #判断是否为NavigableString类型,NavigableString类型标签不存在find等操作
                        continue
                    if isinstance(tag, bs4.Tag):
                        #item = response.meta['item']
                        link =tag.find_all('a')
                        for href in link:
                            item = WinapiItem()
                            item['documentation']=href.text
                            url=href.get('href')
                            #print url,href.text
                            api = response.meta["item_APIName"]
                            item["APIName"] = api
                            item['example_url']=url
                            print url
                            yield scrapy.Request(url, callback=self.parse_chapter,meta={'item':item})
    def parse_chapter(self,response):
        the_page=BeautifulSoup(response.body, 'html5lib')
        # example=the_page.find_all('div',class_='codeSnippetContainerCode')[-1]
        # item = response.meta['item']
        # print item
        # example_content=example.find('pre').text
        example = the_page.find_all('div', class_='codeSnippetContainerCode')
        i = -1
        item = response.meta['item']
        example_content=''
        while i >= -1*len(example):
            text = example[i].find('pre').text
            if re.search(r"#", text):
                example_content= text
                break
            else:
                i=i-1
        if example_content:
            item['example']=example_content
        else:
            item['example']=''
        yield item


