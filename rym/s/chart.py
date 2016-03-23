from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from rym.items import ChartRow, Album
from rym.s.album import AlbumSpider

class ChartSpider(Spider):
    name = "rym-chart"
    allowed_domains = ["googleusercontent.com"]
    start_urls = [
    "http://webcache.googleusercontent.com/search?q=cache:rateyourmusic.com/customchart+&cd=1&hl=en&ct=clnk&gl=us"
    ]

    def __init__(self, *args, **kwargs): 
        super(ChartSpider, self).__init__(*args, **kwargs) 
        self.start_urls = [kwargs.get('start_url')] 

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
        album = AlbumSpider()
        album_data = album.parse(response)
        item = response.meta['item']
        for key,val in album_data.iteritems():
          item[key] = val
        return item
