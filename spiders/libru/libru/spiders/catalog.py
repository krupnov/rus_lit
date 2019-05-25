import scrapy
from libru.items import LibruItem


class CatalogSpider(scrapy.Spider):
    name = "catalog"

    def start_requests(self):
        urls = [
            'http://az.lib.ru/a/abramowich_n_j/text_1914_hristos_dostoevskago_oldorfo.shtml',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield LibruItem(file_urls=[response.urljoin(
            response.xpath('//a[contains(text(), "FB2")]').css('a::attr(href)').extract_first())])
