from scrapy.spiders import Spider
from scrapy.selector import Selector
from rym.items import ChartRow

class ChartSpider(Spider):
    name = "rym-chart"
    allowed_domains = ["googleusercontent.com"]
    start_urls = [
    "http://webcache.googleusercontent.com/search?q=cache:9YX_RJYDDOEJ:rateyourmusic.com/customchart+&cd=1&hl=en&ct=clnk&gl=us"
    ]

    def parse(self, response):
        # get listitems
        sel = Selector(response)
        table = sel.xpath('//table[@class="mbgen"]')
        rows = table.xpath(".//tr")
        for row in rows:
            item = ChartRow()
            item['artist'] = row.xpath('.//td/div/span/a[@class="artist"]/text()').extract_first()
            item['artist_url'] = row.xpath('.//td/div/span/a[@class="artist"]/@href').extract_first()
            item['title'] = row.xpath('.//td/div/span/a[@class="album"]/text()').extract_first()
            item['title_url'] = row.xpath('.//td/div/span/a[@class="album"]/@href').extract_first()
            item['cover_art'] = row.xpath('.//td/a/img[@class="delayloadimg"]/@src').extract_first()
            item['genres']= row.xpath('.//td/div/a[@class="genre"]/text()').extract()
            item['position'] = row.xpath('.//td/span[@class="ooookiig"]/text()').extract_first()
            item['release_year'] = row.xpath('.//td/div/span[@class="mediumg"]/text()').extract_first()
            yield item
