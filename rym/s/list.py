from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from rym.items import ChartRow, Album
from rym.s.album import AlbumSpider
import sys

class ListSpider(Spider):
    name = "rym-list"
    allowed_domains = ["googleusercontent.com"]
    start_urls = [
        "http://webcache.googleusercontent.com/search?q=cache:rateyourmusic.com/list/amlabella/rolling_stones_500_greatest_albums_of_all_time__updated_2012_edition_/+&cd=2&hl=en&ct=clnk&gl=us"
    ]

    def __init__(self, *args, **kwargs): 
        super(ListSpider, self).__init__(*args, **kwargs) 
        self.start_urls = [kwargs.get('start_url')] 

    def parse(self, response):
        # get listitems
        sel = Selector(response)
        rows = sel.xpath('//table[@id="user_list"]').xpath(".//tr")
        content = []

        for row in rows:
          if len(row.xpath('.//td')) == 4:
            content.append(row) 

        for row in content:
            item = ChartRow()
            item['chart_position'] = row.xpath('.//td[@class="number"]/text()').extract_first()
            item['title_url'] = row.xpath('.//td[@class="main_entry"]/h5/a/@href').extract_first()
            item['cover_art_icon'] = row.xpath('.//td[@class="list_art"]/a/img/@data-delayloadurl').extract_first()
            if item['title_url'] is not None:
              url = "http://webcache.googleusercontent.com/search?q=cache:rateyourmusic.com"+item['title_url'].strip()+"+&cd=2&hl=en&ct=clnk&gl=us"
              request = Request(url, self.parse_album)
              request.meta['item'] = item
            else:
              print item['chart_position']
              print item['cover_art_icon']
              sys.exit(1)
            yield request

    def parse_album(self, response):
        album = AlbumSpider()
        album_data = album.parse(response)
        item = response.meta['item']
        for key,val in album_data.iteritems():
          item[key] = val
        return item
