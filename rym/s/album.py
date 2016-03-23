from scrapy.spiders import Spider
from scrapy.selector import Selector
from rym.items import Album

class AlbumSpider(Spider):
    name = "rym-album"
    allowed_domains = ["googleusercontent.com"]
    start_urls = [
        "http://webcache.googleusercontent.com/search?q=cache:lRJdp7maW-4J:rateyourmusic.com/release/album/the_beatles/revolver/+&cd=1&hl=en&ct=clnk&gl=us"
    ]

    def __init__(self, *args, **kwargs): 
        super(AlbumSpider, self).__init__(*args, **kwargs) 
        self.start_urls = [kwargs.get('start_url')] 

    def parse(self, response):
        sel = response.xpath('//*[contains(concat(" ", normalize-space(@class), " "), " section_main_info ")]')
        album_info = sel.xpath('.//table[@class="album_info"]').xpath('.//tr')
        # basic
        item = Album()
        item['artist'] = sel.xpath('.//a[@class="artist"]/text()').extract_first()
        item['cover_art'] = sel.xpath('.//img[@class="coverart_img"]/@src').extract_first()
        item['descriptors'] = sel.xpath('.//tr[@class="release_descriptors"]/td/meta/@content').extract()
        item['genres'] = sel.xpath('.//span[@class="release_pri_genres"]/a/text()').extract()
        item['media'] = album_info[1].xpath('.//td/text()').extract_first()
        item['rating'] = sel.xpath('.//span[@class="avg_rating"]/text()').extract_first()
        item['release_date'] = album_info[2].xpath('.//td/text()').extract_first()
        item['release_year'] = album_info[2].xpath('.//td/a/b/text()').extract_first()
        item['subgenres'] = sel.xpath('.//span[@class="release_sec_genres"]/a/text()').extract()
        item['title'] = sel.xpath('.//div[@class="album_title"]/text()').extract_first()
        item['url'] = response.url
        item['votes'] = sel.xpath('.//span[@class="num_ratings"]/b/span/text()').extract()
        if len(album_info) == 8:
          item['recorded'] = "" 
          ranking = album_info[4].xpath('.//td').xpath('.//b/text()').extract()
        else:
          item['recorded'] = album_info[3].xpath('.//td/text()').extract_first()
          ranking = album_info[5].xpath('.//td').xpath('.//b/text()').extract()
        if len(ranking) > 1:
          item['rank_year'] = ranking[0]
          item['rank_overall'] = ranking[1] 
        else:
          item['rank_year'] = ranking

        return item
