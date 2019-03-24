# -*- coding: utf-8 -*-
import scrapy
from ScrapyTest.items import ScrapytestItem


class DoubanSpiderSpider(scrapy.Spider):
    #爬虫名字
    name = 'douban_spider'
    #允许的域名
    allowed_domains = ['movie.douban.com']
    #入口URL
    start_urls = ['http://movie.douban.com/top250']
    #默认解析方法
    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for i_item in movie_list:
            doubanitem = ScrapytestItem()
            doubanitem['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            doubanitem['movie_name'] = i_item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            content =  i_item.xpath(".//div[@class='info']/div[@class='bd']/p[1]/text()").extract()
            for i_content in content:
                content_s = "".join(i_content.split())
                doubanitem['introduce'] = content_s
            doubanitem['star'] = i_item.xpath(".//span[@class='rating_num']/text()").extract_first()
            doubanitem['evaluate'] = i_item.xpath(".//div[@class='star']/span[4]/text()").extract_first()
            doubanitem['describe'] = i_item.xpath(".//p[@class='quote']/span/text()").extract_first()
            yield doubanitem
        #解析下一页
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250" + next_link,callback=self.parse)
