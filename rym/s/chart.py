from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
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
        content = []

        for row in rows:
          if len(row.xpath('.//td')) == 3:
            content.append(row) 

        for row in content:
            item = ChartRow()
            item['chart_position'] = row.xpath('.//td/span[@class="ooookiig"]/text()').extract_first()
            item['title_url'] = row.xpath('.//td/div/span/a[@class="album"]/@href').extract_first()
            item['cover_art_icon'] = row.xpath('.//td/a/img[@class="delayloadimg"]/@data-delayloadurl').extract_first()
            if item['title_url'] is not None:
              url = "http://webcache.googleusercontent.com/search?q=cache:rateyourmusic.com"+item['title_url'].strip()+"+&cd=2&hl=en&ct=clnk&gl=us"
              request = Request(url, self.parse_album)
              request.meta['item'] = item
            yield request

    def parse_album(self, response):
        item = response.meta['item']
        sel = response.xpath('//*[contains(concat(" ", normalize-space(@class), " "), " section_main_info ")]')
        # basic
        album_info = sel.xpath('.//table[@class="album_info"]')
        ranking = album_info.xpath('.//tr')[5].xpath('.//td')
        # album info
        item['artist'] = album_info.xpath('.//a[@class="artist"]/text()').extract_first().strip()
        item['cover_art'] = sel.xpath('.//img[@class="coverart_img"]/@src').extract_first().strip()
        item['descriptors'] = album_info.xpath('.//tr[@class="release_descriptors"]/td/meta/@content').extract()
        item['genres'] = album_info.xpath('.//tr[@class="release_genres"]/td/div/span[@class="release_pri_genres"]/a/text()').extract()
        item['media'] = album_info.xpath('.//tr')[1].xpath('.//td/text()').extract_first()
        item['ranks'] =  ranking.xpath('.//b/text()').extract()
        item['rating'] = album_info.xpath('.//tr')[4].xpath('.//td/span/span[@class="avg_rating"]/text()').extract_first().strip()
        item['recorded'] = album_info.xpath('.//tr')[3].xpath('.//td/text()').extract_first().strip()
        item['release_date'] = album_info.xpath('.//tr')[2].xpath('.//td/text()').extract_first().strip()
        item['release_year'] = album_info.xpath('.//tr')[2].xpath('.//td/a/b/text()').extract_first().strip()
        item['subgenres'] = album_info.xpath('.//tr[@class="release_genres"]/td/div/span[@class="release_sec_genres"]/a/text()').extract()
        item['title'] = sel.xpath('.//div[@class="album_title"]/text()').extract_first().strip()
        item['url'] = response.url
        item['votes'] = album_info.xpath('.//tr')[4].xpath('.//td/span/span[@class="num_ratings"]/b/span/text()').extract()

        return item
