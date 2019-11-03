# -*- coding: utf-8 -*-
import requests
import scrapy
from lxml import etree
from scrapy_redis.spiders import RedisSpider


class DangdangSpider(RedisSpider):
    name = 'dangdangspider'
    redis_key = 'dangdangspider:urls'
    allowed_domains = ["dangdang.com"]
    start_urls = 'http://category.dangdang.com/?ref=www-0-C'

    def start_requests(self):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \
                      Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        yield scrapy.Request(url=self.start_urls, headers=headers, method='GET', callback=self.parse,
                             dont_filter=True)

    def parse(self, response):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \
                      Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        lists = response.body.decode('gbk')
        selector = etree.HTML(lists)
        goodslist = selector.xpath('//*[@ddt-pit="1"]//*[@class="classify_kind_name"]')
        for goods in goodslist:
            try:
                category_big = goods.xpath('a//text()').pop().replace(" ", "")  # 大种类
                category_big_id = goods.xpath('a/@href').pop().split('.')[3]  # id
                category_big_url = "http://category.dangdang.com/cp01.{}.00.00.00.00.html".format(
                    str(category_big_id))

                yield scrapy.Request(url=category_big_url, headers=headers, callback=self.detail_parse,
                                     meta={"ID1": category_big_id, "ID2": category_big}, dont_filter=True)
            except Exception:
                pass

    def detail_parse(self, response):
        '''
        ID1:大种类ID   ID2:大种类名称   ID3:小种类ID  ID4:小种类名称
        '''
        url = 'http://category.dangdang.com/cp01.{}.00.00.00.00.html'.format(response.meta["ID1"])
        category_small = requests.get(url)
        contents = etree.HTML(category_small.content.decode('gbk'))
        goodslist = contents.xpath('//*[@dd_name="分类"]//*[@class="list_right"]//span')
        for goods in goodslist:
            try:
                category_small_name = goods.xpath('a//text()').pop().replace(" ", "")
                category_small_id = goods.xpath('a/@href').pop().split('.')[2]

                category_small_url = "http://category.dangdang.com/pg1-cp01.{}.{}.00.00.00.html".format(str(response.meta["ID1"]), str(category_small_id))

                yield scrapy.Request(url=category_small_url, callback=self.third_parse,
                                     meta={"ID1": response.meta["ID1"],
                                           "ID2": response.meta["ID2"],
                                           "ID3": category_small_id,
                                           "ID4": category_small_name}, dont_filter=True)
            except Exception:
                pass


    def third_parse(self, response):
        print(response.meta["ID2"])
        print(response.meta["ID4"])
        for i in range(1, 20):
            url = 'http://category.dangdang.com/pg1-cp01.{}.{}.00.00.00.html'.format(str(i), response.meta["ID1"],
                                                                              response.meta["ID3"])
            try:
                page = requests.get(url)
                contents = etree.HTML(page.content.decode('gbk'))
                goodslist = contents.xpath('//*[@id="component_59"]/li')
                for goods in goodslist:
                    try:
                        bookurl = goods.xpath('a/@href')
                        print(bookurl)
                        yield scrapy.Request(url=bookurl, callback=self.book_parse,
                                             meta={"ID1": response.meta["ID1"],
                                                   "ID2": response.meta["ID2"],
                                                   "ID3": response.meta["ID3"],
                                                   "ID4": response.meta["ID4"]},
                                             dont_filter=True)
                    except Exception:
                        pass
            except Exception:
                pass


    def book_parse(self, response):
        print(response.meta["ID2"])
        print(response.meta["ID4"])
        lists = response.body.decode(encoding='utf-8', errors='replace')
        contents = etree.HTML(lists)
        content = contents.xpath('//*[@class="sale_box_left"]')
        for list in content:
            name = list.xpath('//*[@class="name_info"]')[0].xpath('//h1//text()').pop().replace(" ", "").replace("/n",
                                                                                                                 "")
            print(name)
            one = list.xpath('//*[@class="messbox_info"]')
            author = one[0].xpath('span//a//text()')[0]
            print(author)
            publisher = one[0].xpath('span//a//text()')[1]
            print(publisher)
            publishtime = one[0].xpath('span')[2].xpath('text()').pop().replace("出版时间:", "")
            print(publishtime)
            two = list.xpath('//*[@id="original-price"]')
            price = two[0].xpath('text()').pop().replace(" ", "").replace("/n", "")
            print(price)

        descrip = contents.xpath('//*[@id="content"]//*[@class="descrip"]')
        for list in descrip:
            descrip = list.xpath('p//text()')
            print(descrip)
