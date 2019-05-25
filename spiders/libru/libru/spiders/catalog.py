import scrapy
from libru.items import LibruItem


class CatalogSpider(scrapy.Spider):
    name = "catalog"

    def start_requests(self):
        urls = [
            'http://az.lib.ru/d/dostoewskij_f_m/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_text(self, response):
        yield LibruItem(file_urls=[response.urljoin(
            response.xpath('//a[contains(text(), "FB2")]').css('a::attr(href)').extract_first())])

    def parse(self, response):
        for text_ref in response.xpath('//a[contains(@href, "text_")]').css('a::attr(href)').extract():
            yield response.follow(text_ref, self.parse_text)
